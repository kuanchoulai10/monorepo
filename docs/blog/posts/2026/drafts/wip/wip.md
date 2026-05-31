---
draft: true
authors:
  - kuanchoulai10
date:
  created: 2026-05-30
  updated: 2026-05-31
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

## 素材清單

各素材的詳細摘要拆分到 `materials/` 目錄下：

- [Firebolt × Iceberg @ Trillion Rows](materials/firebolt-iceberg-trillion-rows.md) — Firebolt 在 2026 Iceberg Summit 講如何把元數據當成資料來處理，解 40 兆行、20PB、400 萬檔案規模下的五大瓶頸。
- [BigQuery CMETA 的三個時間點](materials/bigquery-cmeta-timeline.md) — 從 2021 VLDB 論文到 2025 產品化的時間軸，釐清 CMETA 不是 2025 才出現的技術。
- [DuckLake Manifesto: SQL as a Lakehouse Format](materials/ducklake-manifesto.md) — 既然 lakehouse 已經需要 database，那為什麼不直接把 metadata 也放進 database 裡管理？
- [Slack × Iceberg @ Scale](materials/slack-iceberg-at-scale.md) — Slack 180PB 數據湖倉的 Iceberg 導入經驗：從 streaming ingestion、CDC（MOR + Ice Chipper），到 REST Catalog 上的 data mesh zero-copy sharing。
