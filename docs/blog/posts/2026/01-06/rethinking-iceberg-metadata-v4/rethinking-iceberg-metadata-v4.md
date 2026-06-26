---
authors:
  - kuanchoulai10
date:
  created: 2026-06-02
  updated: 2026-06-26
categories:
  - Data
links:
  - "Breaking the Mold: Re-thinking Iceberg Metadata Structure in v4": https://youtu.be/ymUCDJV19tE?si=o0rZjQtx7PYP-iWW
tags:
  - Apache Iceberg
  - The Lakehouse Series
comments: true
---


# Re-thinking Iceberg Metadata Structure in v4

!!! info "After reading this article, you will be able to answer..."

    - 為什麼沿用多年的三層 metadata 結構，在新場景下開始不夠用了？
    - Iceberg v4 提出的 Adaptive Metadata Tree 想解決什麼？怎麼解？
    - 這個方向有什麼值得期待的地方？隱憂在哪裡？

<!-- more -->

<iframe width="560" height="315" src="https://www.youtube.com/embed/ymUCDJV19tE?si=o0rZjQtx7PYP-iWW" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
/// caption
[Breaking the Mold: Re-thinking Iceberg Metadata Structure in v4](https://youtu.be/ymUCDJV19tE?si=o0rZjQtx7PYP-iWW)
///

[Steven Wu](https://www.linkedin.com/in/stevenzhenwu/) 與 [Amogh Jahagirdar](https://www.linkedin.com/in/amogh-jahagirdar-aab204b6/) 都是 Apache Iceberg PMC member，分別在 Snowflake 與 Databricks 擔任 software engineer。他們在 2026 Iceberg Summit 完整介紹了社群正在討論的 **v4 metadata 重構**：從 metadata JSON、manifest list、manifest file 這套維持多年的**三層結構**，走向會隨資料規模動態調整的 **Adaptive Metadata Tree**。

原本的三層結構足以支撐 PB 資料規模的 table，但隨著 small commit、頻繁 DML、wide table 更新這些工作負載逐漸變得常見，固定深度的 metadata tree 反而開始拖累 latency 與 write amplification。本文整理自這場分享，先看現有結構在這些場景下面對的五個挑戰，再一條一條看 v4 的對應設計。


## 3-Layer Metadata Tree 的五大挑戰

目前的 Iceberg metadata 都建立在同一套三層結構上：

- Snapshot 對應一份 **metadata JSON**
- Metadata JSON 指向一份 **manifest list**
- Manifest list 再指向一批 **manifest files**
- Manifest file 裡面存著 **data file entries**

這套結構在 PB 資料規模且寫入頻率不高的 big tables 上表現得很好。但隨著 small commit、頻繁 DML、wide table 更新這些工作負載變得常見，固定深度的三層結構就會在以下五個地方面對挑戰：

### 三層 Sequential I/O 拖高 Latency

先從 metadata files 的讀寫順序講起。寫入時，每次 commit 至少要寫三份 metadata files：Writer 先寫 manifest file，再寫引用它的 manifest list，最後寫指向 manifest list 的 metadata JSON。**三份檔案之間有引用關係，後一份必須等前一份寫完才能寫，三輪 I/O 沒辦法並行。**

讀取時也是差不多的情況：Reader 拿到 table location 後，先讀 metadata JSON 取得 manifest list 的位置，再讀 manifest list 取得 manifest files 的位置，最後讀 manifest files 才能定位到 data files。**前一輪沒拿到位置，後一輪就不能開始，三輪 I/O 一樣沒辦法並行。**

這套順序在 PB 資料規模的 table 的 batch query 上不會造成太大的瓶頸，metadata I/O 占整體 query 時間的比例本來就不高。**但放到對 sub-second latency 敏感的 read 場景，或一次只寫幾筆 entry 的 small write 場景，三輪 sequential round-trip 就會拖高 latency，光是 metadata 部分就要 500 ms 起跳。**

### CoR 行為造成的的 Manifest Write Amplification

接著看 manifest file 的更新方式。如果仔細觀察和思考的話，會發現 manifest file 目前採用的是 **copy-on-write 策略**：只要更動其中任何一個 data file 的紀錄，writer 就必須把整份 manifest file 重寫一次。

舉個例子。假設一份 manifest file 記錄了 1,000 個 data files 的位置與統計資訊，現在 query engine 只想刪掉其中 1 個 data file。Iceberg writer 必須寫一份全新的 manifest file，內容包含另外 999 個沒有變動的 data files 的完整紀錄，加上 1 個被標記為 deleted 的 data file 紀錄。接著 manifest list 也要更新，將 pointer 從舊 manifest file 替換為新 manifest file。

為了更動 1 個 data file 的紀錄，卻要重寫整份 manifest file，這就是 manifest write amplification 的核心。對 high-frequency DML 與 streaming compaction 這類場景，多寫的 metadata 量會相當可觀。

### Two-Phase Planning 拖慢 File Scan 啟動

再來是 file scan 啟動前的成本。

目前 **data files** 與 **delete files**（positional delete、equality delete、DV）分開存在不同的 manifests 裡。Query engine 要跑 file scan 之前，必須做兩階段 planning：

- **Phase 1**：讀取符合條件的 **delete manifests**，建出一份 **Delete File Index**，目的是回答「某個 data file 對應到哪些 delete files 或 deletion vectors」。
- **Phase 2**：讀取 **data manifests**，根據 partition info、column stats、query filter 找出實際要掃的 data files。每找到一份 data file，就跟 Phase 1 的 Delete File Index 對照，找出對應的 delete files，組成 scan tasks 交給 query engine。

兩階段是順序的，phase 1 沒做完，phase 2 就不能開始。對 **time-to-first-task** 敏感的 streaming engine 與互動式 query 場景，這套流程會帶來三個成本：

- planner 多一輪 matching 邏輯
- driver 多維護一份 Delete File Index 在 memory 裡
- scan tasks 要等 phase 1 跑完才開始產生。

### 跨 Snapshot 比對 Manifest 拖高 Change Detection 成本

接下來看 snapshot 之間怎麼比對變更。

Iceberg 規範允許 writer 在新的 snapshot 裡直接省略已刪除的 entries。舉個例子：舊 manifest 有 100 筆，新 manifest 可能只剩 99 筆，少掉的那一筆就是被刪掉的 data file。

問題是，reader 只看新 snapshot 沒辦法知道少掉的是哪一筆。要做 change detection，需要拿前後兩個 snapshot 的 manifests 全部讀進來逐一比對，才能還原出「這一輪刪了什麼、新增了什麼」。

對 streaming reader 與 CDC consumer 這類仰賴 incremental change 的場景，change detection 成本會隨 table 規模放大。table 越大、manifests 越多，每次比對都要再掃一輪完整的 metadata。

### Wide Table 更新需要 Full Column Rewrite

最後這條落在 data file 層，不在 metadata 層，但同樣是 v4 想處理的對象之一。

ML 與 feature store 場景常見的需求：在一張 wide table（幾百到幾千個 columns）上新增一個 score column，或更新某個既有 column 的值。Iceberg 目前的 update 是 file 等級的 copy-on-write：要動其中一個 column，writer 必須重寫整份 data file，把其他幾百個沒變動的 columns 也一起重新寫一份。

對 wide table 來說，**為了動一個 column 就要重寫剩下幾百個 columns，成本顯然不成比例。**


## Adaptive Metadata Tree：隨資料規模動態調整

前面五條挑戰看似零散，但 v4 的回應建立在同一個原則上：**metadata tree 的深度與維護方式應該隨資料規模動態調整**。具體做法落在四個機制：一個調整 metadata tree 的結構本身，另外三個調整 manifest 內部該怎麼維護。

### Multi-Level Manifest Tree

先看 metadata tree 的結構本身。前面提到，三層結構不論 table 多大都得寫滿 metadata JSON、manifest list、manifest file 三份，small write 場景的 commit 路徑因此很長、latency 高。

v4 把 metadata tree 的深度交給 table 規模決定，不再強制走完三層。深度分成三個層級：

- **0-level**：table 只有幾十個 data files。所有 metadata 都存在 **REST Catalog** 的資料庫裡，不寫任何 metadata 檔案到 object store。Commit 就是一次 catalog transaction。
- **1-level**：中型 table。只寫一份 **root manifest**，裡面直接列出所有 data file 紀錄，跳過 manifest list 這一層。
- **2-level**：大型 table。root manifest 引用一批 **leaf manifests**，跟現在的三層結構類似。

Table 規模成長時，metadata 結構也跟著加深，不需要 migration 或重建整個 table。對小 table 來說，commit latency 有機會從 ~500ms 級別降到 ~50ms 級別；對大 table 來說，原本的結構就會從 3 層變成 2 層結構，沒有 regression。

### 導入 Inline Manifest DV，改善 Metadata Write Amp

接著看怎麼處理 manifest write amplification。前面提到，manifest 採用 copy-on-write，只動 1 個 data file 紀錄就要重寫整份 manifest，999 個沒變動的紀錄全部跟著被複製一輪。

**v4 把 data layer 已經在用的 deletion vector 概念套用到 metadata 層**。當某份 manifest file 裡的 data file 紀錄要被刪掉時，writer 不再重寫整份 manifest，而是在**引用該 manifest 的位置**（也就是它的 parent，例如 manifest list 或 root manifest）加上一份 **Inline DV**。這份 DV 是一個 logical bitmap，標出該 manifest 中哪些位置（index）的紀錄已經被刪除。

Reader 讀那份 manifest file 時會同時讀 parent 上的 Inline DV，知道哪些 entries 要當作 deleted 忽略。

這帶來兩個直接的好處：

- **Write amplification 大幅降低**：999 個沒變動的紀錄不用再被複製，只多寫一份小的 bitmap。
- **Cache 命中率提升**：原本的 manifest file 沒有被改寫，已經 cache 過的 reader 可以繼續使用。

### 應用 Column File Overlay，簡化 DV Update

再來看怎麼簡化 DV update。Inline Manifest DV 處理的是「manifest 中某些 entries 整筆被刪除」的場景，但 entry 本身要更新（例如某個 data file 的 DV 改了）會遇到另一個問題：data file entry 裡包含大量 stats，要動其中一個欄位（DV reference）就得整筆重寫，跟前面 manifest 的 write amplification 是同一個問題。

v4 的解法是 **Column File Overlay**：要動 entry 中的某一個 column，writer 不重寫整筆 entry，只寫一份只包含那個 column 新值的小檔案。Reader 在讀取 entry 時，會結合 base 上的紀錄與 overlay file 上的對應欄位。

把這個機制套用在 DV update 上：DV 變成 entry 中的一個 column，每次更新 DV 只要寫一份只含新 DV 的 overlay file，base 的 stats 全部維持不動。

這套機制還有一個 side effect。因為 column overlay 是個通用機制，**data files 與 metadata files 可以共用同一套 read / write 邏輯**。原本 stats、DV、column updates 散在不同層的處理，可以收斂成同一個 pattern。

### 採用 Explicit Status + Diff DV，加速 Change Detection

最後看怎麼加速 change detection。前面提到，writer 可以在新 snapshot 直接省略已刪除的 entries，reader 只看新 snapshot 沒辦法判斷哪些 data files 被刪了，必須跟前一份 snapshot 的 manifests 做全量比對，成本隨 table 規模放大。

v4 規範要求 writer 為「被刪除的 entry」保留一個 **explicit deleted status**。這個被刪除的 entry 至少要在下一個 snapshot 之後才會真的從 manifest 中移除。這樣 reader 看新 snapshot 就知道：這個 entry 是「在這一輪刪掉的」，不用比對前一個 snapshot 才能推斷。

但這還不夠。Manifest 層級的變更（例如 leaf manifest 中哪些 positions 被標記為 deleted）也需要快速可見。v4 在每份 manifest 上引入 **Diff DV**：

- **Regular Manifest DV**（前面 Inline Manifest DV 提到的那一份）：記錄該 manifest 中所有被刪除位置的累積狀態。
- **Diff DV**：只記錄「在這一輪 snapshot 中」被刪除的位置。

如果一個 snapshot 在 leaf manifest 中刪掉第 2 筆 data file 紀錄，這份 manifest 的 Diff DV 就只標 position 2。Reader 想找出該 snapshot 的變更，讀 Diff DV 一次就知道。

代價是 manifest 多存一份小的 bitmap。好處是 change detection 不再需要跨 snapshot 比對，streaming reader 與 CDC consumer 可以直接讀新 snapshot 取得 incremental change。


## Next Steps

上面五條挑戰加上四個機制看下來，可以感覺到 Iceberg community 在認真回應 small commit、頻繁 DML、wide table 更新這些新工作負載的需求。這些都是 Iceberg 要從 PB 級 batch table 走向更多應用場景的必要演進。沒有 v4 的 metadata 重構，前面那幾條挑戰會持續限制 Iceberg 在 streaming engine 與 sub-second read 場景上的可用性。

話說回來，如果你看完上面 v4 的實作細節覺得有點頭暈，這也是我的感受。v4 用了非常多複雜的機制（Inline Manifest DV、Column File Overlay、Diff DV、Adaptive Metadata Tree）來處理同一件事：**metadata 本身已經是一份 big data**。我會感到隱憂的點是，這套複雜度有相當部分來自於 metadata 完全被放在 file system 層級來處理。把每一份 manifest、每一個 DV、每一份 overlay 都當成 object store 上的檔案來操作，自然就會需要這種 big data 等級的設計。這真的是長期最好的方向嗎？未來還有多少彈性可以演進？我目前還沒有答案。

即便有這層隱憂，我還是很看好 Iceberg 的下一步。Iceberg 對我來說最有價值的地方，是它已經成為一個讓各家把共識凝聚在一起的開源社群。Snowflake、Databricks、Netflix 這些團隊的 PMC member 都在貢獻和討論這套規格。技術上的隱憂可以等社群慢慢驗證和修正，但這個社群本身已經是 Iceberg 最大的資產。我會繼續關注 Iceberg 在 v4 上的進展，期待這些大神能為 Iceberg 帶來更完整的特性。
