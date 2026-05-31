# DuckLake Manifesto: SQL as a Lakehouse Format

**來源**：[The DuckLake Manifesto: SQL as a Lakehouse Format](https://ducklake.select/manifesto/)

## DuckLake 的核心論點

DuckLake 在舉 BigQuery 的例子時，主要是在驗證它自己的核心想法：

> 既然 lakehouse 最後已經需要一個 database/catalog 來保證 transaction consistency，那就不應該只讓 database 管「目前 table version pointer」這種很小的 metadata，而應該把更多 table metadata 都放進 database 裡管理。

## 推論脈絡

DuckLake manifesto 的脈絡是這樣：

Iceberg / Delta 一開始的設計理念是：不要依賴 database，把 metadata 也放在 object storage 上，用 JSON、Avro、manifest、manifest list 等檔案來描述 table state。這樣可以維持 data lake 的開放性，但問題是後來大家還是需要 transaction、multi-table management、atomic pointer update，所以又加了一層 catalog service，catalog 背後通常還是接 database。DuckLake 認為，這代表原本的設計前提已經改變了。既然 database 已經進入 lakehouse stack，那就應該重新思考：為什麼不直接用 database 管理 metadata？

把 metadata 放進一個真正的資料管理系統，不是 DuckLake 憑空發明的想法，而是大規模 analytical system 已經驗證過的架構方向。DuckLake 原文說，metadata 可以交給 SQL database 管，而 data files 仍然放在 blob storage，用 Parquet 這種開放格式。它接著說，這其實也類似 BigQuery 和 Snowflake 的選擇，只是 BigQuery / Snowflake 底層沒有採用開放 table format 或開放 data file format 作為核心設計。

## 一句話總結

BigQuery 已經證明，把 metadata 管理變成 database/data management problem，是可以 scale 的，而且可以很快。DuckLake 想把這個方向用開放格式重新包裝：data 還是 Parquet，metadata 則是一組 SQL tables。
