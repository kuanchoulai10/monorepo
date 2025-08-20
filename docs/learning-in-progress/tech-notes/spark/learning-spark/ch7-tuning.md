---
tags:
  - Apache Spark
---

# Ch7 Optimizing and Tuning Spark Applications

--8<-- "./docs/disclaimer.md"

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0702.png){width="500"}
/// caption
Executor Memory Layout
///

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0706.png){width="500"}
/// caption
Broadcast Hash Join
///

- Optimizing and Tuning for Efficiency
    - Viewing and Setting Apache Spark Configurations
        - 3 ways to specify Spark configurations
            - configuration files
            - spark-submit conf
            - programmatically interface via the spark shell
    - Scaling Spark for Large Workloads
        - [ ] dynamic resouce allocation
        - [ ] executors' memory
        - [ ] executors' shuffle service
        - [ ] maximizing spark parallelism
            - `spark.sql.shuffle.partitions` 200 by default, reduce 
- Caching and Persistence of Data
    - DataFrame.cache()
    - DataFrame.persist()
        - `MEMORY_ONLY`
        - `MEMORY_ONLY_SER`
        - `MEMORY_AND_DISK`
        - `MEMORY_AND_DISK_SER`
        - `DISK_ONLY`
        - `OFF_HEAP`
    - When to Cache and Persist
        - Iterative ML training
        - DataFrames accessed commonly
    - When not to Cache and Persist
        - Too big to fit in memory

- A Family of Spark Joins
    - Broadcast Joins
    - Shuffle Sort-Merge Joins
        - When each key within two large data sets can be sorted and hashed to the same partition by Spark
        - When you want to perform only equi-joins to combine two data sets based on matching sorted keys
        - When you want to prevent Exchange and Sort operations to save large shuffles across the network

- Inspecting the Spark UI

[Join Strategies](https://github.com/apache/spark/blob/master/sql/core/src/main/scala/org/apache/spark/sql/execution/SparkStrategies.scala#L145)
