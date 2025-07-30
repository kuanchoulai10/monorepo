---
tags:
  - The Data Lakehouse Series
  - Apache Iceberg
---

# [Apache Iceberg Best Practices in AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/apache-iceberg-on-aws/best-practices-general.html)

- Use Iceberg format version 2.
- Use the **AWS Glue Data Catalog** as your data catalog.
- Use the **AWS Glue Data Catalog** as lock manager.
- Use **Zstandard (ZSTD)** compression: you could configure `write.<file_type>.compression-codec` to `zstd` in your Iceberg table properties. It strikes a balance between **GZIP** and **Snappy**, and offers good read/write performance without compromising the compression ratio.

## [Optimizing Storage](https://docs.aws.amazon.com/prescriptive-guidance/latest/apache-iceberg-on-aws/best-practices-storage.html)

- Enable S3 Intelligent-Tiering
- Archive or delete historic snapshots
    - Delete old snapshots: [`expire_snapshots`](https://iceberg.apache.org/docs/latest/spark-procedures/#expire_snapshots)
    - Set retention policies for specific snapshots: use [Historical Tags](https://iceberg.apache.org/docs/latest/branching/#historical-tags) to mark specific snapshots and define a retention policy for them.
        ```sql
        ALTER TABLE glue_catalog.db.table
        CREATE TAG 'EOM-01' AS OF VERSION 30 RETAIN 365 DAYS
        ```

        ![](https://iceberg.apache.org/docs/latest/assets/images/historical-snapshot-tag.png)
    - Archive old snapshots:
        - [S3 Tags](https://iceberg.apache.org/docs/latest/aws/#s3-tags) + S3 Life cycle rules
            ```
            spark.sql.catalog.my_catalog.s3.{==write.tags==}.my_key1=my_val1
            spark.sql.catalog.my_catalog.s3.{==delete-enabled=false==}
            spark.sql.catalog.my_catalog.s3.{==delete.tags==}.my_key=to_archive
            spark.sql.catalog.my_catalog.s3.{==write.table-tag-enabled=true==}
            spark.sql.catalog.my_catalog.s3.{==write.namespace-tag-enabled=true==}
            ```
- Delete orphan files: [remove_orphan_files](https://iceberg.apache.org/docs/latest/spark-procedures/#remove_orphan_files)
- [`VACUUM` statement](https://docs.aws.amazon.com/athena/latest/ug/vacuum-statement.html): equals to `expire_snapshots` + `remove_orphan_files` in Spark.
    ```sql
    VACUUM glue_catalog.db.table
    ```

    ```sql
    CREATE TABLE your_table (
        ...
    )
    TBLPROPERTIES (
        'vacuum_max_snapshot_age_seconds' = '432000', -- 5 days
        'vacuum_min_snapshots_to_keep' = '1',
        'vacuum_max_metadata_files_to_keep' = '100'
    );
    ```

## References

- [General best practices | Using Apache Iceberg on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/apache-iceberg-on-aws/best-practices-general.html)