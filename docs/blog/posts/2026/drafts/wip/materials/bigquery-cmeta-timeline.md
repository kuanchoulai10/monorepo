# BigQuery CMETA 的三個時間點

**來源**：

- 論文：[Big Metadata: When Metadata is Big Data (VLDB 2021)](https://vldb.org/pvldb/vol14/p3083-edara.pdf)
- 官方部落格：[BigQuery under the hood: The power of the Column Metadata index aka CMETA (2025)](https://cloud.google.com/blog/products/data-analytics/understanding-the-bigquery--column-metadata-cmeta-index/)

BigQuery 的 **CMETA**，也就是 **Column Metadata index**，至少可以分成三個時間點來看。

## 三個時間點

**第一，作為 BigQuery 內部技術，2021 年以前就已經存在。**

Google 在 2021 年 VLDB 論文《Big Metadata: When Metadata is Big Data》中說，BigQuery 已經建了一套 metadata management system，用來以分散式方式管理細粒度的 column/block-level metadata，並把 metadata 組織成 system table 來服務查詢規劃與 pruning。這表示它不是 2021 才開始做，而是到 2021 年公開發表時，系統已經在 BigQuery 內部成形並被用來支援大規模查詢。

**第二，作為公開研究成果，CMETA 是 2021 年正式出現在論文中的。**

Google Research 的頁面把這篇論文列為 **VLDB 2021**，Google Cloud 2025 年的官方文章也明確說「In 2021, we presented the Column Metadata, CMETA, index in a 2021 VLDB paper」。所以如果你問「這個技術最早什麼時候被公開提出」，答案就是 **2021 年**。([Google Research][1]) ([Google Cloud][2])

**第三，作為 BigQuery 使用者可觀察、可查詢的產品能力，公開文件是在 2025 年左右變得明確。**

Google Cloud 在 2025 年 9 月發表文章介紹「BigQuery under the hood: The power of the Column Metadata index aka CMETA」，並說 BigQuery 現在會自動建立與管理 CMETA system table，使用者不需要手動維護。BigQuery 文件也有「Metadata indexing for BigQuery tables」頁面，說 BigQuery 會自動為超過 1 GiB 的 BigQuery table 建立 metadata index，並且可以透過 `LAST_METADATA_INDEX_REFRESH_TIME`、`metadata_cache_statistics` 等欄位觀察使用狀況。([Google Cloud][2]) ([Google Cloud Documentation][3])

## 結論

**CMETA 不是 2025 年才出現的技術。它最晚在 2021 年已經作為 BigQuery 內部技術被公開發表；但 Google Cloud 到 2025 年才用比較產品化、使用者可理解的方式，把「Column Metadata index, CMETA」這個能力正式寫進部落格與文件中。**

## 可在文章中引用的段落

> BigQuery 的 CMETA, Column Metadata index, 並不是最近才發明的功能。Google 早在 2021 年 VLDB 論文《Big Metadata: When Metadata is Big Data》中就公開描述了這套 metadata management design。它的核心想法是把細粒度的 block-level 與 column-level metadata 當成 BigQuery 自己也可以分散式處理的資料來管理，而不是只把 metadata 放在集中式 catalog 或個別資料檔案 footer 裡。到了 2025 年，Google Cloud 才更明確地以產品文件與官方文章介紹 CMETA，說明 BigQuery 會自動維護 column metadata index，並用它協助 query planner 做更細粒度的 pruning。

[1]: https://research.google/pubs/big-metadata-when-metadata-is-big-data/ "Big Metadata: When Metadata is Big Data"
[2]: https://cloud.google.com/blog/products/data-analytics/understanding-the-bigquery--column-metadata-cmeta-index/ "Understanding the BigQuery column metadata (CMETA) index | Google Cloud Blog"
[3]: https://docs.cloud.google.com/bigquery/docs/metadata-indexing-managed-tables "Metadata indexing for BigQuery tables | Google Cloud Documentation"
