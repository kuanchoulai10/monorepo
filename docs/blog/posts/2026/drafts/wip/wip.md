---
draft: true
authors:
  - kuanchoulai10
date:
  created: 2026-05-30
  updated: 2026-05-30
categories:
  - Data
links:
  - "What Breaks at Trillion Rows: Eliminating Iceberg Bottlenecks in Firebolt | 2026 Iceberg Summit": https://youtu.be/anebAxlJhGI?si=hCA_yiSHB7_6_7Yp
  - "Big Metadata: When Metadata is Big Data (VLDB 2021)": https://vldb.org/pvldb/vol14/p3083-edara.pdf
  - "BigQuery under the hood: The power of the Column Metadata index aka CMETA | Google Cloud Blog": https://cloud.google.com/blog/products/data-analytics/understanding-the-bigquery--column-metadata-cmeta-index/
  - "Metadata indexing for BigQuery tables | Google Cloud Documentation": https://docs.cloud.google.com/bigquery/docs/metadata-indexing-managed-tables
  - "The DuckLake Manifesto: SQL as a Lakehouse Format": https://ducklake.select/manifesto/
tags:
  -   
comments: true
---


# WIP: Metadata as Data — Trillion-row Iceberg 的思路收斂


<!-- more -->


研究素材分成三塊：Firebolt 在 2026 Iceberg Summit 的演講、Google 從 2021 VLDB 論文到 2025 產品化的 CMETA、以及 DuckLake Manifesto。三者共同指向同一個方向：**當資料規模大到一定程度，metadata 處理本身就會變成大數據問題，必須把 metadata 也當成資料來分散式處理。**

---

## 1. Firebolt × Iceberg @ Trillion Rows

