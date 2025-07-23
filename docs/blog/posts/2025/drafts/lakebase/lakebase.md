---
draft: true
authors:
  - kuanchoulai10
date:
  created: 2025-07-29
  updated: 2025-07-29
categories:
  - Data
links:
  - Data Mesh Principles and Logical Architecture: https://martinfowler.com/articles/data-mesh-principles.html
  - What Is a Lakebase? | Databricks Blog: https://www.databricks.com/blog/what-is-a-lakebase
  - Announcing Lakebase Public Preview | Databricks Blog: https://www.databricks.com/blog/announcing-lakebase-public-preview
  - Lakebase Product Page | Databricks: https://www.databricks.com/product/lakebase
  - Sync data from Unity Catalog tables to a database instance | Databricks Docs: https://docs.databricks.com/aws/en/oltp/sync-data/sync-table
tags:
  - Lakebase
  
comments: true
---


# Lakebase: Redefining the Line Between Databases and Lakehouses


<!-- more -->


Zhamak Dehghani once said in her 2020's article, [*"Data Mesh Principles and Logical Architecture"*](https://martinfowler.com/articles/data-mesh-principles.html):

> *I do believe that at some point in the future our technologies will evolve to bring these two planes even closer together, but for now, I suggest we keep their concerns separate.*

This quote perfectly captures the essence of the current state of data management technologies. While databases and lakehouses serve distinct purposes, the emergence of Lakebase blurs the lines between them.


<iframe width="560" height="315" src="https://www.youtube.com/embed/waGy8eYJvMg?si=2hB0g_ipRv14hXCr" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


What Is a Lakebase?

- Openness
- Separation of storage and compute
- Serverless
- Modern development workflow: branching
- Built for AI agents
- Lakehouse integration

































<iframe width="560" height="315" src="https://www.youtube.com/embed/SRLk_edBB9o?si=4P0NMVT5DYir-aWU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


## neon的架構，儲存在blob storage的檔案，是什麼樣的格式？
Neon 的儲存架構採用「分離式計算與儲存」（compute‑storage separation）設計，用雲端 blob storage（例如 S3 或 Azure Blob Storage）來存放資料。具體來說：

---

### 📦 Blob Storage 中的檔案格式與內容

- **兩種主要「layer」檔案**：

  1. **Image layer**：儲存已物化的完整 Postgres data page（每頁 8 KB），方便直接讀取。
  2. **Delta layer**：儲存 WAL (Write-Ahead Log) 差異，只記錄變更內容，用來增量重建頁面。([Neon][1], [Database of Databases][2])

- **索引結構**：這些層檔案都使用 on-disk B+ tree 結構索引，方便在 blob 中快速定位頁面或 WAL 區段。([Database of Databases][2])

- **不可變、Log‑structured 設計**：

  - Layer 檔案一旦寫入即不再修改。
  - 隨著時間推移，Pageserver 會進行 compaction 將多個 layer 合併，降低 fragmentation 並提升 storage 及 IO 效率。([Database of Databases][2])

- **存取流程**：

  1. Postgres compute 將 WAL 傳送到 Safekeeper（採用 Paxos 協議確保可靠性）。
  2. Pageserver 從 Safekeeper 拉取 WAL，轉換成 delta layer，再生成 image layer，並同步這些 layer 到 blob storage。([Neon][3])
  3. 當 compute 要讀取某頁面時，Pageserver 根據 layer map 判斷應當重放哪些 delta，再找到對應的 image layer，快速組合出當前頁面狀態。([Database of Databases][2])

---

### 為什麼用這種方式？

- **支援快照、時間點查詢、branching**：因為 storage 中保留歷史 layer，所以可以在指定的 LSN（log-sequence number）或日期重現資料狀態，用來實作分支或時光點還原。([Database of Databases][2])

- **高效且可靠**：

  - blob storage（例如 S3/Azure Blob）提供高 durability 和 scalability。
  - 分離 compute/storage 可讓 PostgreSQL 節點快速上下線、擴展或縮減。

