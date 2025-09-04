---
authors:
  - kuanchoulai10
date:
  created: 2025-08-14
  updated: 2025-08-14
categories:
  - Data
tags:
  - Apache Airflow
links:
  - Apache Airflow(r) 3 is Generally Available!: https://airflow.apache.org/blog/airflow-three-point-oh-is-here/
  - Introducing Apache Airflow(r) 3 - the most significant release in Airflow's history: https://www.astronomer.io/airflow/3-0/intro/
  - Apache Airflow(r) 3.0 Is Here - The Most Significant Release Yet: https://www.datacamp.com/blog/apache-airflow-3-0
comments: true
---
# What's New in Apache Airflow 3

<!-- more -->

Apache Airflow 3 was officially released in April 2025, marking one of the most significant updates in Airflow's history. This release introduces numerous new features and improvements aimed at enhancing developer experience and system performance. Let's dive into these exciting updates.

## The New User Interface

<iframe width="560" height="315" src="https://www.youtube.com/embed/JLmyGodTC9s?si=rziw9v-aSQFkWo4p" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

One of the most striking changes in Airflow 3 is the completely revamped user interface. Now built with React, the UI boasts a modern design, including native support for dark mode and seamless integration with Airflow 3's new asset concept. These updates not only improve usability but also provide a more visually appealing experience.

To begin with, Airflow 3 introduces a brand-new **Home Page**, which replaces the DAG List View as the default landing page. The Home Page now features health indicators that allow users to monitor the status of Airflow system components at a glance. Additionally, it provides quick access to Failed, Running, and Active DAGs, as well as execution statistics for DAGs and tasks over specific time intervals.

