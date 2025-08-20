---
tags:
  - Apache Spark
---

# Ch1 & 2 Introduction to Spark

--8<-- "./docs/disclaimer.md"

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0106.png){width="500"}
/// caption
Each executor's core gets a partition of data to work on
///

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0202.png){width="500"}
/// caption
Each executor has 4 cores, each core gets a partition of data to work on
///

**A Spark application is converted** by the driver **into one or more jobs** during execution, with **each job then transformed into a DAG as an execution plan**. **Nodes in the DAG are divided into different stages** based on whether operations can be executed serially or in parallel, with stage boundaries typically determined by computational boundaries that require data transfer between executors. **Each stage contains multiple tasks** that are distributed across executors for execution, where each task corresponds to a core and processes a data partition.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0205.png){width="500"}
/// caption
Spark Application DAG
///


Spark transformations fall into two categories based on their dependency patterns. **Narrow dependencies** occur when each output partition depends on data from only one input partition, making operations like `filter()` and `contains()` efficient to execute.

In contrast, **wide dependencies** require data shuffling across the cluster, as seen in operations like `groupBy()` or `orderBy()`, where multiple input partitions must be accessed to produce a single output partition, resulting in data being redistributed and persisted to storage.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0207.png){width="500"}
/// caption
Narrow vs. Wide Dependencies
///
