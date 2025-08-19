# Learning Notes

--8<-- "./docs/disclaimer.md"

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0106.png)
/// caption
Each executor’s core gets a partition of data to work on
///

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0202.png)
/// caption
Each executor has 4 cores, each core gets a partition of data to work on
///

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0205.png)
/// caption
Spark Application DAG
///

**A Spark application is converted** by the driver **into one or more jobs** during execution, with **each job then transformed into a DAG as an execution plan**. **Nodes in the DAG are divided into different stages** based on whether operations can be executed serially or in parallel, with stage boundaries typically determined by computational boundaries that require data transfer between executors. **Each stage contains multiple tasks** that are distributed across executors for execution, where each task corresponds to a core and processes a data partition.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0207.png)
/// caption
Narrow vs. Wide Dependencies
///

Spark transformations fall into two categories based on their dependency patterns. **Narrow dependencies** occur when each output partition depends on data from only one input partition, making operations like `filter()` and `contains()` efficient to execute.

In contrast, **wide dependencies** require data shuffling across the cluster, as seen in operations like `groupBy()` or `orderBy()`, where multiple input partitions must be accessed to produce a single output partition, resulting in data being redistributed and persisted to storage.

## Ch 7 Optimizing and Tuning Spark Applications

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0702.png){width="500"}
/// caption
Executor memory layout
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
        - MEMORY_ONLY
        - MEMORY_ONLY_SER
        - MEMORY_AND_DISK
        - MEMORY_AND_DISK_SER
        - DISK_ONLY
        - OFF_HEAP
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