<figure markdown="span">
  ![](https://airflow.apache.org/docs/apache-airflow/3.0.0/_images/home_dark.png)
  *Home Page in Airflow 3*
</figure>

Moving on to the **DAG List View**, Airflow 3 replaces the circular indicators from Airflow 2 with visual bar charts that summarize recent run outcomes. These charts use color to represent success or failure and bar length to indicate execution time, making it easier for users to quickly understand the status of recent runs.

<figure markdown="span">
  ![](https://airflow.apache.org/docs/apache-airflow/2.11.0/_images/dags.png)
  *DAG List View in Airflow 2*
</figure>

<figure markdown="span">
  ![](https://airflow.apache.org/docs/apache-airflow/3.0.0/_images/dag_list.png)
  *DAG List View in Airflow 3*
</figure>

The **DAG Details Page** has also undergone significant improvements. In Airflow 2, the page was cluttered with excessive colors and text, and the Grid View and Graph View were displayed in separate sections, making it difficult to view detailed information alongside the graph. 

Airflow 3 addresses these issues by integrating the Grid View and Graph View into a single left-side panel. This allows users to simultaneously view detailed information about DAG runs while exploring the grid or graph. The interface has also been simplified, removing unnecessary elements to help users focus on execution details.

<figure markdown="span">
  ![](https://airflow.apache.org/docs/apache-airflow/2.11.0/_images/grid.png)
  *DAG Details Page in Airflow 2*
</figure>

<figure markdown="span">
  ![](https://airflow.apache.org/docs/apache-airflow/3.0.0/_images/dag_overview_dashboard.png)
  *DAG Details Page in Airflow 3*
</figure>

<figure markdown="span">
  ![](https://airflow.apache.org/docs/apache-airflow/3.0.0/_images/dag_overview_graph.png)
  *Graph View in DAG Details Page in Airflow 3*
</figure>

Furthermore, Airflow 3 enhances the DAG Run View by allowing users to inspect task instance details while simultaneously viewing the Grid or Graph View. Users can even switch between these views to better understand task execution statuses in a graphical format.

<figure markdown="span">
  ![](https://airflow.apache.org/docs/apache-airflow/stable/_images/dag_run_task_instances.png)
  *DAG Run View in Airflow 3*
</figure>

<figure markdown="span">
  ![](https://airflow.apache.org/docs/apache-airflow/3.0.0/_images/dag_task_instance_logs.png)
  *Task Instance View in Airflow 3*
</figure>

In previous versions, Airflow 2 introduced the concept of Datasets, which allowed users to track the flow of data between different DAGs. This was a significant step towards understanding data lineage and dependencies. However, with the release of Airflow 3, the Dataset feature has been upgraded and rebranded as the **Asset** concept, providing a more comprehensive and flexible approach to data and task management.

The new **Asset List View** offers a global overview of all known assets, organizing them by name and displaying which tasks produce them and which DAGs consume them. This clear organization helps users quickly understand the relationships and dependencies between different assets across the platform.

<figure markdown="span">
  ![](https://airflow.apache.org/docs/apache-airflow/2.11.0/_images/datasets.png)
  *Datasets List View in Airflow 2*
</figure>

<figure markdown="span">
  ![](https://airflow.apache.org/docs/apache-airflow/3.0.0/_images/asset_list_consuming_dags.png)
  *Asset List View in Airflow 3*
</figure>

The **Asset Graph View** takes this a step further by providing a contextual map of an asset's lineage. Users can explore upstream producers and downstream consumers of an asset, trigger asset events manually, and inspect recent asset events and the DAG runs they initiated. This comprehensive view offers deep insights into data flow and dependencies.

<figure markdown="span">
  ![](https://airflow.apache.org/docs/apache-airflow/3.0.0/_images/asset_view.png)
  *Asset Graph View in Airflow 3*
</figure>

Finally, when working within a DAG, the **DAG Graph View with Asset Overlays** integrates asset awareness directly into the task dependency graph. This means users can visualize how assets flow between DAGs and uncover asset-triggered dependencies, all within the familiar DAG graph view. This seamless integration completes the picture of how data moves throughout workflows, from task-level execution to broader asset relationships.

<figure markdown="span">
  ![](https://airflow.apache.org/docs/apache-airflow/3.0.0/_images/dag_graph_all_dependencies.png)
  *Graph Overlays in DAG Graph View in Airflow 3*
</figure>

The reimagined Asset system in Airflow 3 provides users with powerful tools to manage and understand their data workflows better than ever before.

## Architecture Changes and Task Isolation

<iframe width="560" height="315" src="https://www.youtube.com/embed/3TDnR_iwUcU?si=Uu82qO_RM5L9JQJc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

In **Airflow 2**, every system component, including the Scheduler, Workers, Webserver, and CLI, could directly communicate with the Metadata Database. This design had a clear advantage: it was **simple** and **straightforward**. **All components coordinated through a single source of truth, ensuring strong consistency across the system**. The **Scheduler** could write task states directly, **Workers** could report results immediately, and the **Webserver** could display the most up-to-date DAG and task information. As a result, users only needed to maintain one reliable database to keep the entire system running smoothly.

However, this architecture also introduced several challenges. Since all components relied on the same **database**, it could quickly become a **performance bottleneck** as the number of DAGs and tasks grew. Under high concurrency, **competition for database locks between Schedulers and Workers could lead to delays or even deadlocks**. In addition, **task code had the ability to access the database directly, which reduced isolation and increased the risk of bugs or malicious code affecting the entire system**. Finally, the tight coupling between the database schema and all components made upgrades more difficult and increased operational costs, while also limiting observability and extensibility.

With **Airflow 3**, these issues were addressed through the introduction of **a dedicated API Server**. Instead of allowing components to connect to the Metadata Database directly, **all interactions now flow through the API Server**. This reduces the load on the database, prevents lock contention, and improves system scalability. It also strengthens **security by ensuring that task code can no longer modify the core database directly**, thereby improving isolation. At the same time, the new API Server, built on **FastAPI**, delivers higher performance and more consistent interfaces. It also enables new capabilities such as the **Task Execution API** and **multi-language SDKs**. Overall, Airflow 3's API Server resolves the bottlenecks and risks present in the earlier architecture while laying the foundation for a more modern and extensible system.

<figure markdown="span">
  ![](https://www.astronomer.io/images/Fig%205.1_original.jpg)
  *Source: [Astronomer](https://www.astronomer.io/airflow/3-0/intro/)*
</figure>

## Remote Execution

<iframe width="560" height="315" src="https://www.youtube.com/embed/RypyFfKBPAQ?si=2pXDK1Frg4QQlbUV" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

One of the most important innovations in Airflow 3.0 is the introduction of a Task Execution API and an accompanying [Task SDK](https://airflow.apache.org/docs/task-sdk/stable/examples.html#). 

These components enable tasks to be defined and executed independently of Airflow’s core runtime engine.

Environment decoupling: Tasks can now run in isolated, remote, or containerized environments, separate from the scheduler and workers

[Edge Executor](https://airflow.apache.org/docs/apache-airflow-providers-edge3/stable/edge_executor.html)

[Why using Edge Worker?](https://airflow.apache.org/docs/apache-airflow-providers-edge3/stable/why_edge.html) The Edge Worker is a execution option that allows you to run Airflow tasks on edge devices. The Edge Worker is designed to be lightweight and easy to deploy. 

[apache-airflow-providers-edge3](https://airflow.apache.org/docs/apache-airflow-providers-edge3/stable/index.html)

## DAG Versioning

<iframe width="560" height="315" src="https://www.youtube.com/embed/Ax25ZRxuSEA?si=7M_Sd36Sej43BHiC" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

[DAG Bundle](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/dag-bundles.html)

## Backfills

<iframe width="560" height="315" src="https://www.youtube.com/embed/_1sIZg8a4Ic?si=AEZ1ILcESHDszRKZ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Assets

<iframe width="560" height="315" src="https://www.youtube.com/embed/gZhmMUDFUDA?si=rls00mA7TA_ItilG" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


## Event Driven Scheduling, Inference Execution

<iframe width="560" height="315" src="https://www.youtube.com/embed/Q0wEnd3rrws?si=33hFP7RkTKvvSfLA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<iframe width="560" height="315" src="https://www.youtube.com/embed/xgX5i7gMxqo?si=DhefS-Xe7lcZUrSD" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

[AIP-83](https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-83+Rename+execution_date+-%3E+logical_date+and+make+logical_date+optional)