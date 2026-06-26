---
authors:
  - kuanchoulai10
date:
  created: 2026-06-06
  updated: 2026-06-26
categories:
  - Data
links:
  - blog/posts/2026/01-06/rethinking-iceberg-metadata-v4/rethinking-iceberg-metadata-v4.md
  - blog/posts/2026/01-06/iceberg-efficient-column-update-and-column-families/iceberg-efficient-column-update-and-column-families.md
  - blog/posts/2026/01-06/lessons-from-slack-iceberg/lessons-from-slack-iceberg.md
  - "Iceberg with ClickHouse: A One-Year Development Retrospective": https://youtu.be/s_eZph1loeA?si=8esDigQ6DGV82rIY
  - "What Breaks at Trillion Rows: Eliminating Iceberg Bottlenecks in Firebolt": https://youtu.be/anebAxlJhGI?si=A5s_0u5iy4O_OTOG
  - "High-Performance Full Text Search Directly on Iceberg via Lucene-Integrated Indexing": https://youtu.be/KO04A2uEa0E?si=Q7DkM3q6P1UGkPnC
tags:
  - Apache Iceberg
  - The Lakehouse Series
comments: true
---


# 從三家 OLAP 產品反推 Iceberg 的設計挑戰

!!! info "After reading this article, you will be able to answer..."

    - ClickHouse、Firebolt、StarTree 在整合 Iceberg 時，為什麼不約而同做了類似的選擇？
    - 這些選擇背後反映的是 Iceberg spec 的哪些結構性不足？
    - Iceberg community 正在怎麼補上這些不足？

<!-- more -->

Iceberg 已經是現在 open table format 的事實標準。從 Snowflake、Databricks、AWS 到 BigQuery，幾乎所有主流分析平台都把 Iceberg 列為支援對象；社群裡的 spec 討論、提案與各種整合工作也維持著高頻率產出。

但實際把 Iceberg 整合進產品時，能不能直接使用標準實作、又能讓查詢延遲降到 sub-second，是另一回事。最近三場 talks 從不同角度，記錄了三家以低延遲查詢為核心的 OLAP 產品在做這件事情時遇到的挑戰：

