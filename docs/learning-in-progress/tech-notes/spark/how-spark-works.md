---
tags
  - Apache Spark
---

# How Apache Spark Works

<figure markdown="span">
  ![](https://spark.apache.org/docs/latest/img/cluster-overview.png)
  *Cluster Overview*
</figure>

## Architecture Components

### Driver Program

: The process running the `main()` function of the application and creating the `SparkContext`

### Cluster Manager

: An external service for acquiring resources on the cluster (e.g. standalone manager, YARN, Kubernetes)

### Worker Node

: Any node that can run application code in the cluster

### Executor

: A process launched for an application on a worker node, that runs tasks and keeps data in memory or disk storage across them. Each application has its own executors.

See [Cluster Mode Overview](https://spark.apache.org/docs/latest/cluster-overview.html) for more details on the architecture components.
