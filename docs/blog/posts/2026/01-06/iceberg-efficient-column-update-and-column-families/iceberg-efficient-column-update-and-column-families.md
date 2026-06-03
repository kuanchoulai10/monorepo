---
authors:
  - kuanchoulai10
date:
  created: 2026-06-03
  updated: 2026-06-03
categories:
  - Data
links:
  - blog/posts/2026/01-06/rethinking-iceberg-metadata-v4/rethinking-iceberg-metadata-v4.md
  - "Efficient Column Updates and Column Families in Apache Iceberg": https://youtu.be/YS8HtMJZCnk?si=9BXuR6e-OE6c6O1T
  - "What is a Data Lakehouse?": https://www.databricks.com/blog/2020/01/30/what-is-a-data-lakehouse.html
  - "Lance v2: A Columnar Container Format": https://www.lancedb.com/blog/lance-v2
tags:
  - Apache Iceberg
comments: true
---


# Efficient Column Update 與 Column Families：Iceberg 對 AI/ML Wide Table 的回應

!!! info "TLDR"

    After reading this article, you will learn:

    - 為什麼 Iceberg 現有以 row 為單位的 update 機制，在 AI/ML feature engineering 帶來的 wide table 場景下會變得非常昂貴
    - Iceberg 正在討論的 Flip the Axis 與 Column Families 是什麼，為什麼這個方向同時涵蓋了 column-level update 與 layout flexibility 兩種應用
    - 為什麼這個方向值得期待，以及它跟新一代 table format（例如 LanceDB）的競爭，對 Iceberg 接下來的位置意味著什麼

<!-- more -->