- [Iceberg with ClickHouse: A One-Year Development Retrospective](https://youtu.be/s_eZph1loeA)，由 ClickHouse 的 Director of Product Malvyn Peignon 主講，回顧他們投入 Iceberg 整合一年半的經驗
- [What Breaks at Trillion Rows: Eliminating Iceberg Bottlenecks in Firebolt](https://youtu.be/anebAxlJhGI)，由 Firebolt CTO Mosha Pasumansky 主講，討論 trillion-row 規模下他們遇到的瓶頸
- [High-Performance Full Text Search Directly on Iceberg via Lucene-Integrated Indexing](https://youtu.be/KO04A2uEa0E)，由 StarTree.ai 的 Xiang Fu 與 Raghav Yadav 共同主講，討論在 Iceberg 之上直接支援 full-text search。

三家公司的價值主張一致，都是在 Iceberg 上做到 sub-second 查詢，投入的工程資源也高度重疊：都在同樣幾個層面自行研發 Reader、加 cache、把單機 metadata planning 改成分散式 metadata planning。

這篇文章的目的，是把這三場 talks 放在一起仔細研究。先看三家公司各自要解的問題，再萃取它們在相同價值主張下投入的共同 patterns，最後從這些 patterns 反推 Iceberg 目前還沒解決的設計不足。

## 三場 Talks 指向同一組挑戰

三家公司都以 sub-second query latency 作為核心價值主張，也都把 Iceberg 列為近期的重點整合對象。產品形態雖然不同，但面對的工程挑戰高度一致：

- [**ClickHouse**](https://clickhouse.com/) 是 open-source columnar OLAP database，以 low query latency和 high throughput寫入著稱，常被用在 observability、event analytics 等 append-heavy 場景。原本以自家儲存格式為主，最近一年半開始正式投入 Iceberg 整合。
- [**Firebolt**](https://www.firebolt.io/) 是面向工程團隊的 cloud-native analytical database（Postgres 相容），主打 sub-second query、high concurrency、price-performance，常用來支撐 customer-facing analytics 與 data application backend。它把 Iceberg 應用在 trillion-row 規模與上萬欄位的 wide table 場景。
- [**StarTree.ai**](https://startree.ai/) 是 Apache Pinot 的商業化平台，主打 streaming data 上的 sub-second 與高並發 user-facing analytics。它把 Iceberg 與 full-text search 結合在一起，讓使用者不必再額外維護一套 Elasticsearch。

價值主張相同，面對的底層限制自然也相同。在 Iceberg 與底層 Parquet 的設計下，三家都在同樣幾個層面遇到相同的限制。

## 三場 Talks 各自在解什麼問題

把三家公司各自的整體取捨先看清楚，後面要歸納共同 patterns 時才不會把不同的問題混在一起。三場 talks 雖然都圍繞「在 Iceberg 上做到 sub-second 查詢」這件事，但各自聚焦的具體問題不同。

### ClickHouse：在 Iceberg 上做到 sub-second 查詢延遲

ClickHouse 原本以自家 columnar 儲存格式提供 sub-second 查詢延遲。要把它整合到 Iceberg 上，問題在於 Iceberg 的標準讀取路徑（從 metadata files、manifest list 到 data files）原本是為 batch 分析設計的，每一層都依賴對 cloud object storage 的請求。標準路徑下的延遲，遠遠超過 sub-second 能容忍的範圍。

所以 ClickHouse 過去一年半的整體取捨是：**所有原本由通用程式庫承擔的 I/O 與 metadata 邏輯，都改由 ClickHouse 自己實作**。用 C++ 重新實作 Iceberg spec、為 Parquet 寫原生 Reader、為 metadata 與 footer 各自設計 cache 層。這些工作都把「整合 Iceberg 後仍要 sub-second」當作不可妥協的設計前提。

### Firebolt：在 trillion-row 規模下，metadata 本身已經是需要被處理的大數據

Firebolt 面對的問題在另一側。它的客戶常用 Firebolt 在 trillion-row 規模、20PB 量、上萬欄位的 wide table 上做 sub-second 查詢。在這種規模下，Iceberg metadata 自己也會變得非常龐大：一張 table 可能對應數百萬個 data files、數萬份 manifest，連單純列出檔案這件事都足以讓 query planning 顯著變慢。

所以 Firebolt 的整體取捨是：**直接把 metadata 視為另一種大數據來處理**。它不再讓單一節點循序掃描 manifest，而是把 metadata 建模成一張 SQL table，用 Firebolt 自己的 query engine 去掃。同時針對 wide table 的 Parquet footer 那種「上萬欄位、上百 MB」的情況自寫 serializer，只解析查詢真正用到的欄位。

### StarTree：在不搬離 Iceberg 的前提下，把 full-text search 做到 sub-second 級

StarTree 的問題定義跟前面兩家不太一樣。它的客戶要在同一份資料上同時做傳統的 OLAP 聚合與 full-text search（fuzzy search、phrase query 等）。過去的做法是把資料同時寫進一個 OLAP 系統與一個 Elasticsearch，由應用層自己 join。這意味著兩套系統的維運、資料同步、一致性處理都要自己負責。

所以 StarTree 的整體取捨是：**在不搬離 Iceberg 的前提下，把 full-text search 能力放回 Pinot 的查詢路徑裡**。具體做法是用一個 Watcher 任務監控 Iceberg table 的檔案目錄，每當新的 Parquet 檔案出現就建立一個輕量的 pseudo segment（只記錄檔案 URL），同時 in-line 為這個檔案產生 Lucene index，允許使用者把 index pin 在本地。查詢端就能用 Lucene index 先找出符合條件的記錄，再從 Iceberg 讀取對應的 page。

## 相同價值主張下的共同 Patterns

三家公司聚焦的具體問題不同，但實際做出的工程動作在同樣三個層面高度重疊。下面依序拆開來看每一個層面，以及每一家在這個層面上做了什麼。

### Pattern 1：S3 的 metadata 讀取延遲，三家都另加一層 cache 改善

第一個重疊層面是 metadata 讀取。Iceberg 的標準讀取路徑是 sequential 三層（metadata files → manifest list → manifest files），每一層都對 cloud object storage 發請求。S3 對單一物件的存取延遲通常在 100-200ms 之間，三層串連起來，光是 query planning 就要花幾百毫秒，sub-second 完全做不到。

- **ClickHouse**：把 Iceberg metadata 解析後留在記憶體 cache，並用 background thread 定期（例如每 30 秒）非同步更新。到時候查詢時 metadata 已在記憶體裡。
- **Firebolt**：以 max-staleness 為單位 cache 整套 metadata，另外引入 sub-result caching 跨查詢復用中間結果（例如 pruning 後的 file list），讓相似查詢直接跳過 metadata scan。
- **StarTree**：實作 data cache 與 index cache，並允許使用者把 index pin 在本地（記憶體或磁碟），讓 Lucene index 與相關 metadata 都不必重新讀 S3。

三家做法的細節不同，但本質都是把 Iceberg metadata 從「跟 S3 同步、每次查詢都重新讀」改成「在本地 cache、按 freshness 規則更新」。Iceberg spec並沒有規定 metadata 應該怎麼被讀取或 cache，這層是三家在自家系統裡自己補上的。

### Pattern 2：標準 Parquet Reader 效能不足，三家都自行研發 Reader

第二個重疊層面在 Parquet 的讀取層。Iceberg 的 data files 是 Parquet 格式，多數 query engine 早期依賴 Apache Arrow 或其他通用 Parquet 函式庫來讀取。但這些通用函式庫的粒度停在 file 或 row group level，缺少 page level 的 I/O 控制；序列化路徑要把資料從 Parquet 經 Arrow 再轉成系統自己的格式，每一道轉換都會疊加延遲。對追求 sub-second 的 OLAP 產品而言，這條路徑無法滿足。

- **ClickHouse**：用 C++ 重新實作 Parquet Reader，完全去除對 Arrow 的依賴。新 Reader 更有效利用 Bloom Filter 與檔案統計做 skipping，並把任務粒度細化到 row group level，讓多個 replica 共同分擔讀取。
- **Firebolt**：針對 wide table（成千上萬個 column）寫自定義的 Parquet serializer。標準 Reader 必須先解析整份 footer 才能定位欄位，這在 wide table 場景動輒上百 MB；Firebolt 的 Reader 能直接跳過不需要的欄位 metadata，只解析查詢真正用到的 column。
- **StarTree**：自寫 Parquet Reader 取得 page level 的 I/O 控制，能把 predicate 下推到 page level、只讀必要的 page，並與 Pinot 自己的非同步 prefetch / pipelining 機制深度整合。

三家寫出來的 Parquet Reader 細節不一樣，但都對「通用函式庫不夠用」這件事達成了共識。Arrow 的中介轉換、缺少 page level 控制、wide table 場景下的 footer 開銷，這三件事讓三家都選擇自行實作 Reader。

### Pattern 3：單機 metadata planning 在大規模下成為瓶頸，三家都把 planning 分散化

第三個重疊層面是 metadata planning 本身的 scaling。Iceberg spec描述了 metadata 的 layout，但沒有規定 query engine 該如何分配 planning 工作。多數實作的預設是「由一個 coordinator 節點讀完所有 metadata，再分發實際的 data read」。當 metadata 規模從幾百份 manifest 變成數萬份、數百萬個 data files，這個 coordinator 就變成 single point of bottleneck。

- **ClickHouse**：已意識到單一 coordinator 是瓶頸，目前正在開發把 metadata 讀取分散到多個 replica 的方案。同時把 data 讀取的任務粒度細化到 row group level，避免某個巨大的 file 讓單一 replica 成為瓶頸。
- **Firebolt**：呼應 Google 在 2021 年論文中提出的「metadata as data」概念。在自家系統中，manifest 不再被當成「需要循序掃描的小檔案」，而是建模成 SQL table，用 Firebolt 既有的分散式 SQL 機制去 scan、prune、distribute。整套 metadata planning 變成一個分散式 SQL job。
- **StarTree**：把每個 Parquet 檔案抽象成輕量的 pseudo segment（只記 URL 與 metadata），於是 Pinot 原本針對 segment 設計的 Broker/Server 兩層 pruning 架構可以直接套用：Broker 在分發查詢前先剔除不符合的 segment，接著 Server 再做 file 內部的 predicate 過濾。整套 planning 自然就分散到 Broker 與 Server 上。

三家用了不同做法，但都是解決同樣的問題：把原本集中在一個 coordinator 上的 metadata planning 拆解到多個節點上。Iceberg spec 本身對這件事沒有規定，三家都用自家既有的分散式機制各自重新設計了一套，以滿足它們自家產品的價值主張：sub-second query latency。

## 這些 Patterns 反推出的 Iceberg 設計不足

如果只是一家公司在某個層面上投入額外工程，那可以解釋為他們的場景特殊。但同一個層面上同時有三家公司、用三種不同抽象解決同一個問題，比較像是 Iceberg spec本身在這幾個層面做得不夠。下面把這幾個不足整理出來，並區分：哪些是 Iceberg / Parquet 本身的設計限制、哪些其實是整合方面對自家場景的特殊需求。

### Sequential metadata 路徑與雲端儲存延遲不相容

第一個不足直接源自 Pattern 1。Iceberg 的 metadata 結構在設計時假設 metadata 讀取相對廉價：依序讀 metadata.json、manifest list 與 manifest files 三層 sequential 路徑，在本地或低延遲儲存上沒有問題。但 cloud object storage 對單一物件的存取延遲落在 100-200ms 之間，光是讀取這三層檔案本身就要花掉幾百毫秒。

而且這幾百毫秒只是「拿到 bytes」的成本。把這些 bytes 解析成 Avro / JSON 結構、抽出 data file list 與相關 statistics、提供給 query planner 做 pruning，這些工作都還沒開始。當整體時間預算只有 sub-second 時，這個假設就無法成立。

這個問題不會因為換家公司就消失。任何想在 cloud object storage 上做低延遲查詢的產品都會面對相同的瓶頸。因此這算是 Iceberg metadata layout 在 cloud-native 場景下的設計限制，屬於 spec 層面的不足。

### 讀 Parquet 仍需大量優化，但 Iceberg spec 沒提供標準路徑

第二個不足涵蓋 Pattern 2 與 Pattern 3 共同呈現的事實：**讀完 metadata 之後，真正去讀 Parquet 這件事還需要大量優化**，三家公司都得從頭實作一遍 Reader 才能達到 sub-second 目標。

仔細了解，讀 Parquet 的效能瓶頸會散落在好幾個面向：

- footer 整份解析的成本不容忽視，標準 Reader 沒提供跳過不必要部分的方式
- page level 的 I/O 控制不在 Parquet 標準 API 裡，無法只讀必要的 page、無法做 pipelining 與非同步 prefetch
- file 內部 row group 級的任務切分不在 Iceberg spec 裡，一個巨大的 file 容易讓單一節點成為瓶頸
- 通用中介層（例如 Arrow）為了適配多種 query engine 而付出的格式轉換成本，在 sub-second 場景下會被放大

Iceberg 對 file 層級的 read pattern 給出了完整 spec （manifest 列出 files、column stats 落在 file 或 row group level、partition pruning 與 column projection 都有對應規則），但 file 之內如何被讀取，幾乎沒有任何規定。這個範圍可以理解為 spec 刻意留白，也可以理解為不足。我傾向把它視為不足：cloud-native + sub-second 已經是查詢場景的主流，每家公司都各自重新設計一套 sub-file 讀取模型，對 Iceberg 生態而言這個工程成本相當顯著。

### Iceberg 透過 Puffin 為 index 留了空間，但離 first-class 還有距離

第三個不足的證據主要來自 StarTree 在 Pattern 1 與 Pattern 2 中所有 index 相關的努力：把 Lucene index pin 在本地、用 Watcher 任務同步 index、自行研發 Reader 整合 index 查詢。

要說 Iceberg 完全沒有 index 概念並不公平。Iceberg 透過 **Puffin file** 這個 sidecar 容器，為 statistics 與 index 類資料留了空間。Puffin 目前 spec 上明確支援的 blob type 包含 Theta sketch（用來估 NDV）與 deletion vector，並透過 metadata.json 的 `statistics` 欄位連結到對應的 snapshot。

但 Puffin 的角色還在很早的階段。它在 spec 上是 optional 的，reader 可以選擇忽略，這意味著不同 query engine 對 Puffin 的支援程度落差很大。spec 明確列出的 blob type 也只有兩種， full-text search、向量檢索、inverted index 這類其他類型的 index 沒有對應的標準化容器。想做 Lucene 之類的 index 時，整合方仍然得回到 StarTree 那套自己做的路徑：自己管理 index file、自己處理同步、自己定義跨 catalog 跨 query engine 的讀取協定。

所以這個不足準確的描述是：Iceberg 已經透過 Puffin 為 index 留了空間，但這個空間還不夠 first-class、覆蓋範圍也還窄。下一個整合方做 Iceberg 上不在 Puffin spec 內的 index 時，仍然要從頭設計一輪。

## Future Plans

面對先天上的不足，Iceberg community 也正積極著手這些面向。在 metadata 路徑這個面向上，Iceberg v4 已經在重新設計整套 metadata layout，把原本 sequential 的三層讀取改成 adaptive tree，讓 metadata 結構本身可以隨 table 體量伸縮。這個方向我之前在 [Iceberg v4 的 metadata 重新設計](../rethinking-iceberg-metadata-v4/rethinking-iceberg-metadata-v4.md) 那篇寫過，這裡不再贅述。同一個面向上，[Understanding Column Statistics in v4](https://www.youtube.com/watch?v=U5yvmq7S8Js) 進一步討論 column statistics 在新結構下要怎麼分層、什麼時候放進 Puffin、什麼時候做 on-demand 載入。整體上，這個面向的轉變是：正視 metadata 本身就是 big data，用同樣分散式、按需處理的思路來管理。

在 Parquet 讀取這個面向上，community 同時在兩個方向上進行。一個方向是改進 Parquet 自身，例如 [The Decompression Bottleneck: Evolving Parquet with PFOR and ALP](https://www.youtube.com/watch?v=OiowtisBGIw) 提到的新編碼與解壓縮路徑，目標是用更少 CPU cycles 完成讀取；另一個方向是讓 Iceberg 能用 Parquet 以外的 file format，例如 [Vortex 這個被設計為 Parquet 後繼者的格式](https://youtu.be/5x4ppDPuliE)，原生支援 SIMD filtering、GPU decompression、AI workload 場景。能讓這兩個方向並存的關鍵基礎，是 Iceberg 1.11.0（2026 年 5 月）finalize 的 [File Format API](https://iceberg.apache.org/blog/apache-iceberg-file-format-api/)：透過 pluggable 介面把 file format 抽象出來，Iceberg 不再 hard-code Parquet。這個改動在 spec 層級把「file format 是什麼」變成了一個可替換的維度，整合方可以針對自家 workload 選擇最合適的格式。

在 index 這個面向上，[secondary index framework](https://youtu.be/vB63kyYm4ks) 已經有正式提案，並有初步 PoC 的結果（point lookup 把讀取的 file 數從 50 降到 1、equality delete 場景達到約 5x 的速度差距）；[vector / ANN index](https://youtu.be/kwjNer5q0bg) 的底層算法由 Microsoft 開源的 DiskANN 提供，目前在補上 Iceberg 端的 Reader / Writer 與 index 生命週期管理。整體目標是把 index 升級成 Iceberg 的 first-class concept，讓 Iceberg 之上的 full-text search、向量、secondary index 查詢都能像 partition pruning 一樣由 spec 統一定義。

把這三個面向放在一起看，未來的 Iceberg 會同時是 sub-second 查詢、cloud-native infrastructure、AI 與搜尋的共用 lakehouse 基礎。對這個方向我非常看好，也很期待 lakehouse 的能力最終能延伸到什麼形態。對這幾個面向有興趣的讀者，上面這幾個 references 是很好的下一站。
