---
draft: true
authors:
  - kuanchoulai10
date:
  created: 2025-06-02
  updated: 2025-06-06
categories:
  - Data
tags:
  - The Lakehouse Series
comments: true
---

# The Lakehouse Series: Hudi vs Iceberg vs Delta Lake — Format Wars Begin

!!! info "TLDR"

    After reading this article, you will learn:

    - abc
    - def
    - ghi


<!-- more -->

![Star History Chart](https://api.star-history.com/svg?repos=apache/hudi,apache/iceberg,delta-io/delta,duckdb/ducklake&type=Date)


## From Data Lakes to Lakehouses

**Common Pitfalls in Traditional Data Lakes**

Traditional data lakes often suffer from issues such as:

- **Lack of ACID Transactions**: Without transactional guarantees, data corruption and inconsistencies can occur during concurrent writes or failures.
- **Schema Management Challenges**: Evolving schemas can lead to compatibility issues and broken pipelines.
- **Inefficient Query Performance**: Scanning large datasets without proper indexing or partitioning can result in slow query execution.
- **Limited Interoperability**: Many data lakes are tightly coupled with specific engines, limiting flexibility in tool selection. 傳統的 data lake（如 Hive Metastore + HDFS）通常與 Spark 或 Hive 綁很緊。Delta Lake 剛推出時僅支援 Spark，也曾被批評 interoperability 不佳。Apache Hudi 初期也是 Spark-centric，後來才逐漸加強 Flink 與 Presto 支援。

These pitfalls highlight the need for a more robust solution to manage and query data effectively.


**From Data Lakes to Lakehouses**

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



**The Role of Lakehouse Data Formats in Solving These Issues**

At the heart of this are data lakehouse table formats, which are metadata layers that allow tools to interact with data lake storage like a traditional database.


Table formats like Apache Hudi, Apache Iceberg, and Delta Lake address these challenges by introducing:

- **ACID Transactions**: Ensuring data consistency and reliability during writes and updates.
- **Schema Evolution Support**: Allowing seamless changes to data schemas without breaking downstream processes.
- **Efficient Metadata Management**: Leveraging manifest or log files to optimize query planning and execution.
- **Multi-Engine Compatibility**: Enabling interoperability across various processing engines like Spark, Flink, and Trino.

By bridging the gap between raw data storage and structured data management, lakehouse data formats empower organizations to build scalable, performant, and reliable lakehouse architectures.

each lakehouse data format has its own design philosophy and its own implementation details, but they all share the common goal of addressing the limitations of traditional data lakes while providing a unified platform for data analytics and machine learning.


## Apache Hudi Overview

Apache Hudi (Hadoop Upserts Deletes and Incrementals) was created by Vinoth Chandar at Uber in 2016 to solve real-world data ingestion challenges in Uber's massive data platform. Originally developed to handle frequent updates and deletes in their data lake while maintaining query performance, Hudi was open-sourced in 2017 and became an Apache Software Foundation top-level project in 2020. As of June, 2025, the project has garnered over 5,800 GitHub stars with contributions from 500 developers worldwide. The project is currently maintained by the Apache Software Foundation, with key contributors from Uber, Amazon, Onehouse, and other organizations driving its development roadmap.

Hudi's core design philosophy centers around providing **incremental processing primitives** for data lakes, treating datasets as **continuously evolving streams** rather than static snapshots. The framework is built around the concept of **upserts** (update + insert operations) and **incremental consumption**, enabling near real-time data pipelines with strong consistency guarantees. Hudi distinguishes itself by offering two storage types - **Copy-on-Write (COW)** for **read-heavy workloads** and **Merge-on-Read (MOR) for write-heavy scenarios** - allowing users to optimize for their specific use case.

### Timeline

Changes to table state (writes, table services, schema changes, etc) are recorded as actions in the Hudi timeline. The Hudi timeline is a log of all actions performed on the table at different instants (points in time). It is a key component of Hudi's architecture, acting as a source of truth for the state of the table.

<figure markdown="span">
  ![Actions in the Timeline](https://hudi.apache.org/assets/images/hudi-timeline-actions-e56d0d9fad5645d9910f2591ad7775de.png)
  [*Actions in the Timeline*](https://hudi.apache.org/docs/next/timeline/)
</figure>

- **requested instant**: Instant time representing when the action was requested on the timeline and acts as the transaction id. An immutable plan for the action should be generated before the action is requested.
- **completed instant**: Instant time representing when the action was completed on the timeline. All relevant changes to table data/metadata should be made before the action is completed.
- **state**: state of the action. valid states are `REQUESTED`, `INFLIGHT` and `COMPLETED` during an action's lifecycle.
- **type**: the kind of action performed. For example, `COMMIT`, `DELTA_COMMIT`, `REPLACE_COMMIT`, `COMPACTION`, `INDEXING`, `ROLLBACK`, etc.



### Storage Layout

Hudi organizes data tables into a **directory** structure under a base path on a storage. Tables are **optionally broken up into partitions**, based on partition columns defined in the table schema. Within each **partition**, files are organized into **file groups**, uniquely identified by a file ID (uuid). Each **file group** contains several **file slices**. Each **slice** contains a **base file** (parquet/orc/hfile) (defined by the config - `hoodie.table.base.file.format`) written by a commit that completed at a certain instant, along with set of **log files** (`.log.`) written by commits that completed before the next base file's requested instant.

A file slice represents what the data looked like at a given time. A file group contains a subset of the row data. a file group is essentially a chunk of row data, and a file slice captures the state of that chunk at a specific commit time.

Hudi employs **Multiversion Concurrency Control (MVCC)**, where **compaction** action merges logs and base files to produce new file slices and **cleaning** action gets rid of unused/older file slices to reclaim space on the file system. **All metadata** including timeline, metadata table are stored in a special `.hoodie` directory under the base path.

---

Here is a series of operations that illustrate how Hudi manages data over time:

<figure markdown="span">
  ![File Format Structure in Hudi](https://hudi.apache.org/assets/images/file_format_2-b4e10be3218071ebde48f3603109126f.png)
  [*File Format Structure in Hudi*](https://hudi.apache.org/docs/hudi_stack#file-formats)
</figure>

At **t1**, Apache Hudi creates an initial base file (**b**) for a file group, capturing a snapshot of the data at that time—this forms the starting point for **File Slice 1**. As new data arrives, delta commits at **t2** and **t3** append data blocks to a log file, allowing efficient updates without rewriting the base file. At **t4**, another delta commit occurs, but the operation is rolled back, resulting in a rollback block being written to a second log file. This rollback preserves ACID semantics by marking the data from **t4** as invalid. 

At **t5**, Hudi performs a **compaction**, merging all accumulated log files into a new base file (**b'**), effectively starting **File Slice 2**. This compaction improves read performance by reducing the need for on-the-fly merging. Following this, at **t6**, a delete block is appended to a new log file associated with **b'**, indicating a record deletion.

Later on, at **t10**, a **clean** operation is executed to remove obsolete or unreferenced files, such as outdated log files or old base files, maintaining storage hygiene. Finally, at **t15**, a **clustering** operation reorganizes the files (e.g., by sorting) to further optimize query performance. Throughout this timeline, Hudi maintains a detailed history of actions to support versioned reads, time travel, and transactional guarantees.

---

<figure markdown="span">
  ![Apache Hudi's Table format](https://hudi.apache.org/assets/images/table_format_1-40380ed7db1d89a0f66dba3ba70c229a.png)
  [*Apache Hudi's Table format*](https://hudi.apache.org/docs/hudi_stack#table-format)
</figure>

In the first step, new records are written to the latest file slice of the appropriate file group. If a suitable file group doesn’t exist, a new one is created. The files are stored under the partition path of the table.

Next, the write action is committed to the timeline. This commit is added to the event log, recording the exact point in time when the write occurred.

Then, when a read is triggered, Hudi consults the timeline and metadata table to find the relevant file slices. This determines which version of the data should be read.

Finally, the read operation loads the file slices. If needed, Hudi merges base files with log files to reconstruct the correct version of the data before returning the results.

---

<figure markdown="span">
  ![Storage Layouts](https://hudi.apache.org/assets/images/MOR_new-aa806492cc5034a48039f9d8a392b9d8.png)
  [*Storage Layouts*](https://hudi.apache.org/docs/storage_layouts)
</figure>

At the start, a series of file groups each contain a base file labeled with version **10:05**, which corresponds to a **previous compaction commit** that consolidated earlier changes into columnar Parquet files. These base files serve as the foundation for reading data efficiently in a **read-optimized mode**.

Later in the timeline, a new delta commit at **10:10** occurs, representing an upsert operation where inserts and updates are written. These changes are appended as **row-based log files** to the appropriate file groups. For example, File Groups 2 and 4 receive additional logs corresponding to the most recent commit at 10:10. File Group 3, however, remains unchanged after 10:05, requiring no new writes.

After the 10:10 commit, two types of queries can be executed. In a **read-optimized query**, **Hudi returns only the columnar base files without merging any append logs**. This means the result reflects the state of the data as of the last compaction (version **10:05**). For this query mode, File Groups 1, 2, and 3 all return their 10:05 base files directly, while File Group 4 is excluded because it has no base file at that version.

Alternatively, a **near real-time query** will read from the most recent commit and merge base files with append logs as necessary. In this mode, File Groups 1 and 2 return their base file at version 10:05, combined with the latest append logs to reflect the most up-to-date data. File Group 3 requires no merging since it has no logs beyond the base file. File Group 4, which lacks a recent base file, returns only the log content, delivering the most recent updates without a base file merge.

Through this timeline and storage layout, the diagram captures how Hudi supports both high-throughput ingestion with deferred compaction and flexible query models that balance performance with freshness of data.

### Table Services

<figure markdown="span">
  ![Table Services in Hudi](https://hudi.apache.org/assets/images/table_services_2-46585c7180ac268596828a72f5f42b04.png)
  [*Table services in Hudi*](https://hudi.apache.org/docs/hudi_stack#table-services)
</figure>



Apache Hudi offers various table services to help keep the table storage layout and metadata management performant. 

- **Clustering**: The clustering service, akin to features in cloud data warehouses, allows users to group frequently queried records using sort keys or merge smaller Base Files into larger ones for optimal file size management.
- **Compaction**: Hudi's compaction service, featuring strategies like date partitioning and I/O bounding, merges Base Files with delta logs to create updated Base Files.
- **Cleaning**: Cleaner service works off the timeline incrementally, removing File Slices that are past the configured retention period for incremental queries, while also allowing sufficient time for long running batch jobs (e.g Hive ETLs) to finish running.
- **Indexing**: Hudi's scalable metadata table contains auxiliary data about the table.


### Table Types and Query Types



## Apache Iceberg Overview

## Delta Lake Overview






## References
- [Exploring the Architecture of Apache Iceberg, Delta Lake, and Apache Hudi](https://www.dremio.com/blog/exploring-the-architecture-of-apache-iceberg-delta-lake-and-apache-hudi/)
- [Comparison of Data Lake Table Formats (Apache Iceberg, Apache Hudi and Delta Lake)](https://www.dremio.com/blog/comparison-of-data-lake-table-formats-apache-iceberg-apache-hudi-and-delta-lake/)
- [Table Format Governance and Community Contributions: Apache Iceberg, Apache Hudi, and Delta Lake](https://www.dremio.com/blog/table-format-governance-and-community-contributions-apache-iceberg-apache-hudi-and-delta-lake/)
- [Table Format Partitioning Comparison: Apache Iceberg, Apache Hudi, and Delta Lake](https://www.dremio.com/blog/table-format-partitioning-comparison-apache-iceberg-apache-hudi-and-delta-lake/)
- [Tampa Bay DE Meetup: The Who, What and Why of Data Lake Table Formats (Iceberg, Hudi, Delta Lake)](https://www.youtube.com/watch?v=1eEcWopaFqE)
- [Hudi vs Iceberg vs Delta Lake: Data Lake Table Formats Compared](https://lakefs.io/blog/hudi-iceberg-and-delta-lake-data-lake-table-formats-compared/)
- [What Is a Lakehouse?](https://www.databricks.com/blog/2020/01/30/what-is-a-data-lakehouse.html)