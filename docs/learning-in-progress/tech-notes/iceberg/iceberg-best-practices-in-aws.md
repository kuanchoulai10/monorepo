---
tags:
  - The Lakehouse Series
  - Apache Iceberg
---
# [Best Practices for Optimizing Apache Iceberg Workloads in AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/apache-iceberg-on-aws/best-practices.html)

## [General Best Practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/apache-iceberg-on-aws/best-practices-general.html)

!!! tip

    - [x] Use Iceberg format **version 2**.
    - [x] Use the **AWS Glue Data Catalog** as your data catalog.
    - [x] Use the **AWS Glue Data Catalog** as lock manager.
    - [x] Use **Zstandard (ZSTD)** compression

## [Optimizing Storage](https://docs.aws.amazon.com/prescriptive-guidance/latest/apache-iceberg-on-aws/best-practices-storage.html)

!!! tip

    - [x] Enable **S3 Intelligent-Tiering**
    - [x] **Archive or delete historic snapshots**
        - Delete old snapshots: [`expire_snapshots`](https://iceberg.apache.org/docs/latest/spark-procedures/#expire_snapshots)
        - Set **retention policies** for specific snapshots: use [Historical Tags](https://iceberg.apache.org/docs/latest/branching/#historical-tags)
        - Archive old snapshots: [S3 Tags](https://iceberg.apache.org/docs/latest/aws/#s3-tags) + S3 Life cycle rules
    - [x] **Delete orphan files**
        - [`remove_orphan_files`](https://iceberg.apache.org/docs/latest/spark-procedures/#remove_orphan_files)
        - [`VACUUM` statement](https://docs.aws.amazon.com/athena/latest/ug/vacuum-statement.html): equals to `expire_snapshots` + `remove_orphan_files` in Spark.


#### [Historical Tags](https://iceberg.apache.org/docs/latest/branching/#historical-tags)

to mark specific snapshots and define a retention policy for them.

```sql
ALTER TABLE glue_catalog.db.table
CREATE TAG 'EOM-01' AS OF VERSION 30 RETAIN 365 DAYS
```

![](https://iceberg.apache.org/docs/latest/assets/images/historical-snapshot-tag.png){width="500"}
/// caption
Historical Snapshot Tag
///

#### [S3 Tags](https://iceberg.apache.org/docs/latest/aws/#s3-tags)

```
spark.sql.catalog.my_catalog.s3.{==write.tags==}.my_key1=my_val1
spark.sql.catalog.my_catalog.s3.{==delete-enabled=false==}
spark.sql.catalog.my_catalog.s3.{==delete.tags==}.my_key=to_archive
spark.sql.catalog.my_catalog.s3.{==write.table-tag-enabled=true==}
spark.sql.catalog.my_catalog.s3.{==write.namespace-tag-enabled=true==}
```

#### [`VACUUM` statement](https://docs.aws.amazon.com/athena/latest/ug/vacuum-statement.html)

```sql
CREATE TABLE my_table (
    ...
)
TBLPROPERTIES (
    'vacuum_max_snapshot_age_seconds' = '432000', -- 5 days
    'vacuum_min_snapshots_to_keep' = '1',
    'vacuum_max_metadata_files_to_keep' = '100'
);
```

```sql
VACUUM glue_catalog.db.my_table
```

## [Optimizing Read Performance](https://docs.aws.amazon.com/prescriptive-guidance/latest/apache-iceberg-on-aws/best-practices-read.html)

!!! tip

    - [x] Partitioning
        - Partition your data
            - Identify columns that are frequently used in queries
            - Choose a low cardinality partition column to avoid creating an excessive number of partitions
        - Use [Hidden Partitioning](https://iceberg.apache.org/docs/latest/partitioning/#icebergs-hidden-partitioning)
        - Use [Partition Evolution](https://iceberg.apache.org/docs/latest/evolution/#partition-evolution)
    - [x] Tuning File Size
        - Set target file size and row group size: `write.target-file-size-bytes`, `write.parquet.row-group-size-bytes`, `write.distribution-mode`
        - Run regular compaction
    - [x] Optimize Column Statistics
        - `write.metadata.metrics.max-inferred-column-defaults`: `100`
    - [x] Choose the Right Update Strategy (CoR)
        - `write.update.mode`, `write.delete.mode`, and `write.merge.mode` can be set at the **table level** or independently on the **application side**.
    - [x] Use ZSTD Compression
        - `write.<file_type>.compression-codec`
    - [x] Set the Sort Order
        - [`ALTER TABLE ... WRITE ORDERED BY`](https://iceberg.apache.org/docs/latest/spark-ddl/#alter-table-write-ordered-by)
        - [`ALTER TABLE ... WRITE DISTRIBUTED BY PARTITION`](https://iceberg.apache.org/docs/latest/spark-ddl/#alter-table-write-distributed-by-partition)
        - `ALTER TABLE prod.db.sample WRITE DISTRIBUTED BY PARTITION LOCALLY ORDERED BY category, id`


- As a rule of thumb, "too many partitions" can be defined as a scenario where *the data size in the majority of partitions* is **less than 2-5 times** *the value set by `target-file-size-bytes`*.

## [Optimizing Write Performance](https://docs.aws.amazon.com/prescriptive-guidance/latest/apache-iceberg-on-aws/best-practices-write.html)

!!! tip

    - [x] Set the Table Distribution Mode
        - [`write.distribution-mode`](https://iceberg.apache.org/docs/latest/spark-writes/#writing-distribution-modes): `none`, `hash`, `range`
        - Spark Structured Streaming applications --> `set write.distribution-mode` to `none`.
    - [x] Choose the Right Update Strategy (MoR)
    - [x] Choose the Right File Format
        - Set `write-format` to **Avro** (row-based format) if **write speed** is important for your workload.

- By default, Iceberg's compaction **doesn't merge delete files** unless you change the default of the `delete-file-threshold property` to a **smaller** value.