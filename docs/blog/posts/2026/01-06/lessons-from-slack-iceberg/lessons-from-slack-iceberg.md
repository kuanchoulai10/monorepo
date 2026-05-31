---
authors:
  - kuanchoulai10
date:
  created: 2026-05-31
  updated: 2026-05-31
categories:
  - Data
links:
  - "Maintaining Iceberg at Scale: Lessons from Slack | 2026 Iceberg Summit": https://youtu.be/NRSlundcwvc?si=NOw46genitJRooXX
tags:
  - Apache Iceberg
  - Slack
comments: true
---


# Lessons from Slack：在 180PB 規模上維運 Iceberg

!!! info "TLDR"

    After reading this article, you will learn:

    - Slack 如何在每天有超過 300TB 資料流入 180PB 規模的 Data Lakehouse 下，穩定維持 99.9% 的 Iceberg 維護成功率
    - Slack 在開發 IceChipper 時的思考過程：4 種資料、5 條設計準則、3 條被否決的替代方案
    - Slack 在維護 4,000 張 Iceberg tables 過程中遇到的 3 大痛點以及他們如何因應

<!-- more -->

<iframe width="560" height="315" src="https://www.youtube.com/embed/NRSlundcwvc?si=q1bDIgJk901Dwp6c" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
/// caption
[Maintaining Iceberg at Scale: Lessons from Slack](https://youtu.be/NRSlundcwvc?si=x4urD1PX3EK816NX)
///

Lawrence Weikum 是 Slack 的 Staff Software Engineer。他在 2026 Iceberg Summit 分享了 Slack 那座 **180 PB** 數據湖的 Iceberg 採用經驗，這座湖上跑著 **35,000 張 tables** 與 **29,000 條 pipelines**，每天還在以 **250 TB** 的日誌與 **55 TB** 的 CDC 變更數據持續長大。

規模本身已經夠驚人，但這場 talk 最吸引我的地方，是 Lawrence 把 Slack 一路走來的決策過程都攤了出來：哪些痛點讓他們動手換、為什麼採用率曾經停下來、又怎麼把維護整理成一套能擴展的系統。本文整理自這場分享，從 Slack 用 Hive 時代踩到的瓶頸開始講起。


## Iceberg 之前，Hive + Parquet 的四個瓶頸

在採用 Iceberg 之前，Slack 的數據湖架構主要建立在 **Hive Metastore + Parquet** 之上。這套組合在規模還小的時候運作得不錯，但隨著資料規模越來越大、tables 越來越多，四個面向的痛點逐漸浮上來：

### Partitioning strategy 綁死 table 結構

在 Hive 時代，一張 table 的 partitioning strategy 一旦定下來就很難變更。當不同的查詢需求需要不同的 partitioning 時，最直接的解法就是把同一份資料用新的 partitioning strategy 再寫一份成新的 table。久而久之，Slack 必須維護多份內容相同、只是 partitioning 不同的 tables，儲存成本與管理負擔都跟著增加。

### Hive Metastore 成為效能瓶頸

Slack 某些大型 tables 擁有數百萬個 partitions。Hive Metastore 作為一個 centralized service，所有 partition 的 metadata 都得從同一個地方讀寫；到了百萬級 partitions 的規模，光是 query planning 階段要從 Metastore 拉出所需的 partition metadata，就成了拖慢查詢的瓶頸。

### 災難恢復仰賴手動補回 schema 與 partitions

在 Hive 時代，誤刪一張 production table 是場惡夢。工程師必須先把 schema 從備份或記憶裡拼回來，再用 `MSCK REPAIR TABLE` 或手動 `ADD PARTITION` 把 partitions 一個一個補回去，整個過程動輒幾小時起跳，而且容易出錯。

### Hive 缺乏支援 Data Mesh 的共享能力

Slack 內部已經採用 Data Mesh 架構，希望各團隊能在不複製資料的前提下，把自己擁有的 tables 分享給其他團隊或不同的 Compute Engine 使用。但 Hive 在這條路上一直是個明顯的阻礙：它的 Catalog 設計綁定特定的生態系，跨團隊或跨 Compute Engine 的存取通常得回到「複製一份資料給對方」的老路，違背了 Data Mesh 強調的 zero-copy sharing。


## Adopting Iceberg: from batch to streaming, then CDC

Slack 是透過三階段逐步導入 Iceberg 的：先從轉換 batch 到 streaming pipeline 開始，再擴展到 CDC pipeline，最後讓 Iceberg 成為 business metrics、telemetry 等重要資料的 table format。

### First move: Kafka Connect

Slack 最初導入 Iceberg 的動機，是想把原本的 batch ingestion 改成 streaming ingestion。他們選擇 **Kafka Iceberg Sink Connector** 作為工具。之所以選擇它是因為它能把 Kafka topic 上的資料快速同步進 Data Lakehouse，並且原生支援 Iceberg table format。對 Slack 來說，這條 pipeline 的成功也讓 Iceberg 從一個「值得評估的選項」變成「下一步要擴展到哪裡」的問題。

### Next move：CDC pipeline

在第一條 streaming pipeline 完成且穩定後，Slack 著手挑戰更難處理的 CDC pipeline。整條 pipeline 的資料流向是這樣的：上游的 Vitess 資料庫由 **Debezium** 監控變更，產生 CDC 事件後送進 Kafka topics；接著由 **Kafka Iceberg Sink Connector** 把這些變更寫進對應的 Iceberg tables。每小時 Slack 會在這些 tables 上跑一次 `MERGE` statement，從累積的 change log 中算出與上游一致的 snapshot。

因為這類資料的特性是頻繁 upsert 與 delete，Slack 在這些 tables 上啟用了 **Merge-on-Read (MOR)** 模式：寫入時只記錄 delete files，不立即重寫資料本身。這讓寫入端的延遲與 lock 持有時間都明顯下降，代價是會累積大量 small files 與 delete files，必須靠後續的 compaction 才能維持查詢效能。

### Payoffs：Performance, Flexibility, Sharing

走過 streaming 與 CDC 兩個階段，Slack 在 Performance, Flexibility, 和 Sharing 三個面向上都有很好的改善。

**Performance**：在 multi-petabyte 規模的分析資料集上，查詢速度比 Hive 時代加快了 **70%**。關鍵在於 Iceberg 把 partition 與 file level 的 metadata 寫進 S3 上的 manifest files，query planning 階段可以靠這些 metadata 直接跳過大量無關 files，不必再讓 Metastore 一個一個查 partition。

**Flexibility**：**partition evolution** 讓 Slack 在改變 partitioning strategy 時，不必再把整張 table 重寫一遍；**snapshot rollback** 與 **table reregistration** 把過去要花幾小時的災難恢復縮到 30 秒內完成；**redaction** 因為可以精準定位到包含特定資料的 files，成本也明顯下降。

**Sharing**：透過 **Iceberg REST Catalog**，Slack 的 Data Mesh 終於做到了真正的 **zero-copy sharing**。同一份資料可以同時被不同團隊、不同 Compute Engine 直接讀取，不必再複製給每個下游。


## Iceberg 的隱藏成本

Slack 導入 Iceberg table format 確實改善了在 Hive 時代的問題，但這條路上沒有免費的午餐。Lawrence 在 talk 中點出一個讓我印象深刻的觀察：Iceberg 的採用率在 Slack 內部一度停在 plateau 上，新的 tables 不再以同樣的速度被導入。他用一句話總結原因：

> **Maintenance is the cost of adopting Iceberg.**

真正卡住擴展的，是維護 Iceberg 所需要的工程量被低估了。為了讓 Slack 能繼續大規模採用 Iceberg，他們評估過幾個方向。

**第一個方向是讓各資料團隊自己負責維護自己擁有的 tables。** 畢竟資料是他們建的，理論上他們最了解。但實際評估後，Slack 發現這條路會帶來高得不合理的 onboarding cost：每個團隊都需要被教育一遍 Iceberg 的 maintenance 細節，知識傳遞的負擔會持續累積，而且各團隊的執行標準很難保持一致。

**第二個方向是提供一組統一的 curated scripts 或 self-service 工具**，讓各團隊用同一套工具自己跑維護。這雖然解決了執行不一致的問題，但團隊的回饋很直接：他們只想專注在資料內容與洞察上，不想花時間處理底層的 plumbing。對資料團隊來說，Hive 是 plumbing、Iceberg 也是 plumbing，他們希望這層完全不出現在自己的工作清單裡。

**第三個方向是直接採用 AWS 的 S3 Tables**，把 maintenance 完全外包給雲端服務。Slack 約一年半前曾與 AWS 討論過這個選項，但當時 S3 Tables 缺乏 Slack 需要的微調能力，例如無法精確控制維護頻率，也無法為了 file pruning 做 internal sorting 等優化。對 Slack 的規模與既有經驗來說，這條路的代價反而比自建更高。

三條路都走不通之後，Slack 最後選擇由基礎設施團隊建立一套 **centralized maintenance service**：所有的維護動作收斂到一個地方執行，使用者完全不需要關心底層細節，執行標準也能保持一致。為了把這套系統設計好，他們先做了一件事：把資料分類。


## 根據資料特性決定維護策略

在動手蓋系統之前，Slack 先做了一件事：根據讀寫模式，把 Data Lakehouse 內的 tables 分成四類。每一類有不同的變動頻率、不同的 file 累積方式，也對應到不同的維護動作與 SLA。

### Static: low change, low maintenance

變動極少的 tables 屬於 Static 類，常見例子是 billing tiers 這類兩三年才更新一次的設定資料。它們的寫入頻率極低，幾乎所有查詢都是讀取，因此沒有 small files 或 delete files 累積的問題。對這類 tables 來說，snapshot expiration 不需要每天執行，整體維護成本最低。

### Append-only: batch-stacked, lightweight maintenance

Append-only tables 主要是 batch-stacked 的資料，例如每小時或每天追加一次的長期 logs。它們的寫入模式是 append-only，偶爾會做整個 partition 的 insert overwrite，但既不會產生 delete files、也不會在 partition 內反覆改寫。因此維護需求與 Static 接近：snapshot expiration 與 manifest rewrite 為主，整套流程通常幾分鐘就能完成。

### Streaming: compaction is the core

Streaming tables 屬於持續寫入的類型，例如稍早提到的 streaming ingestion 與 CDC pipeline 寫進的 tables。問題在於：每一次 micro-batch 的提交都會產生新的 small files，沒有人介入的話，這些 small files 會越累積越多，把 query planning 與實際讀取都拖慢。對這類 tables 來說，compaction 是維護的核心動作，而且 SLA 通常要拉到比每天更嚴格的頻率，例如每小時一次，這樣每次 compaction 處理的資料量也比較可控。

### Volatile: delete files are the hard part

Volatile tables 是維護難度最高的一類，常見於 CDC pipeline 寫進的 tables。它們的特性是頻繁 upsert 與 delete，搭配 MOR 模式運作：每次寫入只在 delete files 裡記下「這一筆資料已失效」，原始 data files 維持不動。這在寫入端省下大量重寫成本，但代價是 delete files 會持續累積，讓 query 端在讀取時必須做更多的合併計算。要維持查詢效能，必須定期把 delete files 重寫回 data files 裡，這個動作的成本也會隨著 table 規模 compound。


## 維護系統的五個設計需求

回頭看 4 種資料的維護需求，5 個共同的設計需求就清楚了：

**Frequency**

所有 tables 必須至少每天執行一次維護，否則 snapshot、manifest 與 orphan files 都會持續累積；對於 streaming 與 volatile tables，Slack 把目標朝每小時一次推進，這樣每次 compaction 處理的資料量比較可控、失敗時也容易重跑。

**Partial progress**

在這個規模下，「全有或全無」的 batch processing 不切實際。一個 batch 裡有 35 張 tables 要跑維護，其中一張失敗，不應該讓其他 34 張的進度也跟著 rollback。系統必須允許部分完成、紀錄個別 table 的狀態，下次再回頭處理失敗的那幾張。

**Infrastructure leverage**

Slack 直接重用既有的 **Airflow** 做排程、**Spark on EMR** 做執行，避免為了這套維護服務再多接一套新的 infra，減少額外的維運負擔。

**Visibility**

每一次維護動作的開始、結束、成功、失敗、處理過的 files 數量都要被紀錄下來，並接到 dashboards 給 on-call 工程師查問題。沒有觀測性，4,000 張 tables 的維護一旦出狀況就無從 debug 起。

**Idempotency**

Spark job 在 EMR 上失敗是常態，系統必須能 idempotent 地重試，重啟後可以憑同一個 Run ID 重新取回原本的 lock、接著繼續未完成的工作。


## IceChipper：Slack 的集中式 Iceberg 維護服務

Slack 把這套 centralized maintenance service 叫做 **IceChipper**。它由四個元件組合而成：**Discovery service** 動態納管所有 Iceberg tables，**Airflow** 在預定的時間觸發維護 batch，**Spark on EMR** 真正執行 compaction、orphan file deletion 等操作，**Lock** 與 **Tracking** 兩張 Iceberg tables 則用來協調與紀錄整個流程。

一張 table 從被排程到維護結束的流程是這樣的：Discovery service 從 Catalog 找出所有 Iceberg tables 並登記到 Discovery table；Airflow 觸發 Spark job 之後，job 在 Lock table 上跑一次 `MERGE` 取得一批 tables 的維護 lock，照「先輕後重」的順序執行維護動作，過程中把每一步的狀態寫進 Tracking table；24 小時內若還沒做完，就會被 kill 掉、tables 釋出，等下一輪 batch 再來。

### 從 Catalog 自動發現待維護的 table

Discovery service 的工作是讓 IceChipper 知道「現在有哪些 tables 需要被維護」。它會定期掃描 Catalog，把新出現的 Iceberg tables 自動登記到一張 Discovery table 裡，標記為「active 且 eligible for maintenance」；如果某張 table 從 Catalog 中消失，也會自動從 Discovery table 移除。這套機制讓新團隊與新 tables 無需任何 onboarding 動作就能進入維護排程。Discovery table 同時也支援手動覆寫，讓特定 tables 可以暫時跳過維護，方便工程師處理特殊情況。

### 用既有的 Airflow 與 EMR 撐起執行層

在預定的時間，Airflow 從 Discovery table 撈出一批待維護的 tables，啟動一個 Spark on EMR 的 job。為了避免少數慢 tables 把 EMR cluster 卡死，每個 job 都有 24 小時的 time-boxing，超時就會被 kill、tables 自動釋出，等下一輪 batch 再來。job 內部則用 Spark 的 parallelism 同時處理整批 tables，並嚴格按「required first, then optional」的順序執行：先跑所有 tables 都要做的 snapshot expiration、manifest rewrite、orphan file deletion，再跑只有 streaming 與 volatile tables 需要的 compaction 與 delete file rewriting。

### Locking：避免重複維護

維護動作必須有 lock，否則同一張 table 可能被兩個 actors 同時處理。這不僅會浪費資源，還會在 Catalog 之外產生互相未追蹤的 orphan files。Slack 的 lock 機制只限制 IceChipper 內部，不會阻擋外部的 analytical pipelines 對 tables 的讀寫。

實作上，Slack 直接用一張 Iceberg Lock table 當作 lock 的載體。Spark job 啟動之後，會用 `MERGE` 在 Lock table 上嘗試插入一筆紀錄，Primary Key 是這個 job 的 **Run ID**；`MERGE` 成功就拿到 lock，可以開始維護動作。Run ID 同時讓系統具備 idempotency：如果 Spark job 中途失敗、被重啟，它能憑同樣的 Run ID 重新取回原本的 lock 並從中斷處繼續往下做。

不過 Lock table 本身也是一張 Iceberg table，頻繁寫入會帶來自身的維護成本。Slack 在這張 table 上同時做了兩件事：**batch insert** 把多次小寫入合併成一次提交，降低 snapshot 與 small files 的累積；同時啟用 **MOR** 模式縮短 lock 持有時間。如果 job 因為 infra 問題而中止、沒有正常釋出 lock，Lock table 也設有 24 小時 timeout，超時後 lock 會自動釋出，避免一張 table 永遠卡在「正在維護」的狀態。

### Tracking：紀錄每次維護動作

Lock table 解決了「誰來做」的問題，Tracking table 則回答「做了什麼、結果如何」。Spark job 每執行一次維護動作，例如 snapshot expiration、orphan file deletion、compaction，都會在 Tracking table 裡寫入一筆紀錄，包含開始時間、結束時間、成功或失敗、處理的 files 數量等 metadata。這些紀錄直接接到 dashboards，on-call 工程師可以即時看到 4,000 張 tables 的維護狀況；失敗會被自動分組與排序，方便工程師依優先度修問題。

## 規模、成功率與效率同時到位

一年多下來，IceChipper 在規模、成功率與效率三方面都有很好的成果：

- **規模**：目前負責 **4,000 多張 tables**，能處理的單張 table 規模可達 **17 PB**，每天還會清掉數百萬個 orphan files。
- **成功率**：所有維護操作的成功率達到 **99.9%**。
- **效率**：每個 batch 平均處理 35 張 tables、15 分鐘完成，其中最輕量的 snapshot expiration 等操作甚至只需要 2 分鐘。

這套服務上線之後，Iceberg 在 Slack 內部的採用率也突破了先前的 plateau，開始以倍數持續成長。

## Future Plans

即使 IceChipper 跑出了亮眼的數字，Lawrence 在 talk 結尾並沒有迴避系統的限制。他攤出三類目前還沒解決的問題，也清楚地說明了 Slack 接下來打算怎麼處理。

**Orphan file deletion 的記憶體與 rate limit 雙重壓力**。當一個 batch 要刪掉的 files 多達數百萬個時，Spark driver 收回所有刪除清單時可能會 OOM，即使配給 driver 的記憶體已經提高到 80 GB 也不夠用。檔案實際已經被刪除，但系統會因此失去這次操作的可見性。同時，AWS 的 delete API 有 rate limit，遇到 batch 裡刪太快就只能完成部分刪除，未完成的會累積到下一輪 batch，問題會越來越嚴重。

**大型 streaming tables 的 batch 衝突**。當好幾張流量大、體積大的 streaming tables 被排到同一個 batch 一起做 compaction 時，這幾張重量級 tables 會佔用所有 EMR 資源，較小的 tables 沒有資源可用，最後就觸發 24 小時的 timeout 被 kill 掉。未完成的維護會被排進下一輪 batch，惡性循環會持續放大。

**S3 lifecycle policy 的舊設定衝突**。Slack 早年針對 file level 的資料保留設定了大量 S3 lifecycle policies；如果轉移到 Iceberg 之後忘記清掉舊的 policy，這些 policy 可能會誤刪 Iceberg 的 manifest 或 data files，導致查詢失敗。幸好 Slack 的 S3 buckets 開啟了 versioning，被誤刪的 files 還能救回來，但從這個 edge case 我們可以知道，從 file level 維護過渡到 dataset level 維護的過程中，舊有的清理機制必須一起檢視。

對應這些挑戰，Slack 把方向集中在兩條主軸：

**核心與重型操作的解耦**。Compaction 與 orphan file deletion 這類重型操作會從 IceChipper 主流程獨立出去，擁有自己的排程節奏與 resource pool，不再與 snapshot expiration、manifest rewrite 等核心操作競爭 EMR cluster 資源。為了支援這個拆分，Slack 也正在評估把 orchestration tool 從 Airflow 換成 Temporal，讓系統可以按「操作類型」而非「table」動態組成 batch，輕量與重型工作各自走自己的 pipeline。同時，Slack 計畫納入 Puffin files 提供的 stats 與 partition stats，讓系統更聰明地判斷哪些 partitions 真正需要被處理。

**把大規模操作改成穩定可控的節奏**。Orphan file deletion 計畫改用 dry run mode 收集要刪的 files 清單，放進 buffer 或 queue，以穩定可控的速率送進 AWS delete API；同時也參考 Salesforce 的做法，直接比對 S3 listing 與 Iceberg metadata 找出 orphan files，繞過內建 `remove_orphan_files` 的限制。Compaction 也不再每次都把整張 table 重壓一次，改成只壓最近 N 天（投影片提到 7 天）的資料；streaming tables 的 SLA 也會拉到每小時一次，讓單次處理量更可控。

往更長遠看，Slack 還規劃了兩個方向：

- **從觀察者轉成貢獻者**：把累積的調參優化經驗反饋回 Apache Iceberg 社群，從目前的 lurker 角色轉成 active contributor。
- **AI 介入維護決策**：探索用 AI 自動 tune compaction 的執行頻率與參數，讓系統更聰明地適應每張 table 的特性。

Talk 結尾，Lawrence 對這套系統的未來做了一句直白的總結

> I'm very confident in our future.

他的信心來自一個有趣的內部驗證：Salesforce 旗下另一個技術棧、規模、tables 數量都與 Slack 高度相似，但採用 Iceberg 早了兩年的團隊，獨立開發出了與 IceChipper 幾乎一模一樣的系統，目前已經穩定運作在 Slack **10 倍**的資料規模上。對 Lawrence 來說，這既是 IceChipper 設計被獨立驗證的訊號，也代表系統還有相當大的擴展空間。
