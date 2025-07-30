# Iceberg Resources

## [Turbocharging Efficiency & Slashing Costs: Mastering Spark & Iceberg Joins with Storage-Partitioned](https://medium.com/expedia-group-tech/turbocharge-efficiency-slash-costs-mastering-spark-iceberg-joins-with-storage-partitioned-join-03fdc1ff75c0)

- Optimizing data pipelines has become synonymous with cost savings in cloud computing.
- Apache Spark and new table formats like Iceberg, Delta, and Hudi are improving how large datasets are managed.
- Expedia Group™ uses Spark and Iceberg to improve data processing workflows; storage-partitioned join (SPJ) is a feature that promises to greatly improve performance.
- Apache Iceberg is a high-performance table format for large analytics datasets that overcomes the limitations of Hive tables by providing features such as ACID transactions, schema evolution, partition evolution, and hidden partitioning.
- In distributed systems, non-broadcast joins are expensive operations due to data shuffling between nodes.
- Data shuffling involves significant network I/O and can drastically impact performance.
- Understanding Spark execution plans is essential for grasping performance.
- Sort-merge join is the default strategy for handling non-broadcasted joins in Spark.
- Iceberg sets write.spark.fanout.enabled to false by default, which forces a local sort before writing the data.
- Shuffle-hash join improves performance over sort-merge join by eliminating the CPU-intensive sorting steps.
- Storage-partitioned join (SPJ) removes 2 exchanges and 2 sorts.
- The storage-partitioned join is a new approach built on the concept of bucketed joins.
- Triggering SPJ requires the partition schema of the two joined Iceberg tables to be exactly the same and specific configurations to be applied.
- Scenarios tested are based on real-world data, with data size referring to deserialized data into memory.
- In Scenario 1, using a storage-partitioned join reduces the duration to just six minutes, with a cost of only $6.7, compared to 11 minutes and $12.2 for a sort-merge join.
- By combining three use cases, Expedia anticipates saving $5,000 for their next data pipeline.
- One of the most significant benefactors of the storage-partitioned join (SPJ) is the merge statement.
- SPJ is not applicable for non-equi-joins.
- Storage-partitioned joins, similar to the bucketed join, require both tables to follow the same partitioning schema, which can be challenging.


---

- [How We Migrated Our Data Lake to Apache Iceberg | Insider Engineering | Oct. 2022](https://medium.com/insiderengineering/how-we-migrated-our-production-data-lake-to-apache-iceberg-4d6892eca6e6)
- [Apache Iceberg Reduced Our Amazon S3 Cost by 90% | Insider Engineering | Sep. 2022](https://medium.com/insiderengineering/apache-iceberg-reduced-our-amazon-s3-cost-by-90-997cde5ce931)
- [Building a Feature Store with Apache Iceberg on AWS | Insider Engineering | Sep. 2023](https://medium.com/insiderengineering/building-a-feature-store-with-apache-iceberg-on-aws-8bfb98e3f5dc)