- **節省資源，適合 Serverless**：

  - Compute 節點不再保留 local disk，全部 IO 都走 network。
  - 不使用時自動 scale-to-zero，不佔預算。

---

### 🧩 總結

儲存在 blob storage 的檔案：

- **Image layers**：已物化的 8KB page snapshots
- **Delta layers**：WAL 差異 log
- **內部結構**：以 B+ tree 索引，layer 檔案 immutable，並會作 compaction
- **作用**：重現歷史頁面、支援 random read、branch & PITR 機制

這是一種高度雲原生、歷史追蹤完整、且可無痛 scale 的 Postgres 存儲策略。如果你想深入程式細節，也可以參考 GitHub 專案裡的 storage\_broker、pageserver‑storage 文件。([Neon][1], [Jack Vanlightly][4], [Database of Databases][2])

---

如需進一步探討某部分（例如 compaction 的細節、Pageserver 架構元件），也歡迎隨時再聊～

[1]: https://neon.com/docs/guides/file-storage "File storage - Neon Docs"
[2]: https://dbdb.io/db/neon "Neon - Database of Databases"
[3]: https://neon.com/docs/introduction/architecture-overview "Neon architecture - Neon Docs"
[4]: https://jack-vanlightly.com/analyses/2023/11/15/neon-serverless-postgresql-asds-chapter-3 "Neon - Serverless PostgreSQL - ASDS Chapter 3 - Jack Vanlightly"

















## databricks提到，使用lakebase可以無縫整合lakehouse，我不太懂

不太懂的原因是因為，lakebase的資料放在s3上，lakehouse的資料也放在s3上，這兩者的資料格式不同，怎麼無縫整合的？

在 Databricks 的語境裡，「無縫整合 Lakebase 與 Lakehouse」指的不是把兩種檔案格式硬塞成同一種，而是透過 **平台層（Unity Catalog + Lakeflow 管線 + Lakehouse Federation）把兩邊的資料與權限『接起來』**。底層仍是各自最適合的存儲格式——Lakehouse 保持 Delta Lake（Parquet + transaction log），Lakebase 保留 Postgres page /WAL 物件；開發者與應用程式只看到一張可即時同步、可跨庫查詢的表。以下拆解細節：

### 1. 兩種儲存格式長什麼樣？

| 層次   | Lakehouse (Delta Lake)                                                             | Lakebase (Postgres, serverless)                                    |
| ---- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| 實體檔案 | Parquet data files + `_delta_log` JSON　([Delta][1], [Delta Lake Documentation][2]) | 8 KB Postgres page 與 WAL segmentation 存成 blob 物件　([Databricks][3]) |
| 交易機制 | ACID 由 Delta log 管理                                                                | ACID 由 Postgres 引擎管理　([Microsoft Learn][4])                        |
| 存放位置 | S3/ADLS/GCS 等                                                                      | 同樣是 S3/ADLS/GCS，但資料格式不同                                            |

> **因此：同樣放在 S3，但一邊是列式 Parquet，一邊是行式 Postgres page，並沒有強行共用檔案。**

### 2. 為何還能「無縫」？

#### 2.1 Synced Table：Delta → Postgres 的即時複製

* 你在 Unity Catalog 點一下「Create → Synced Table」，Databricks 會用 **Lakeflow Declarative Pipeline** 把 Delta 表初始快照匯入 Postgres，之後用 **Delta Change Data Feed** 持續增量同步。表在 Postgres 端唯讀，可建索引，延遲可做到毫秒等級。([Databricks Documentation][5])
* 省去自己寫 CDC／Reverse ETL；格式差異由平台處理。

#### 2.2 Lakehouse Federation：查詢層的跨庫 join

* Unity Catalog 把 Lakebase 註冊成 **Foreign Catalog**，Databricks SQL 或 Spark 可直接 `SELECT … FROM postgres_catalog.table JOIN delta_catalog.table`。不需把檔案挪來挪去，只跑網路 I/O。([Databricks Documentation][6])

