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


### Table Types

Hudi table types define how data is stored and how write operations are implemented on top of the table (i.e how data is written). In turn, query types define how the underlying data is exposed to the queries (i.e. how data is read).

**Copy-on-Write (COW) Table**

<figure markdown="span">
  ![Copy-on-Write (COW) Table](https://hudi.apache.org/assets/images/COW_new-34af9e190486467e1b0bfbc5dc410ee2.png)
  [*Copy-on-Write (COW) Table*](https://hudi.apache.org/docs/next/table_types/#copy-on-write-table)
</figure>

The Copy-on-Write (CoW) table type is optimized for read-heavy workloads. In this mode, record updates or deletes trigger the creation of new base files in a file group and there are no log files written. This ensures that each query reads only the base files, offering high read performance with no need to merge log files dynamically. While CoW tables are ideal for OLAP scans/queries, their write operations can be slower due to the overhead of rewriting base files during updates or deletes, even if small percentage of records are modified in each file.

good use-cases for CoW tables:

- Batch ETLs/Data Pipelines
- Data Warehousing on Data Lakes
- Static or Slowly Changing Data

**Merge-on-Read (MOR) Table**

<figure markdown="span">
  ![Merge-on-Read (MOR) Table](https://hudi.apache.org/assets/images/MOR_new-aa806492cc5034a48039f9d8a392b9d8.png)
  [*Merge-on-Read (MOR) Table*](https://hudi.apache.org/docs/next/table_types/#copy-on-write-table)
</figure>

The Merge-on-Read (MoR) table type balances the write and read performance by combining lightweight log files with the base file using periodic compaction. Data updates and deletes are written to log files (in row based formats like Avro or columnar/base file formats) and these changes in log files are then merged dynamically with base files during query execution. This approach reduces write latency and supports near real-time data availability. However, query performance may vary depending on whether the log files are compacted.

great fit for the following use-cases:

- Change Data Capture Pipelines
- Streaming Data Ingestion
- Hybrid Batch + Streaming workloads
- Frequent Updates and Deletes

**Comparison**

<figure markdown="span">
  ![comparison](./static/hudi-vs-iceberg-vs-delta-lake/comparison.png)
  [*Comparison Between COW and MOR Tables*](https://hudi.apache.org/docs/next/table_types/#comparison)
</figure>

### Query Types

- **Snapshot Queries**: Queries see the latest snapshot of the table as of the latest completed action. These are the regular SQL queries everyone is used to running on a table. 
- **Time Travel Queries**: Queries a snapshot of a table as of a given instant in the past.
- **Read Optimized Queries**(Only MoR tables) : Read-optimized queries provides excellent snapshot query performance via purely columnar files (e.g. Parquet base files).
- **Incremental Queries (Latest State)**: Incremental queries only return new data written to the table since an instant on the timeline.
- **Incremental Queries(CDC)**: These are another type of incremental queries, that provides database like change data capture streams out of Hudi tables.

About Incremental Queries:

<figure markdown="span">
  ![Incremental Queries](https://hudi.apache.org/assets/images/hudi_timeline-bf5d8c5e59180434796d82af2b783e6c.png)
  [*Incremental Queries*](https://hudi.apache.org/docs/next/table_types/#incremental-queries)
</figure>

In streaming workflows, Hudi combines the timeline (ingestion time) with partitions (event time), enabling both accurate tracking of data updates and precise querying by event time. This makes incremental ETL pipelines more efficient and reliable.


## Apache Iceberg Overview

Apache Iceberg was born at Netflix in 2017 from the brilliant minds of Ryan Blue and Daniel Weeks, who were wrestling with the limitations of Hive tables at Netflix's mind-boggling scale. When you're dealing with petabytes of data and schema evolution nightmares, you need something better than what existed. Open-sourced in 2018 and graduating to an Apache Software Foundation top-level project in 2020, Iceberg has become a heavyweight in the lakehouse arena. As of June 2025, the project boasts over 7,500 GitHub stars with contributions from more than 600 developers worldwide, backed by industry giants like Netflix, Apple, Tabular, Dremio, and AWS.

What sets Iceberg apart is its **architectural elegance**. Built on a sophisticated **3-tier metadata hierarchy**, Iceberg orchestrates table-level metadata files (`metadata.json`), snapshot-level manifest lists, and data-level manifest files into a symphony of efficiency.

Iceberg's design philosophy centers around **hidden partitioning** and **schema evolution without the headaches**. Forget about manually managing partitions or rewriting entire tables when your schema changes — Iceberg handles this behind the scenes like a data concierge. The format's **storage-agnostic approach** means true multi-engine compatibility through standardized APIs and REST-based catalogs, making it the diplomat of the lakehouse world.

At its core, Iceberg treats every table state as an **immutable, versioned snapshot** with complete lineage tracking. This enables bulletproof concurrent reads and writes, automatic schema evolution, and surgical partition pruning. Built with both backward and forward compatibility in mind, Iceberg ensures your data infrastructure won't break when you upgrade.

### Storage Layout

<figure markdown="span">
  ![iceberg architecture](./static/hudi-vs-iceberg-vs-delta-lake/iceberg.drawio.svg){width="600"}
  *Iceberg Architecture*
</figure>

**Catalog**

Think of Iceberg's catalog as your **data's personal directory service** — like the phone book of the data world, but actually useful! It uses familiar systems like Hive Metastore or AWS Glue to keep track of where your tables live, making it a breeze for query engines like Spark or Presto to find what they're looking for.

Here's where things get exciting: the **REST catalog**. Introduced in Iceberg 0.14.0, it's like having a universal translator for your data infrastructure. Instead of each query engine speaking its own dialect, they all chat through this standardized REST API.

The beauty of the REST catalog? One client rules them all. No more wrestling with different JARs or compatibility nightmares when you want to connect engines like Athena or Starburst. It's like having a single remote control that works with every device in your house — finally!

Iceberg REST Catalog 是一套 API 規範，旨在提供統一的方式讓各種查詢引擎與 Catalog 互動。實際的 REST Catalog Server 實作需由開發者或社群根據該規範自行開發。

Who also implemented the REST catalog server? Apache Polaris, Project Nessie, Apache Gravitino



```
┌────────────────────────────┐
│        查詢引擎 (Trino)     │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│     Polaris REST Catalog   │
│ (實作 Iceberg 的 REST API)  │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│     Iceberg 表格與元資料     │
│ (儲存在 S3、HDFS 等儲存系統)  │
└────────────────────────────┘
```

**Metadata Files**

Picture metadata files as your table's comprehensive diary, written in JSON and stored at the **table level**. These files are the keepers of everything important: what your table looks like, how it's organized, and which data files actually belong to it. Without these files, your query engines would be like tourists without a map — completely lost!

Here's what makes these files so clever:

- **Schemas**: Think of this as your table's DNA — it remembers every field structure it's ever had, including names, types, and whether nulls are welcome at the party. This is what makes **schema evolution** possible without breaking everything downstream.
- **Snapshots**: Your table's photo album! Every time something changes, Iceberg takes a snapshot with all the juicy details — timestamp, what happened, and which manifest list to check. This is your ticket to time travel and bulletproof consistency.
- **Current Snapshot ID**: The "you are here" marker that tells everyone which version of reality they're looking at when they query your table.
- **Partition Specs**: The traffic director for your data, deciding where each record should live based on clever transformations like bucketing or truncating. Like a smart filing system that evolves over time.
- **Location**: Your table's home address in the storage world — the root path where all the metadata, manifests, and data files hang out together.

**Snapshots**

A snapshot is like taking a Polaroid of your entire table — it captures exactly what your data looked like at that precise moment. Each snapshot is basically a guest list of all the data files that were invited to the table party at that specific time.

Here's the clever part: instead of listing millions of data files directly (imagine the paperwork!), snapshots delegate the heavy lifting to manifest files, and all those manifests get neatly organized in a single manifest list file. It's like having a master guest list that points to smaller, more manageable sub-lists.

**Manifest List Files**

Working at the **snapshot level**, manifest list files are like event coordinators who keep track of all the different guest lists (manifest files) for a particular table snapshot. These Avro-formatted files don't just list manifests — they're smart enough to include a cheat sheet about each one.

Each manifest gets its own summary card with details like:

- Where to find it (`manifest_path`)
- How big it is (`manifest_length`) 
- Which partitioning rules it follows (`partition_spec_id`)
- When it joined the party (`added_snapshot_id`)
- A headcount of added, existing, and deleted files
- Partition statistics that help with query pruning

This hierarchical approach is brilliant for performance — instead of opening every single guest list to find what you need, you can quickly scan the coordinator's summary and only dive into the relevant details.

**Manifest Files**

At the **data level**, manifest files are where the rubber meets the road. These Avro-formatted files are like detailed guest lists that know everything about each data file in their care. They're the ones doing the heavy lifting when it comes to tracking your actual data.

For every data file, the manifest knows:

- Exactly where it lives (`file_path`)
- What format it prefers (`file_format` — Parquet, ORC, or Avro)
- Its partition neighborhood (`partition_data`)
- How many records it's hosting (`record_count`)
- Its storage footprint (`file_size_in_bytes`)
- Detailed statistics for every column — think value counts, null counts, and data ranges that make query optimization possible

This granular tracking is what makes Iceberg so powerful at query planning. Instead of blindly scanning everything, query engines can peek at these manifests and make smart decisions about which files actually contain the data they need.

**Putting all together**

1. 一個 Manifest List File 可以包含多個 Manifest Files 嗎？

是的。 在 Apache Iceberg 中，每個快照（snapshot）都會有一個對應的 Manifest List File，該檔案列出該快照所包含的所有 Manifest Files。 這些 Manifest Files 追蹤了構成該快照的資料檔案（如 Parquet、ORC、Avro 等）。 這種設計有助於查詢優化，因為查詢引擎可以根據 Manifest List 中的摘要資訊，快速篩選出相關的 Manifest Files，避免不必要的掃描，提高查詢效率。

⸻

2. 這些 Manifest Files 所指向的 Data Files 會重複嗎？

在正常情況下，不會重複。 Iceberg 的設計原則之一是每個資料檔案（Data File）在同一個快照中只會被追蹤一次。 這意味著在一個快照的 Manifest List 中，指向的多個 Manifest Files 所涵蓋的 Data Files 是互不重疊的。 這種結構有助於：
	•	查詢優化：避免重複掃描相同的資料檔案，提高查詢效率。
	•	資料一致性：確保每筆資料在快照中只出現一次，避免重複計算或統計。
	•	元資料管理：簡化元資料的維護與更新，降低出錯的可能性。

然而，在某些特定情況下，仍可能出現重複的資料檔案，例如：
	•	手動或錯誤的操作：例如，使用 add_files 程序多次將相同的資料檔案加入表格，可能導致重複。
	•	不當的資料更新流程：如在執行 MERGE INTO 操作時，未正確處理資料的新增與更新，可能會產生重複的資料檔案。
	•	多個寫入者的競爭條件：在高併發的寫入環境中，若未妥善處理寫入的同步與衝突解決，可能導致重複的資料檔案被加入。

為了避免上述情況，建議：
	•	使用 Iceberg 提供的 API 進行資料操作：確保所有的資料新增、更新與刪除操作都透過 Iceberg 的 API 進行，以維持元資料的一致性。
	•	實施寫入衝突檢查與解決機制：在多寫入者環境中，採用 Iceberg 的衝突檢查與解決策略，避免資料重複。
	•	定期執行資料清理與壓縮操作：使用 Iceberg 提供的 rewrite_manifests 或 rewrite_data_files 等程序，清理重複或冗餘的資料檔案。

⸻

3. 一個 Metadata File（metadata.json）可以包含多個 Manifest List Files 嗎？

是的。 每個 metadata.json 檔案代表表格的一個版本，並追蹤該版本的所有快照（snapshots）。 每個快照對應一個 Manifest List File，用於列出該快照所包含的 Manifest Files。 因此，一個 metadata.json 檔案可以關聯多個 Manifest List Files，每個對應不同的快照。

### Query Types

Apache Iceberg offers a range of query capabilities that, while not identical to Apache Hudi’s, provide robust data management and analysis features:
	•	Time Travel: Query historical snapshots of your data using SQL clauses like TIMESTAMP AS OF or VERSION AS OF.  ￼
	•	Incremental Reads: Perform incremental data ingestion by scanning snapshots for added or removed files. This is particularly useful for change data capture (CDC) scenarios.  ￼
	•	Metadata Queries: Access metadata tables such as history, snapshots, and files to gain insights into table versions, schema changes, and data file statistics.  ￼

While Apache Hudi provides specialized query types like incremental and snapshot queries tailored for streaming data, Apache Iceberg’s approach focuses on providing a consistent and flexible framework for both batch and streaming workloads, with strong support for schema evolution and concurrent writes.

## Delta Lake Overview


Delta Lake emerged from Databricks in 2019 as the brainchild of the same team that created Apache Spark, led by Matei Zaharia and his colleagues who were tackling the reliability and performance challenges of big data pipelines at scale. Born from real-world production pain points at Databricks and their enterprise customers, Delta Lake was designed to bring ACID transactions and data versioning to the data lake ecosystem. Open-sourced under the Apache 2.0 license in 2019 and later contributed to the Linux Foundation as the Delta Lake project, it has rapidly gained traction with over 8,100 GitHub stars and contributions from over 350 developers worldwide. The project enjoys strong backing from Databricks, Microsoft, AWS, and a growing ecosystem of data platform vendors.

Delta Lake's architecture is built around **simplicity and reliability**. At its core, Delta Lake uses a **transaction log** (the `_delta_log` directory) that acts as a single source of truth, recording every change to the table as ordered, atomic commits stored in JSON files. This **log-based approach** ensures ACID guarantees while maintaining compatibility with existing Parquet-based data lakes. Delta Lake's design philosophy emphasizes **zero-copy cloning**, **automatic schema enforcement**, and **seamless integration with Apache Spark**, making it the pragmatic choice for organizations already invested in the Spark ecosystem. The format's **unified streaming and batch processing** capabilities, combined with **built-in data quality constraints** and **automatic file management**, position Delta Lake as the Swiss Army knife of lakehouse formats.

### Storage Layout

Ever wondered how Delta Lake keeps track of all your data without losing its mind? The secret sauce lies in its beautifully simple yet powerful architecture that revolves around one core principle: **everything goes through the transaction log**. Think of it as your data's personal accountant who never takes a day off!

**The Transaction Log: Your Data's Single Source of Truth**

Picture the `_delta_log` directory as the ultimate diary of your table — it's where Delta Lake writes down every single thing that happens to your data, no matter how small. This isn't just any ordinary log; it's a **chronologically ordered sequence of JSON files** that captures every action like a meticulous historian.

Here's what makes this approach absolutely brilliant:

```
my_table/
├── _delta_log/
│   ├── 00000000000000000000.json  # The beginning of time
│   ├── 00000000000000000001.json  # First transaction
│   ├── 00000000000000000002.json  # Second transaction
│   └── ...
├── part-00000-xyz.parquet         # Actual data files
├── part-00001-abc.parquet
└── ...
```

Each JSON file in the transaction log is like a **commit message on steroids** — it doesn't just say "hey, something changed," it provides the complete blueprint of what the table should look like after that transaction. It's like having a GPS that not only tells you where you are, but also remembers every turn you've made to get there!

**Transaction Log Files: The Building Blocks**

Every time you perform an operation (insert, update, delete, schema change), Delta Lake creates a new numbered JSON file in the `_delta_log` directory. These files contain **actions** that describe exactly what happened:

- **Add File Actions**: "Hey, we've got a new data file joining the party! Here's where it lives and what it contains."
- **Remove File Actions**: "Time to say goodbye to this old file — it's been replaced or deleted."
- **Metadata Actions**: "The table schema just got an upgrade — here are the new rules everyone needs to follow."
- **Protocol Actions**: "We're updating the table format version — buckle up for new features!"

What's mind-blowing is that these JSON files are **immutable** — once written, they never change. It's like having a paper trail that can't be tampered with, ensuring your data's history is bulletproof.

**Checkpoints: The Smart Shortcuts**

Now, you might be thinking: "What happens when I have thousands of these JSON files? Won't reading through all of them take forever?" That's where Delta Lake's **checkpoint mechanism** comes to the rescue like a superhero!

Every 10 commits (by default), Delta Lake creates a special **checkpoint file** — think of it as a "save game" feature that captures the entire state of your table at that moment. Instead of reading through hundreds of individual transaction files, query engines can just load the latest checkpoint and then catch up with any newer transactions. It's like fast-forwarding through a movie to get to the good parts!

```
_delta_log/
├── 00000000000000000000.json
├── ...
├── 00000000000000000009.json
├── 00000000000000000010.checkpoint.parquet  # Snapshot at commit 10
├── 00000000000000000011.json
├── ...
├── 00000000000000000020.checkpoint.parquet  # Snapshot at commit 20
└── ...
```

**Data Files: Where the Magic Lives**

While the transaction log handles all the bookkeeping, your actual data lives in **Parquet files** (or other columnar formats) stored right alongside the `_delta_log` directory. These files are like the actual books in a library, while the transaction log is the card catalog that tells you exactly which books exist and where to find them.

Here's the elegant part: Delta Lake doesn't move or modify your existing data files when you perform updates or deletes. Instead, it plays a clever game of **"add and subtract"** through the transaction log:

1. **Updates**: Create new files with the updated records, mark old files as removed
2. **Deletes**: Mark files as removed without physically deleting them (until cleanup runs)
3. **Inserts**: Simply add new files and record them in the transaction log

This approach is like having a **time machine for your data** — you can always travel back to any previous version by replaying the transaction log up to that point!

**ACID Guarantees Through Atomic Commits**

The real genius of Delta Lake's design is how it achieves **ACID transactions** through atomic file operations. When you write to a Delta table, here's what happens behind the scenes:

1. **Write data files**: New Parquet files are written to the table directory
2. **Prepare transaction**: A JSON transaction file is prepared with all the changes
3. **Atomic commit**: The transaction file is atomically written to `_delta_log`
4. **Success or failure**: Either the entire transaction succeeds, or none of it does

It's like a bank transfer — either the money moves completely from one account to another, or the transaction fails entirely. No partial transfers, no inconsistent states, no sleepless nights wondering if your data is corrupted!

**Schema Evolution: Painless Progress**

One of Delta Lake's most delightful features is how it handles **schema evolution**. When you need to add a new column or change a data type, Delta Lake records these changes in the transaction log as **metadata actions**. Every subsequent read operation knows exactly how to interpret the data based on when it was written.

It's like having a universal translator that automatically adapts to new languages — your old data doesn't need to be rewritten, and your new data can use the updated schema seamlessly!

**Multi-Reader, Single-Writer (with Optimistic Concurrency)**

Delta Lake's transaction log enables **optimistic concurrency control** — multiple readers can safely access the table simultaneously, while writers coordinate through the atomic commit mechanism. If two writers try to modify the table at the same time, Delta Lake detects the conflict and asks one of them to retry with the latest state.

Think of it like a polite conversation where everyone takes turns speaking — no one talks over each other, but multiple people can listen at the same time!

This simple yet powerful architecture is what makes Delta Lake so reliable and easy to reason about. No complex metadata hierarchies, no distributed coordination nightmares — just a straightforward transaction log that keeps everything in perfect harmony.



## References

- [Apache Iceberg Copy-On-Write (COW) vs Merge-On-Read (MOR): A Deep Dive](https://estuary.dev/blog/apache-iceberg-cow-vs-mor/)
- [Exploring the Architecture of Apache Iceberg, Delta Lake, and Apache Hudi](https://www.dremio.com/blog/exploring-the-architecture-of-apache-iceberg-delta-lake-and-apache-hudi/)
- [Comparison of Data Lake Table Formats (Apache Iceberg, Apache Hudi and Delta Lake)](https://www.dremio.com/blog/comparison-of-data-lake-table-formats-apache-iceberg-apache-hudi-and-delta-lake/)
- [Table Format Governance and Community Contributions: Apache Iceberg, Apache Hudi, and Delta Lake](https://www.dremio.com/blog/table-format-governance-and-community-contributions-apache-iceberg-apache-hudi-and-delta-lake/)
- [Table Format Partitioning Comparison: Apache Iceberg, Apache Hudi, and Delta Lake](https://www.dremio.com/blog/table-format-partitioning-comparison-apache-iceberg-apache-hudi-and-delta-lake/)
- [Tampa Bay DE Meetup: The Who, What and Why of Data Lake Table Formats (Iceberg, Hudi, Delta Lake)](https://www.youtube.com/watch?v=1eEcWopaFqE)
- [Hudi vs Iceberg vs Delta Lake: Data Lake Table Formats Compared](https://lakefs.io/blog/hudi-iceberg-and-delta-lake-data-lake-table-formats-compared/)
- [What Is a Lakehouse?](https://www.databricks.com/blog/2020/01/30/what-is-a-data-lakehouse.html)