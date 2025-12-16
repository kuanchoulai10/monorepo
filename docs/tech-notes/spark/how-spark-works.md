---
tags:
  - Apache Spark
  - How It Works
---

# How Spark Works

![](https://spark.apache.org/docs/latest/img/cluster-overview.png){width="500"}
/// caption
[Cluster Overview](https://spark.apache.org/docs/latest/cluster-overview.html)
///

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

## [Kubeflow Spark Operator](https://www.kubeflow.org/docs/components/spark-operator/overview/)

When [Spark 2.3 introduced Kubernetes](https://spark.apache.org/docs/latest/running-on-kubernetes.html) as an official scheduler backend, it created challenges in managing Spark application lifecycles on Kubernetes. Unlike traditional workloads such as Deployments and StatefulSets, Spark applications required different approaches for submission, execution, and monitoring, making them difficult to manage idiomatically within Kubernetes environments.

The [Kubeflow Spark Operator](https://www.kubeflow.org/docs/components/spark-operator/overview/) addresses these challenges by implementing **the operator pattern to manage Spark applications declaratively**. It allows users to specify Spark applications in YAML files without dealing with complex `spark-submit` processes, while **providing native Kubernetes-style status tracking and monitoring capabilities that align with other Kubernetes workloads**.

![](https://www.kubeflow.org/docs/components/spark-operator/overview/architecture-diagram.png){width="500"}
/// caption
[Architecture diagram of the Kubeflow Spark Operator](https://www.kubeflow.org/docs/components/spark-operator/overview/#architecture)
///

## Spark Connect

Introduced in Spark 3.4, [Spark Connect](https://spark.apache.org/docs/latest/spark-connect-overview.html),  decoupled client-server architecture that allows remote connectivity to Spark clusters using the DataFrame API and unresolved logical plans as the protocol

![](https://spark.apache.org/docs/latest/img/spark-connect-api.png){width="500"}
/// caption
[The Spark Connect API is a language-agnostic protocol](https://spark.apache.org/docs/latest/spark-connect-overview.html#spark-connect-overview)
///

![](https://spark.apache.org/docs/latest/img/spark-connect-communication.png){width="500"}
/// caption
[How Spark Connect Works](https://spark.apache.org/docs/latest/spark-connect-overview.html#how-spark-connect-works)
///