#### 2.3 統一治理與權限

* 同一份 Metastore 管理 Delta 與 Postgres 表，Row-Level / Column-Level 權限仍生效。([Microsoft Learn][4])

#### 2.4 Delta UniForm：跨格式互讀互寫

* Delta UniForm 會在每次 Delta commit 後 **自動產生 Iceberg/Hudi metadata**，讓任何支援 Iceberg／Hudi 的引擎也能讀這張 Delta 表，不必轉檔，減少第二次複製。([Databricks][7], [Databricks][8])
* 雖然 UniForm 直接服務的是分析端，但它展示了 Databricks 對「格式共存」的解法：同步或生成 metadata，而非強制同一格式。

### 3. 整合流程示意

1. **應用程式寫入 Lakebase**→ Postgres WAL 進 S3。
2. \*\*Lakeflow Pipeline（可選）\*\*把需要分析的行級變更批量寫回 Delta Lake，或直接用 Federation 讀。([Databricks][9])
3. **分析／AI 工作**在 Lakehouse 做 ETL、ML；結果表若要即時服務，再用 Synced Table 推回 Lakebase 供 API 查詢。([Medium][10])

### 4. 常見疑問

| 疑問                        | 解答                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------ |
| 會不會有雙份資料？                 | Synced Table 只同步你選的表；OLTP 與 OLAP 通常關注欄位不同，因此不是全湖複製。                                        |
| 延遲多久？                     | `Continuous` 模式可做到秒級；對高變動表可選 `Triggered` 或 `Snapshot` 平衡成本。([Databricks Documentation][5]) |
| 可以把 Postgres 表回寫 Delta 嗎？ | 目前官方 roadmap 提到「反向同步」在開發中；暫可用 CDC pipeline 或 Lakehouse Federation 查詢。([Databricks][3])     |

### 5. 小結

* **Lakebase** 用 Postgres page/WAL 放在 S3，解決 OLTP 延遲與彈性；
* **Lakehouse (Delta)** 用 Parquet+Log 放在 S3，解決 OLAP 與 AI 場景；
* **Unity Catalog + Synced Table + Federation** 讓兩套格式在「查詢層」無縫合作，不用手寫 ETL，也不會被格式鎖死。

換句話說，Databricks 強調的「無縫」是 **體驗與治理層的無縫**，而不是物理檔案完全一致。只要你透過平台提供的同步與聯邦機制，就能像查同一個資料庫一樣，同時利用 Lakehouse 的批量/AI 能力與 Lakebase 的低延遲 OLTP 能力。

[1]: https://delta.io/ "Delta Lake: Home"
[2]: https://docs.delta.io/latest/delta-uniform.html "Universal Format (UniForm) - Delta Lake Documentation"
[3]: https://www.databricks.com/blog/what-is-a-lakebase "What Is a Lakebase? | Databricks Blog"
[4]: https://learn.microsoft.com/en-us/azure/databricks/oltp/ "What is Lakebase? - Azure Databricks | Microsoft Learn"
[5]: https://docs.databricks.com/aws/en/oltp/sync-data/sync-table "Sync data from Unity Catalog tables to a database instance | Databricks Documentation"
[6]: https://docs.databricks.com/aws/en/query-federation/ "What is Lakehouse Federation? - Databricks Documentation"
[7]: https://www.databricks.com/blog/delta-uniform-universal-format-lakehouse-interoperability "Delta UniForm: a universal format for lakehouse interoperability"
[8]: https://www.databricks.com/blog/announcing-delta-lake-30-new-universal-format-and-liquid-clustering "Delta Lake 3.0: Universal Format & Liquid | Databricks Blog"
[9]: https://www.databricks.com/product/lakebase "Lakebase | Databricks"
[10]: https://medium.com/%40mayuransivasothy/databricks-lakebase-is-this-the-future-of-oltp-on-the-lakehouse-2297f060d9d5 "Databricks LakeBase: Is This the Future of OLTP on the Lakehouse? | by Mayuran | Jun, 2025 | Medium"
