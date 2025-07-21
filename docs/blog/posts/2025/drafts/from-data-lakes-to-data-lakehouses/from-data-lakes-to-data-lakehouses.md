---
draft: true
authors:
  - kuanchoulai10
date:
  created: 2025-07-01
  updated: 2025-07-01
categories:
  - Data
tags:
  - The Lakehouse Series
comments: true
---

# The Lakehouse Series: From Data Lakes to Data Lakehouses

!!! info "TLDR"

    After reading this article, you will learn:

    - abc
    - def
    - ghi


<!-- more -->

![Star History Chart](https://api.star-history.com/svg?repos=apache/hudi,apache/iceberg,delta-io/delta,duckdb/ducklake&type=Date)


## From Data Lakes to Lakehouses

### Common Pitfalls in Traditional Data Lakes

Traditional data lakes often suffer from issues such as:

- **Lack of ACID Transactions**: Without transactional guarantees, data corruption and inconsistencies can occur during concurrent writes or failures.
- **Schema Management Challenges**: Evolving schemas can lead to compatibility issues and broken pipelines.
- **Inefficient Query Performance**: Scanning large datasets without proper indexing or partitioning can result in slow query execution.
- **Limited Interoperability**: Many data lakes are tightly coupled with specific engines, limiting flexibility in tool selection. 傳統的 data lake（如 Hive Metastore + HDFS）通常與 Spark 或 Hive 綁很緊。Delta Lake 剛推出時僅支援 Spark，也曾被批評 interoperability 不佳。Apache Hudi 初期也是 Spark-centric，後來才逐漸加強 Flink 與 Presto 支援。

These pitfalls highlight the need for a more robust solution to manage and query data effectively.


### Data Architecture Evolution

<figure markdown="span">
  ![Data Lakehouse](https://www.databricks.com/wp-content/uploads/2020/01/data-lakehouse-new.png)
  [*Data Architecture Evolution*](https://www.databricks.com/blog/2020/01/30/what-is-a-data-lakehouse.html)
</figure>

Data lakes emerged as a solution to store vast amounts of raw data in its native format. However, as organizations sought to derive insights from this data, they encountered challenges in managing and querying it efficiently. This led to the evolution of the "lakehouse" paradigm, which combines the scalability of data lakes with the transactional capabilities of data warehouses. 2020年 databricks 首次提出 lakehouse 概念，旨在解決傳統 data lake 的問題。

- Transaction support: In an enterprise lakehouse many data pipelines will often be reading and writing data concurrently. 
- Schema enforcement and governance: The Lakehouse should have a way to support schema enforcement and evolution, supporting DW schema architectures such as star/snowflake-schemas
- BI support: Lakehouses enable using BI tools directly on the source data. 
- Storage is decoupled from compute: In practice this means storage and compute use separate clusters, thus these systems are able to scale to many more concurrent users and larger data sizes.
- Openness: The storage formats they use are open and standardized, such as Parquet, and they provide an API so a variety of tools and engines, including machine learning and Python/R libraries, can efficiently access the data directly.
- Support for diverse data types ranging from unstructured to structured data
- Support for diverse workloads: including data science, machine learning, and SQL and analytics.
- End-to-end streaming: Real-time reports are the norm in many enterprises. 


Table formats play a pivotal role in enabling this transition by providing structure and governance to otherwise unstructured data.



### The Role of Lakehouse Data Formats

At the heart of this are data lakehouse table formats, which are metadata layers that allow tools to interact with data lake storage like a traditional database.


Table formats like Apache Hudi, Apache Iceberg, and Delta Lake address these challenges by introducing:

- **ACID Transactions**: Ensuring data consistency and reliability during writes and updates.
- **Schema Evolution Support**: Allowing seamless changes to data schemas without breaking downstream processes.
- **Efficient Metadata Management**: Leveraging manifest or log files to optimize query planning and execution.
- **Multi-Engine Compatibility**: Enabling interoperability across various processing engines like Spark, Flink, and Trino.

By bridging the gap between raw data storage and structured data management, lakehouse data formats empower organizations to build scalable, performant, and reliable lakehouse architectures.

each lakehouse data format has its own design philosophy and its own implementation details, but they all share the common goal of addressing the limitations of traditional data lakes while providing a unified platform for data analytics and machine learning.



## References

- [Apache Iceberg Copy-On-Write (COW) vs Merge-On-Read (MOR): A Deep Dive](https://estuary.dev/blog/apache-iceberg-cow-vs-mor/)
- [Exploring the Architecture of Apache Iceberg, Delta Lake, and Apache Hudi](https://www.dremio.com/blog/exploring-the-architecture-of-apache-iceberg-delta-lake-and-apache-hudi/)
- [Comparison of Data Lake Table Formats (Apache Iceberg, Apache Hudi and Delta Lake)](https://www.dremio.com/blog/comparison-of-data-lake-table-formats-apache-iceberg-apache-hudi-and-delta-lake/)
- [Table Format Governance and Community Contributions: Apache Iceberg, Apache Hudi, and Delta Lake](https://www.dremio.com/blog/table-format-governance-and-community-contributions-apache-iceberg-apache-hudi-and-delta-lake/)
- [Table Format Partitioning Comparison: Apache Iceberg, Apache Hudi, and Delta Lake](https://www.dremio.com/blog/table-format-partitioning-comparison-apache-iceberg-apache-hudi-and-delta-lake/)
- [Tampa Bay DE Meetup: The Who, What and Why of Data Lake Table Formats (Iceberg, Hudi, Delta Lake)](https://www.youtube.com/watch?v=1eEcWopaFqE)
- [Hudi vs Iceberg vs Delta Lake: Data Lake Table Formats Compared](https://lakefs.io/blog/hudi-iceberg-and-delta-lake-data-lake-table-formats-compared/)
- [What Is a Lakehouse?](https://www.databricks.com/blog/2020/01/30/what-is-a-data-lakehouse.html)