**來源**：[What Breaks at Trillion Rows: Eliminating Iceberg Bottlenecks in Firebolt | May 21, 2026 | 2026 Iceberg Summit](https://youtu.be/anebAxlJhGI?si=hCA_yiSHB7_6_7Yp)

這場演講主要討論 Firebolt（一家專注於低延遲與高並發的分析型資料庫新創公司）如何解決 **Apache Iceberg 在處理「兆級行數」（Trillion-row）超大型資料表時所面臨的元數據（Metadata）效能瓶頸**。

### 1.1 規模背景與核心策略

- **超大規模挑戰**：講者以一家大型零售商的點擊流資料為例，該表包含約 **40 兆行數據**、總量達 **20PB**，且擁有超過 **400 萬個檔案**，在這種規模下，元數據本身也變得巨大且難以處理。
- **元數據即數據（Metadata as Data）**：Firebolt 的核心策略是將元數據視為普通數據，利用分散式 **SQL 引擎來處理元數據的查詢、過濾（Pruning）與節點分配**，取代傳統的手動處理方式。
- **優化查詢延遲**：為了達成毫秒級的延遲，Firebolt 解決了雲端儲存（如 S3）讀取元數據過慢（通常需 0.5 秒以上）的問題。他們透過**緩存機制**與獨有的**「子結果緩存」（Sub-result caching）**，讓跨查詢間的統計數據與元數據能被重複使用，大幅提升速度。
- **應對超寬表（High Column Count）**：針對擁有數萬個欄位的資料表，Firebolt 開發了**自定義的序列化工具**，用於快速跳過不需要的 Parquet 檔案註腳（Footer）內容，從而縮短解析時間。

### 1.2 五大技術瓶頸（Problem Statements）

當資料規模達到**兆級行數（Trillion Rows）**時，Apache Iceberg 面臨的核心問題在於**「元數據（Metadata）本身也變成了大數據」**，導致傳統的處理方式崩潰。具體瓶頸如下：

#### (1) 元數據規模過大導致處理緩慢（Metadata Scale）

在兆級規模下（如來源提到的 40 兆行、20PB 資料），檔案數量可能高達 **400 萬個**。當檔案數量如此龐大時，傳統的元數據處理方式（如列出檔案、過濾不必要的資料片段等）會變得極其挑戰，單機或簡單的過濾邏輯已無法在短時間內完成查詢規劃。

#### (2) 雲端儲存的延遲瓶頸（Cloud Storage Latency）

在毫秒級查詢的需求下，雲端儲存（如 AWS S3）的存取延遲是一大硬傷：

- **讀取路徑過長**：典型的 Iceberg 查詢需要依序讀取元數據檔案、清單檔案（Manifest files）以及 Parquet 檔案的腳註（Footer）。
- **累積延遲**：即使在理想狀況下，單次讀取 S3 的延遲約 100-200 毫秒。這意味著完成所有元數據讀取可能就需要耗費 **0.5 秒以上**，這對要求「毫秒級」回應的系統來說太慢了。

#### (3) 「超寬表」造成的解析負擔（High Column Count / Ultra-wide Tables）

當資料表擁有**數千甚至上萬個欄位**時，Parquet 檔案的腳註（Footer）會變得非常龐大：

- **序列化效能**：標準的串流反序列化工具（Stream deserializer）在解析包含 10,000 個欄位定義的架構（Schema）時，會耗費大量時間，甚至比實際讀取資料還要久。
- **無效讀取**：即使查詢只需要其中 5 個欄位，傳統方式仍可能需要掃描整個龐大的元數據架構資訊。

#### (4) 資源分配與調度挑戰（Node Allocation & Planning）

如何將 **400 萬個檔案**優化地分配給叢集中的節點（Node）是一個難題：

- 需要決定哪些檔案該由哪個節點處理，以達到最佳的並行度與資料局部性。
- 如果分配邏輯不夠快，查詢規劃的時間就會拖累整體的執行效率。

#### (5) 數據估算的準確性與代價（Cardinality Estimates）

在如此巨大的資料量下，傳統的基數估算（Cardinality estimates）往往不夠準確：

- 精確的統計數據（如直方圖、唯一值數量等）雖然有利於優化查詢計畫（如 Join 排序），但在兆級規模下計算這些統計數據本身可能就非常昂貴且耗時。

### 1.3 六項解法（Solutions）

針對上述瓶頸，Firebolt 提出的核心解法與具體做法：

#### (1) 將「元數據視為數據」（Metadata as Data）

Firebolt 的核心理念是將龐大的元數據當作普通數據來處理，利用其分散式 SQL 引擎來進行運算，而不是手動處理。

- **做法**：開發**表值函數（Table Valued Function, TVF）**來發現與列出檔案，並透過 **Lateral Join** 讓 SQL 流水線能並行且重疊地讀取檔案與處理數據。
- **優點**：能夠利用現有的分散式引擎進行大規模並行處理，解決單機無法負荷數百萬個檔案元數據的問題。

#### (2) 使用 SQL 進行高效剪枝（Pruning）

為了從數百萬個檔案中精確找出所需的資料，Firebolt 將剪枝邏輯表達為 SQL 查詢。

- **做法**：利用 SQL 語法對 Manifest 檔案中的統計資訊（如 Min/Max、Bloom Filter）進行過濾。例如，透過比較查詢條件與檔案統計值來剔除不必要的檔案。
- **優點**：整個過程是流式（Streaming）且並行的，能大幅縮短查詢規劃（Planning）的時間。

#### (3) 利用窗口函數優化節點分配（Node Allocation）

當有數百萬個檔案需要分配給叢集節點執行時，如何達成負載平衡是一大挑戰。

- **做法**：Firebolt 內建了多種**窗口函數（Window Functions）**，根據檔案大小、分區屬性等特徵，動態計算並決定每個檔案應該路由到哪個節點處理。
- **優點**：確保資源分配的靈活性與執行效率。

#### (4) 解決雲端儲存延遲的緩存機制（Caching）

S3 等雲端儲存的讀取延遲（通常 >100ms）會導致查詢無法達到毫秒級回應。

- **緩存管理器（Buffer Manager）**：將元數據、Manifest 檔案以及 Parquet 檔案的腳註（Footer）緩存於記憶體中，減少與 S3 的往返次數。
- **子結果緩存（Sub-result caching）**：這是 Firebolt 的獨特功能，它不僅緩存最終結果，還能**緩存查詢過程中的中間統計數據（如 Join 規劃所需的基數估算）**。這些緩存可以跨查詢共享，讓後續查詢甚至不需要重新讀取元數據。

#### (5) 針對超寬表的自定義序列化（Custom Serializer）

傳統序列化工具在解析包含數萬個欄位的 Parquet 腳註時非常緩慢。

- **做法**：Firebolt 編寫了**完全自定義的序列化工具**，它具備「跳躍式」搜尋能力，能直接定位到所需的 5 到 10 個欄位，而跳過其餘上萬個不相關的欄位資訊。
- **優點**：解決了「超寬表」在元數據解析上的效能瓶頸。

#### (6) 精確的查詢規劃（Accurate Planning）

在兆級規模下，僅靠估算是不夠的。

- **做法**：直接從 Iceberg 的 Manifest 檔案中加總實際的行數與統計值，而非使用模糊的估計。
- **優點**：能為 Join 等複雜操作提供最優化的執行計畫。

### 1.4 一句話總結

當資料達到兆級規模時，**「元數據處理」取代了「資料掃描」成為效能的主要障礙**，必須將元數據當作普通的數據進行分散式處理與快取優化才能解決。這場演講分享了如何透過將元數據處理「數據化」與「緩存化」，讓 Iceberg 資料表在極大規模下仍能保持極高性能。

---

## 2. BigQuery CMETA 的三個時間點

**來源**：

- 論文：[Big Metadata: When Metadata is Big Data (VLDB 2021)](https://vldb.org/pvldb/vol14/p3083-edara.pdf)
- 官方部落格：[BigQuery under the hood: The power of the Column Metadata index aka CMETA (2025)](https://cloud.google.com/blog/products/data-analytics/understanding-the-bigquery--column-metadata-cmeta-index/)

BigQuery 的 **CMETA**，也就是 **Column Metadata index**，至少可以分成三個時間點來看。

### 2.1 三個時間點

**第一，作為 BigQuery 內部技術，2021 年以前就已經存在。**

Google 在 2021 年 VLDB 論文《Big Metadata: When Metadata is Big Data》中說，BigQuery 已經建了一套 metadata management system，用來以分散式方式管理細粒度的 column/block-level metadata，並把 metadata 組織成 system table 來服務查詢規劃與 pruning。這表示它不是 2021 才開始做，而是到 2021 年公開發表時，系統已經在 BigQuery 內部成形並被用來支援大規模查詢。

**第二，作為公開研究成果，CMETA 是 2021 年正式出現在論文中的。**

Google Research 的頁面把這篇論文列為 **VLDB 2021**，Google Cloud 2025 年的官方文章也明確說「In 2021, we presented the Column Metadata, CMETA, index in a 2021 VLDB paper」。所以如果你問「這個技術最早什麼時候被公開提出」，答案就是 **2021 年**。([Google Research][1]) ([Google Cloud][2])

**第三，作為 BigQuery 使用者可觀察、可查詢的產品能力，公開文件是在 2025 年左右變得明確。**

Google Cloud 在 2025 年 9 月發表文章介紹「BigQuery under the hood: The power of the Column Metadata index aka CMETA」，並說 BigQuery 現在會自動建立與管理 CMETA system table，使用者不需要手動維護。BigQuery 文件也有「Metadata indexing for BigQuery tables」頁面，說 BigQuery 會自動為超過 1 GiB 的 BigQuery table 建立 metadata index，並且可以透過 `LAST_METADATA_INDEX_REFRESH_TIME`、`metadata_cache_statistics` 等欄位觀察使用狀況。([Google Cloud][2]) ([Google Cloud Documentation][3])

### 2.2 結論

**CMETA 不是 2025 年才出現的技術。它最晚在 2021 年已經作為 BigQuery 內部技術被公開發表；但 Google Cloud 到 2025 年才用比較產品化、使用者可理解的方式，把「Column Metadata index, CMETA」這個能力正式寫進部落格與文件中。**

### 2.3 可在文章中引用的段落

> BigQuery 的 CMETA, Column Metadata index, 並不是最近才發明的功能。Google 早在 2021 年 VLDB 論文《Big Metadata: When Metadata is Big Data》中就公開描述了這套 metadata management design。它的核心想法是把細粒度的 block-level 與 column-level metadata 當成 BigQuery 自己也可以分散式處理的資料來管理，而不是只把 metadata 放在集中式 catalog 或個別資料檔案 footer 裡。到了 2025 年，Google Cloud 才更明確地以產品文件與官方文章介紹 CMETA，說明 BigQuery 會自動維護 column metadata index，並用它協助 query planner 做更細粒度的 pruning。

[1]: https://research.google/pubs/big-metadata-when-metadata-is-big-data/ "Big Metadata: When Metadata is Big Data"
[2]: https://cloud.google.com/blog/products/data-analytics/understanding-the-bigquery--column-metadata-cmeta-index/ "Understanding the BigQuery column metadata (CMETA) index | Google Cloud Blog"
[3]: https://docs.cloud.google.com/bigquery/docs/metadata-indexing-managed-tables "Metadata indexing for BigQuery tables | Google Cloud Documentation"

---

## 3. DuckLake Manifesto: SQL as a Lakehouse Format

**來源**：[The DuckLake Manifesto: SQL as a Lakehouse Format](https://ducklake.select/manifesto/)

### 3.1 DuckLake 的核心論點

DuckLake 在舉 BigQuery 的例子時，主要是在驗證它自己的核心想法：

> 既然 lakehouse 最後已經需要一個 database/catalog 來保證 transaction consistency，那就不應該只讓 database 管「目前 table version pointer」這種很小的 metadata，而應該把更多 table metadata 都放進 database 裡管理。

### 3.2 推論脈絡

DuckLake manifesto 的脈絡是這樣：

Iceberg / Delta 一開始的設計理念是：不要依賴 database，把 metadata 也放在 object storage 上，用 JSON、Avro、manifest、manifest list 等檔案來描述 table state。這樣可以維持 data lake 的開放性，但問題是後來大家還是需要 transaction、multi-table management、atomic pointer update，所以又加了一層 catalog service，catalog 背後通常還是接 database。DuckLake 認為，這代表原本的設計前提已經改變了。既然 database 已經進入 lakehouse stack，那就應該重新思考：為什麼不直接用 database 管理 metadata？

把 metadata 放進一個真正的資料管理系統，不是 DuckLake 憑空發明的想法，而是大規模 analytical system 已經驗證過的架構方向。DuckLake 原文說，metadata 可以交給 SQL database 管，而 data files 仍然放在 blob storage，用 Parquet 這種開放格式。它接著說，這其實也類似 BigQuery 和 Snowflake 的選擇，只是 BigQuery / Snowflake 底層沒有採用開放 table format 或開放 data file format 作為核心設計。

### 3.3 一句話總結

BigQuery 已經證明，把 metadata 管理變成 database/data management problem，是可以 scale 的，而且可以很快。DuckLake 想把這個方向用開放格式重新包裝：data 還是 Parquet，metadata 則是一組 SQL tables。
