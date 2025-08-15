---
tags
  - Apache Flink
---

# How Flink Works

<figure markdown="span">
  ![](https://nightlies.apache.org/flink/flink-docs-release-2.1/fig/learn-flink/flink-application-sources-sinks.png)
  Source: [Flink Documentation](https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/learn-flink/overview/#stream-processing)
</figure>


<figure markdown="span">
  ![](https://nightlies.apache.org/flink/flink-docs-release-2.1/fig/distributed-runtime.svg)
  Source: [Flink Documentation](https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/learn-flink/datastream_api/#stream-execution-environment)
</figure>



## Architecture Components

<figure markdown="span">
  ![](https://nightlies.apache.org/flink/flink-docs-release-2.1/fig/processes.svg)
  [*Anatomy of a Flink Cluster*](https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/concepts/flink-architecture/#anatomy-of-a-flink-cluster)
</figure>

### JobManager

coordinating the distributed execution of Flink Applications

- ResourceManager
- Dispatcher
- JobMaster

### TaskManager

- Task Slot
- For distributed execution, Flink chains operator subtasks together into
tasks. Chaining operators together into

- Each task is executed by one thread

## Tasks and Operators chains

- Flink chains operator subtasks together into tasks.
- Chaining operators together into tasks is a useful optimization: it reduces the overhead of thread-to-thread handover and buffering, and increases overall throughput while decreasing latency.


<figure markdown="span">
  ![](https://nightlies.apache.org/flink/flink-docs-release-2.1/fig/tasks_chains.svg)
  Source: [Flink Documentation](https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/concepts/flink-architecture/#tasks-and-operator-chains)
</figure>


## Task Slots and Resources

- Note that no CPU isolation happens here; currently slots only separate the managed memory of tasks.
- By adjusting the number of task slots, users can define how subtasks are isolated from each other. 
- Having **one** slot per TaskManager means that **each task group runs in a separate JVM** (which can be started in a separate container, for example).
- Having **multiple** slots means **more subtasks share the same JVM**. Tasks in the same JVM share TCP connections (via multiplexing) and heartbeat messages. They may also share data sets and data structures, thus **reducing the per-task overhead**.


<figure markdown="span">
  ![](https://nightlies.apache.org/flink/flink-docs-release-2.1/fig/tasks_slots.svg)
  Source: [*Flink Documentation*](https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/concepts/flink-architecture/#task-slots-and-resources)
</figure>

- By default, **Flink allows subtasks to share slots** even if they are subtasks of different tasks, so long as **they are from the same job**. 
- 2 benefits
    - A Flink cluster needs exactly as many task slots as the highest parallelism used in the job.
    - It is easier to get better resource utilization.

## Streaming Processing

![Streaming Processing](https://nightlies.apache.org/flink/flink-docs-release-2.1/fig/learn-flink/bounded-unbounded.png)

![Program to Dataflow](https://nightlies.apache.org/flink/flink-docs-release-2.1/fig/learn-flink/program_dataflow.svg)

![](https://nightlies.apache.org/flink/flink-docs-release-2.1/fig/learn-flink/parallel_dataflow.svg)


<figure markdown="span">
  ![](https://nightlies.apache.org/flink/flink-docs-release-2.1/fig/slot_sharing.svg)
  Source: [*Flink Documentation*](https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/concepts/flink-architecture/#task-slots-and-resources)
</figure>

![](https://nightlies.apache.org/flink/flink-docs-release-2.1/fig/learn-flink/parallel-job.png)

## Flink Application Execution

- Flink Application Cluster
- Flink Session Cluster



## [APIs](https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/concepts/overview/)

<figure markdown="span">
  ![](https://nightlies.apache.org/flink/flink-docs-release-2.1/fig/concepts/levels_of_abstraction.svg)
  [*Flink APIs*](https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/concepts/overview/#flinks-apis)
</figure>
From high to low level:

- SQL: High-level Language
- Table API: Declarative DSL
- DataStream API: Core API
- Stateful and timely stream processing: building blocks, 透過DataStream API的Process Function來使用