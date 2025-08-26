---
tags:
  - Apache Airflow
---

# How Airflow Works?

[*Scheduler*](https://airflow.apache.org/docs/apache-airflow/3.0.0/administration-and-deployment/scheduler.html)

: handles both triggering scheduled workflows, and submitting Tasks to the executor to run. The [executor](https://airflow.apache.org/docs/apache-airflow/3.0.0/core-concepts/executor/index.html), is a configuration property of the scheduler, not a separate component and runs within the scheduler process. There are several executors available out of the box, and you can also write your own.


*Dag Processor*

: parses DAG files and serializes them into the metadata database


*Web Server*

: presents a handy user interface to inspect, trigger and debug the behaviour of dags and tasks.


*Metadata Database*

: Airflow components use to store state of workflows and tasks.


*Worker* (Optional)

: executes the tasks given to it by the scheduler.


*Triggerer* (Optional)

: executes deferred tasks in an asyncio event loop


[Architecture Overview](https://airflow.apache.org/docs/apache-airflow/3.0.0/core-concepts/overview.html)