<iframe width="560" height="315" src="https://www.youtube.com/embed/YS8HtMJZCnk?si=9BXuR6e-OE6c6O1T" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
/// caption
[Efficient Column Updates and Column Families in Apache Iceberg](https://youtu.be/YS8HtMJZCnk?si=9BXuR6e-OE6c6O1T)
///

Gabor 與 Peter 都在 Microsoft 的一個研究小組工作，大部分時間都投入在開源 Apache Iceberg 的開發上。他們在 2026 Iceberg Summit 完整介紹了一項仍在早期階段的提案：**Efficient Column Updates** 與 **Column Families**。這個提案要回答的問題是，當 AI/ML feature engineering 讓 Iceberg table 動輒擁有上萬個 column、而且需要頻繁地以 column 為單位更新時，現有以 row 為單位設計的 Copy-on-Write 與 Merge-on-Read 都會變得非常昂貴。提案的核心想法是 **Flip the Axis**：把 update 操作改以 column 為單位進行；而 column-level 拆分一旦成立，這個機制就能繼續推廣到 cache、cold storage、access control 等更多 layout 用途。

我之所以特別想分享這場 talk，是因為雖然自己才剛開始在工作上接觸這塊，就已經實際遇到相同的問題。每次想為一張既有的 wide table 加一個新 column，或更新某個 feature 的計算結果，整張 table 都得重新寫一遍。這個寫入動作的成本會直接反映在 compute 用量與 object storage 的存取費用上，當 column 數量越多、更新頻率越高，這筆成本就越難忽略。talk 裡提到「寫入時間縮短 90%」的數字，背後對應到的就是這筆成本的縮減。

## AI/ML Feature Engineering 帶給 Iceberg Wide Table 的三個挑戰

[Lakehouse 一開始的願景](https://www.databricks.com/blog/2020/01/30/what-is-a-data-lakehouse.html)就是要在同一份資料上同時支撐 BI、analytics 與 AI/ML 等各種 workload，但 Iceberg 的現有設計在那時並沒有把 AI/ML feature engineering 的需求一起納入。在 ML training pipeline 裡，每個 column 都對應到一個 feature，而 feature engineering 這件事本身就需要持續地加新 column、更新舊 column；這種以 column 為單位的 update pattern，跟 Iceberg 為 row-level update 預設的 Copy-on-Write 與 Merge-on-Read 並不對齊。當 ML workload 越來越常見，Iceberg 在 Lakehouse 願景裡原本應該支援的 AI/ML 場景上，就出現了三個具體的挑戰。

### 需要以 Column 為單位頻繁更新 Feature

ML 模型輸入的每一個 feature，本質上就是 table 裡的一個 column：可能是某個聚合數值（例如使用者在過去 30 天的消費總額）、某個 embedding 向量、或是某個機率分數。這些 feature 都有時效性，例如「過去 7 天消費總額」每天的數值都不同，舊值不再有意義，必須整批換成新算好的值。

對 Iceberg 而言，這意味著 update 的單位從以前的「整 row 換掉」變成「整個 column 換掉」。原本以 row 為單位設計的 Copy-on-Write 與 Merge-on-Read 在這個情境下就會變得相當昂貴：為了更新 1 個 column，要把與它寫在同一個 data file 裡的 999 個 column 都讀進來再寫出去，沒有任何一行資料的 row identity 改變。

### 面對上萬個 Column 的 Wide Table 規模壓力

特徵工程很容易讓 column 數量一路成長到上千、上萬個，這在傳統 BI 的 table 上幾乎見不到。例如一張 user profile table，可能會同時存放數百個 categorical feature、數百個 aggregate feature，再加上一兩個 dimension 為 512 或 1024 的 embedding 向量。

這個規模直接放大了前一個挑戰的代價。當 column 數量從 50 變成 10,000，每次「更新 1 個 column 就要重寫整個 data file」的 write amplification 也跟著線性放大，連帶把運算成本與儲存成本都提升一個數量級。

### 遵循快速迭代的實驗節奏

Feature engineering 本質上是一個實驗性的過程：今天試一個新的 time window，明天試一組新的 categorical encoding，後天又想把某個 aggregate 換成另一種演算法。每一次嘗試都會產生新的 column，每一次驗證都可能需要刷新一批舊的 column。

這種節奏代表 Iceberg 在這個場景下面對的每一次 update，都是高頻率、小規模、且 column 維度會持續往上成長的型態。在這種節奏下，每一次 update 的開銷都會被乘上實驗次數，最終決定了團隊一天能跑幾輪實驗、能驗證多少個 hypothesis。

## 重新檢視現有 CoW 與 MoR 的不足

Iceberg 目前處理 update 的兩種策略 Copy-on-Write 與 Merge-on-Read，本來都是針對 row-level update 設計的：你修改某一筆 row 上的某個欄位，CoW 會把整個 data file 重寫一次、MoR 則會把舊 row 標記成 deleted、把新 row 寫到另一個 file。這套以 row 為單位的設計，在 narrow & deep table 上面對的更新通常也都是 row-level 的，運作得很順。可是一旦把 update 換成「整個 column 換掉」的情境，這兩種策略就會把成本花在不該花的地方。

### Copy-on-Write 的寫入放大

承接上一節的場景，假設你有一張 wide table 共 1000 個 column，現在只想把 col5 換成新算好的值。Copy-on-Write 的語意是「把更新後的內容寫成新的 data file，舊的 data file 整份淘汰」，所以它不會只寫 col5，而是會把這個 data file 裡所有 row、所有 column 全部重新讀出來、計算出新版的 col5，再把完整的 1000 個 column 寫回一份新的 data file。

這意味著為了動 1 個 column，要付出 1000 個 column 的寫入成本。如果 table 規模是 N 個 data file，這份 write amplification 會隨 N 線性放大。對於每天可能要更新數十個 feature 的 ML pipeline 而言，這個成本是難以接受的。

### Merge-on-Read 的讀取開銷

Merge-on-Read 降低寫入成本的方式，是讓寫入只負責產生兩樣東西：一個 position delete file（標記哪些 row 在 base file 的位置已經被淘汰），以及一個只含更新後 row 的新 data file。代價則是 query 時的讀取邏輯變複雜：reader 必須同時讀 base file、套用 position delete、再 merge 新 data file，才能還原出當下這份 table 的內容。

問題是這套機制依然是 row-centric 的。即使你只更新了 col5，新寫出來的 data file 仍然得帶上完整的 1000 個 column，因為 stitch 的單位是 row，少了任何 column 都會讓 row 不完整。寫入端的 write amplification 沒有真的消失，只是部分轉嫁到了讀取端；並且每多累積一份 delete file，後續每一次 query 的 merge 成本就會跟著上升。

## Flip the Axis：用 Vertical Split 重新思考更新

如果以上挑戰的共同根源都是「以 row 為單位處理 column-level update」，那很自然的下一個問題就是：能不能把這個軸線翻轉過來，讓 update 從一開始就以 column 為單位進行？這場 talk 的核心提案 **Flip the Axis** 就是這條路的具體實踐：透過 **Vertical Split**，把 update 行為從橫向的「整 row 換掉」改成縱向的「只寫被動到的那幾個 column」，並把跨檔案的 stitch 邏輯延後到讀取時才處理。

關於這個方向的具體成效，talk 後段分享了一份與 Apple 團隊合作的 Spark POC，分別針對寫入端的節省與讀取端的代價做了量測，下面引用的數字都來自這份 POC。

### 只寫入被更新的 Column Update File

承接 CoW 重寫整份 data file 的情境，假設你執行 `UPDATE tbl SET col1 = concat('new', id)`，過去得把所有 row、所有 column 都重寫一遍。Vertical Split 想做的事情很簡單：既然只有 col1 的值會變，那麼產出的檔案就只該包含 col1，其餘 999 個 column 完全不必碰。

實際的 write path 大致是這樣：scan 階段只讀計算 col1 所需的最小欄位集合（在這個例子裡是 `_file`、`_pos`、`_partition` 與 `id`），算出新的 col1 之後，依照 `_file` shuffle 分組、依照 `(_file, _pos)` 排序，最後為每一份原始 data file 各寫出一份只含 col1 的 column update file。寫完之後再透過類似下面這段 API 把 mapping 一次 commit 到 metadata：

```java
table.newColumnUpdate()
  .withFieldIds(fieldIds)
  .addColumnUpdate(FILE_A, updateFileA)
  .addColumnUpdate(FILE_B, updateFileB)
  .commit();
```

從寫入端的角度看，原本「動 1 個 column 等於寫 1000 個 column」的 write amplification 直接降為「動 1 個 column 就只寫 1 個 column」。對應到 POC 的數字，在 R1W1（輸入 1 個 column、輸出 1 個 column）的情境下，寫入時間縮短超過 90%；即使提高到 R20W20，也仍能省下約 75%。

### 用 Composite Reader 在讀取時 stitch

承接寫入端的設計，讀取端要解決的問題就變得明確：當一份 table 的某些 column 散落在 base file、某些 column 散落在多份 column update file 時，reader 必須能在 query 執行階段，把這些散落的 column 重新組合回完整的 row。Iceberg 在這條路上引入的關鍵元件是 **Composite Reader**。

以 `SELECT col1, col2, col4 FROM tbl` 為例，Composite Reader 會先讀 metadata 來判斷每個 column 的來源：col1 沒被更新，從 base file 讀；col2 被某份 update file 覆寫過，要去那份 update file 讀；col4 完全是新增的，只存在另一份 update file 裡。確定好來源之後，Composite Reader 會為每個來源建立各自的 reader、平行讀出資料，再用一個 row identity（例如 `__row_id` 或 `_file + _pos`）把同一個邏輯 row 的 column 對齊、stitch 成最終結果。對 query 端而言，整個過程看起來跟讀一份普通的 Parquet 檔案沒有差別。

### 處理 Row Group 對齊帶來的讀取開銷

讀取端的主要成本來自底層 Parquet 結構不對齊。stitch 邏輯本身相對便宜，真正昂貴的是 row group 邊界無法在 update file 上對齊：base data file 通常很大，例如 512MB，內部會被切成多個 row group 以方便平行讀取；column update file 則通常很小，往往只有一個 row group。當 reader 想要平行掃 base file 後半段的 row group 時，它在 update file 裡找不到對應的起始 offset 可以直接 seek 過去，必須先從 update file 開頭一路遍歷下去，才能定位到正確的縫合點。

POC 也量出讀取端的代價：當 query 只需要 stitch 一份 column update file 時，整體讀取會多出約 10% 的開銷；當 update 累積到 20 份 column update file 時，這個開銷會上升到約 35%。Talk 裡也提到這部分的優化方向，例如善用 dictionary encoding 讓 update file 進一步縮小，或從 file format 層級提供更友善的 offset metadata。整體看來，Vertical Split 把 column-level update 的寫入成本降低了一個量級，代價是讀取端被引入了一個目前在 10–35% 量級、且仍有改善空間的 overhead。

## Column Families：重新定義的 Layout 設計

到這裡為止，Vertical Split 都還只是一個讓 column-level update 變便宜的機制。Talk 後半段由 Peter 接手，他提出的觀察是：既然系統已經能把同一張 table 的不同 column 物理拆到不同檔案、再於讀取時 stitch 回完整 row，那這份能力其實也可以被當作一種 **layout 工具**，不必只用在 update 場景上。Peter 把這個概念稱為 **Column Families**，讓使用者依照 access pattern 主動把 column 分群、選擇要落在什麼樣的檔案上，並以此推導出下面幾種具體的用法，最後再透過一份微基準測試來驗證整體可行性。

### 提升讀取效能

承接 Vertical Split 的能力，假設一張 user profile table 有 1000 個 column，但日常 query 真正會碰到的可能只是其中幾十個 hot column（例如使用者 ID、年齡、最近一次活躍時間、目前等級等）。在原本的單檔案 layout 下，這些 hot column 與其他冷門 column 物理混雜在同一份 Parquet 檔案裡，cache 也只能粗粒度地以整份檔案為單位：要嘛整份載入 cache，要嘛完全沒上 cache。

把這些 hot column 獨立成一個 column family、物理上拆到專屬的檔案後，cache 層就可以只服務這個小而集中的子集：檔案大小通常只有原本的幾十分之一，能完整放進 cache；其他不需要 cache 的 column 則自然落在比較慢、比較便宜的 storage 上。query 在大多數情況下只需要打到 hot column 檔案，cache hit rate 上升，整體 latency 自然下降。

### 降低存儲成本

對應 hot column 的另一面是 cold column：某些 audit log、debug-only metadata、或久遠的歷史 feature，可能一個月只被讀到幾次，卻佔據了不小的儲存體積。如果它們混在主要的 Parquet 檔案裡，整份檔案就只能放在比較昂貴的高速 storage tier 上，等於是讓不常用的資料一起付高 storage 費用。

把 cold column 獨立成一個 column family 檔案後，這份檔案就可以直接放到便宜的 cold storage（例如 S3 Glacier 或對應的低頻存取等級），只在真的需要時才付出 retrieval 成本，平常的 storage 帳單則大幅下降。當 wide table 規模一旦進到 TB、PB 等級，這種冷熱分層帶來的成本節省會非常可觀。

### 增強安全控管

身分證字號、信用卡號、銀行帳戶這類敏感欄位，在傳統 Parquet layout 下會跟其他 column 一起寫在同一個檔案裡。即使上層 catalog 或 query engine 有 column-level access control，底層只要任何流程能讀到那份檔案，技術上就有可能解析出敏感欄位：query engine 漏洞、或某段 log 不小心 dump 整個 row，都可能成為突破口。

Column Families 讓這類欄位可以被指定為一個獨立的 column family，物理上落在一個只有特定身份才能讀的檔案夾或 bucket 內，並由 object storage 既有的 file-level ACL 處理權限控管。一般的 ML training pipeline 連那份檔案的 read permission 都沒有，從物理層級就排除了存取的可能；同時 audit log 上也能直接看到誰存取了 sensitive column family，合規回報相對單純。

### 改善壓縮效率

Parquet 的壓縮機制是以 column chunk 為單位，當同一份檔案裡混雜了寬度差異極大的 column（例如只有 4 byte 的 integer，與動輒幾 KB 的長字串或 JSON blob），壓縮演算法很難對所有 column 都做到理想的壓縮率。寬的 column 會佔掉大部分檔案空間，連帶讓整份檔案的 metadata 變得龐大；窄的 column 即使有重複模式可以高度壓縮，也享受不到同等程度的編碼最佳化。

把寬度相近、資料模式接近的 column 分成同一個 column family、各自寫到專屬的檔案，每份檔案內部的 column 就會比較同質，編碼與壓縮選擇也比較容易最佳化。不過 Peter 也誠實指出，總體壓縮率最終仍然會取決於實際資料模式：在完全隨機的資料上，把一張 10,000 個 column 的 table 拆成 10 個各 1,000 個 column 的 column family 檔案，總大小跟維持單檔基本不會差太多；只有當資料本身具備可以被壓縮的 pattern 時，異質性切開帶來的差距才會明顯。使用者必須自行 benchmark 過才知道在自家資料上是否真的划算。

### 驗證整體可行性

除了上面四個應用場景，Peter 還針對 Column Family 整體的讀寫成本做了一份微基準測試：把一張 10,000 個 column 的 table 切成 1、2、5、10 個 column family，分別量測單執行緒與多執行緒讀取下的表現。結論是這套設計在不同 compute 環境下的表現落差非常明顯。

在單執行緒模式下，Column Family 的讀取效能與原始 Iceberg 大致相當：stitch 帶來的額外開銷剛好被 metadata 變小帶來的節省抵銷掉。把讀取改成平行（每個 column family 各自一個 reader）後，微基準測試裡的效能可以提升 80–90%。但同樣的設計在 Spark 上實測時，效能卻反過來下降了 30–40%，原因是測試環境的 CPU 核心數不足，平行 reader 競爭核心反而造成額外的 scheduling 開銷。這個結果也反映了一件事：Column Family 要在分散式 compute engine 上真正發揮潛力，前提是底層有足夠的並行運算資源，這也是社群接下來需要繼續處理的方向。

## Next Steps

整體看下來，Efficient Column Update 與 Column Families 是一個我非常看好的方向。它把 column-level update 與 layout flexibility 直接做進 table format 的底層，而不是靠應用層或 compute engine 去迴避 row-centric 的限制。這是 Iceberg 在 AI/ML workload 上真正補齊 Lakehouse 願景的關鍵一步。

值得對照的是，新一代的 table format 例如 **[LanceDB](https://www.lancedb.com/blog/lance-v2)** 早就把這類 column-level 的能力做成核心特色之一。它原生就以 column 為單位處理 update、cache 與儲存策略，這也是 LanceDB 在目前 lakehouse 競爭格局裡成長最快、最多人看好的原因之一。當 AI/ML 工作流逐漸主導 lakehouse 上的 read/write pattern，誰能把 column-level 的成本降到合理區間，誰就會被選為新一代基礎建設的預設選項。

面對這樣的壓力，期待 Iceberg community 能盡早把 Efficient Column Update 與 Column Families 納入正式版本。這對既有使用者是一個明顯的改善，也是 Iceberg 維持 Lakehouse 主流地位的必要動作。
