---
tags:
  - SQLMesh
  - dbt
---

# Comparisons: SQLMesh vs dbt Core

As dbt Labs announced that they are no longer maintain dbt core and move forward to dbt Fusion engine. Everyone started talking about sequel mash. Which is another. Analytics engineer engineering tools. Open source. 

And at the very beginning of. Second match launching. The CEO of Sidomesh, the founder of. Cyclone Mash. As always, roasted DBT for its functionalities. And how single match is better than DBT? And SQL, mash even support. Migrating from DBT projects to sqlmass project in a few clicks. Trying to attend DBT users to sqlmesh. 

So in this article I'm going to talk about. What are the features that Sigma? mesh? Has the DBT open source version doesn't have. And how you can benefit from them. 

- Virtual Data Environments
- Multi-engine Support
- Multi-project / Multi-repo Support
- Column-level Lineage and Smart Recalculation
- Plan Mechanism and Automatic Backfill Calculation
- Semantic / Metrics Layer
- Local Debuggable Python Models
- Built-in Scheduler

## Virtual Data Environments

Virtual Data Environments 是 SQLMesh 的核心創新，透過分離虛擬層與實體層來解決傳統資料環境管理的問題。每當模型發生變化時，SQLMesh 會自動建立新的模型快照（model snapshot），並為其分配基於指紋識別（fingerprint）的唯一表格，讓不同版本的同一模型可以同時存在而不互相衝突。

系統採用雙層架構：實體層（physical layer）儲存真實的table與view，而虛擬層（virtual layer）則透過view提供間接存取。下游消費者永遠不直接存取實體資料集，而是透過虛擬層的view，這讓 SQLMesh 能夠即時更新view指向不同的資料集版本，而不影響使用者。

SQLMesh 能夠自動偵測變更並進行分類，將直接修改分為「破壞性」（影響下游模型）或「非破壞性」（僅影響修改的模型本身）變更。透過語意層級的 SQL 分析，系統可計算語意差異並自動減少不必要的重算，確保正確性的同時達到最大效率。

建立新環境僅需要建立一組新的檢視，因此成本極低且幾乎即時。新環境立即擁有代表性資料（重用生產環境資料），無需複製資料或手動設定。當變更部署到生產環境時，也是透過虛擬層操作，確保開發環境觀察到的結果與生產環境完全一致。

這種設計帶來顯著優勢：環境建立成本低、資料立即可用、自動變更分類、即時回滾能力、以及生產部署時的資料與程式碼同步。相比 dbt 需要重建整套開發 schema 的方式，Virtual Data Environments 大幅降低運算與儲存成本，同時提供更安全可靠的開發體驗。

![Virtual Data Environments](https://cdn.prod.website-files.com/67f7cdf0feddc96ca194ff33/67f7cdf0feddc96ca195018d_virtual_envs_end_to_end.png)

*Snapshots*

: A snapshot is a record of a model at a given time. Along with a copy of the model, a snapshot contains everything needed (a copy of all macro definitions and global variables at the time the snapshot is taken) to evaluate the model and render its query. This allows SQLMesh to have a consistent view of your project's history and its data as the project and its models evolve and change. **Snapshots are generated automatically when a new `plan` is created and applied**.

*Fingerprinting*

: Snapshots have unique fingerprints that are derived from their models. SQLMesh uses these fingerprints to determine when existing tables can be reused, or whether a backfill is needed as a model's query has changed. No new fingerprint is generated when a model is modified only superficially, such as through query formatting.


- [Virtual Data Environments | SQLMesh Blog](https://www.tobikodata.com/blog/virtual-data-environments)
- [SQLMesh and virtual data environments | Medium](https://medium.com/%40foundinblank/sqlmesh-and-virtual-data-marts-3ee9b2d1e146)
- [Environments | SQLMesh Docs](https://sqlmesh.readthedocs.io/en/stable/concepts/environments/) 

## Multi-engine Support

同一個專案中不同模型可以使用不同查詢引擎（如同時用 Spark、DuckDB、Snowflake 等），降低 vendor lock‑in；dbt Core 一次只能對接單一 adapter。

In a multi-engine project with a shared data catalog, the model-specific gateway is responsible for the physical layer, while the default gateway is used for managing the virtual layer.



The data landscape continues to evolve, and one of the most significant paradigm shifts now taking place is the emergence of data lakes as the new architecture of choice for modern organizations. Recent developments, most notably AWS's integration with Apache Iceberg, underscore the growing momentum toward vendor neutrality and adoption of open standards.

interoperatibility

proliferration of data sources, types and applications

one project, multiple engines

So you can run individual models specific engines. 

how?

- the models you'll be running should reside in a shared data catalog, and
- for each engine you'll use, you must secure admin permissions to perform read/write operations on said shared catalog

![multi-engine config](https://cdn.prod.website-files.com/67f7cdf0feddc96ca194ff33/67f7cdf0feddc96ca1950182_config.png)

```yaml
gateways:
  duckdb:
    connection:
      type: duckdb
      catalogs:
        main_db:
          type: postgres
          path: 'dbname=main_db user=postgres host=127.0.0.1'
      extensions:
        - name: iceberg
  postgres:
    connection:
      type: postgres
      database: main_db
      user: user
      password: password
      host: 127.0.0.1
      port: 5432
default_gateway: postgres
```

- the PostgreSQL engine is set as the default gateway, so it will be used to manage views in your virtual layer.
- Meanwhile, DuckDB’s [`ATTACH`](https://duckdb.org/docs/stable/sql/statements/attach.html) feature enables read-write access to the PostgreSQL catalog’s physical tables.
- when a model’s gateway is explicitly set to DuckDb, it will be materialized within the PostgreSQL main_db catalog, but it will be evaluated using DuckDB’s engine.

![multi-engine query](https://cdn.prod.website-files.com/67f7cdf0feddc96ca194ff33/67f7cdf0feddc96ca1950181_model.png)

```sql
MODEL (
  name orders.order_ship_date,
  kind FULL,
  gateway duckdb,
);

SELECT
  l_orderkey,
  l_shipdate
FROM
  iceberg_scan('data/bucket/lineitem_iceberg', allow_moved_paths = true);
```

Given this configuration, when a model’s gateway is set to DuckDB, the DuckDB engine will perform the calculations before materializing the physical table in the PostgreSQL main_db catalog.



In the `order_ship_date` model, the DuckDB engine is set, which will be used to create the physical table in the PostgreSQL database. This allows you to efficiently scan data from an Iceberg table, or even query tables directly from S3 when used with the HTTPFS extension.

In this example, using both PostgreSQL and DuckDB in a single project offers the best of both worlds: PostgreSQL handles transactional workloads with its robust ACID compliance and relational capabilities, while DuckDB excels at fast, in-memory analytics on large datasets like CSV or Parquet files. Unlike PostgreSQL, which requires indexing to achieve optimal query performance, DuckDB will run complex analytical queries much faster without the need for such setup. This approach lets you leverage PostgreSQL’s versatility for transactional operations and DuckDB’s speed for analytics, applying the optimal engine to each model to streamline your workflow and maximize overall performance.

a view in the default gateway can access a table in another gateway

- shared virtual layer

![Multi-engine overview](https://cdn.prod.website-files.com/67f7cdf0feddc96ca194ff33/67f7cdf0feddc96ca1950180_overview.png)

The gateways denote the execution engine, while both the virtual layer’s views and the physical layer's tables reside in Postgres

- gateway-managed virtual layer

If your project's engines don’t have a mutually accessible catalog or your raw data is located in different engines, you may prefer for each model's virtual layer view to exist in the gateway that ran the model.

```yaml
gateways:
  redshift:
    connection:
      type: redshift
      user: <redshift_user>
      password: <redshift_password>
      host: <redshift_host>
      database: <redshift_database>
    variables:
      gw_var: 'redshift'
  athena:
    connection:
      type: athena
      aws_access_key_id: <athena_aws_access_key_id>
      aws_secret_access_key: <athena_aws_secret_access_key>
      s3_warehouse_location: <athena_s3_warehouse_location>
    variables:
      gw_var: 'athena'
  snowflake:
    connection:
      type: snowflake
      account: <snowflake_account>
      user: <snowflake_user>
      database: <snowflake_database>
      warehouse: <snowflake_warehouse>
    variables:
      gw_var: 'snowflake'

default_gateway: redshift
gateway_managed_virtual_layer: true

variables:
  gw_var: 'global'
  global_var: 5
```

![](https://sqlmesh.readthedocs.io/en/stable/guides/multi_engine/athena_redshift_snowflake.png)


- [SQLMesh sets a new precedent with support for multi-engine projects | SQLMesh Docs](https://www.tobikodata.com/blog/support-for-multi-engine-projects)
- [Multi-Engine guide | SQLMesh Docs](https://sqlmesh.readthedocs.io/en/stable/guides/multi_engine/)

## **Multi‑project / Multi‑repo

官方文件與社群均提到這是擴大量使用者與團隊協作的關鍵優勢。 ([sqlmesh.readthedocs.io][12], [Listed][13])

SQLMesh supports:

- SQLMesh repo + SQLMesh repo
- SQLMesh repo + dbt repo
- dbt repo + dbt repo

```yaml hl_lines="1"
project: repo_1

gateways:
...
```

- [Multi-Repo guide](https://sqlmesh.readthedocs.io/en/latest/guides/multi_repo/)

## Built-in Scheduler

SQLMesh 本身就提供內建的 cron 式排程與執行追蹤，不必再額外部署 Airflow / Dagster 等外部編排器；dbt Core 沒有內建排程。 ([sqlmesh.readthedocs.io][3], [Medium][4])



## 本地可除錯的 Python Models**

SQLMesh 的 Python model 在本地執行，對任何支援的資料庫都適用且可設 breakpoint；dbt 的 Python models 受限於具完整 Python runtime 的少數平台。 ([sqlmesh.readthedocs.io][7])


## Semantic / Metrics Layer

可用 `METRIC()` 定義可重用的商業指標；而 dbt Core 本身沒有內建 semantic layer（相關能力主要在 dbt Cloud）。 ([sqlmesh.readthedocs.io][8], [Datacoves][9])

## Plan 機制與自動 Backfill 計算

`sqlmesh plan` 會比對本地與目標環境差異，自動判斷哪些模型、哪些日期區間需要回填，讓你在執行前審閱所有變更。 ([sqlmesh.readthedocs.io][10], [sqlmesh.readthedocs.io][11])

## Column‑level Lineage 與智慧重算

SQLMesh 具備欄位等級血緣與狀態化執行，只重建受影響的下游模型，減少不必要的計算與等待時間。 ([Reddit][1], [tobikodata.com][2])

## Support WAP Pattern with Apache Iceberg

- [Introducing WAP Pattern Support with Apache Iceberg](https://www.tobikodata.com/blog/introducing-wap-pattern-support)

## Support Streaming Framworks

[Streamlining Real-Time Pipelines: Managing RisingWave with SQLMesh](https://www.tobikodata.com/blog/risingwave-sqlmesh-integration)





[Comparisons: SQLMesh vs. dbt Core](https://sqlmesh.readthedocs.io/en/stable/comparisons/)

[1]: [SQLMesh versus dbt Core - Seems like a no-brainer](https://www.reddit.com/r/dataengineering/comments/1j5bttx/sqlmesh_versus_dbt_core_seems_like_a_nobrainer/)
[2]: https://tobikodata.com/sqlmesh "SQLMesh • Open-source scalable & efficient data transformations"
[3]: https://sqlmesh.readthedocs.io/en/latest/guides/scheduling/ "Scheduling guide - SQLMesh"
[4]: https://tsaiprabhanj.medium.com/sqlmesh-and-dbt-3be5f8501787 "SQLMesh and DBT - Sai Prabhanj Turaga"
[5]: https://www.tobikodata.com/blog/support-for-multi-engine-projects "SQLMesh sets a new precedent with support for multi-engine projects"
[6]: https://sqlmesh.readthedocs.io/en/stable/guides/multi_engine/ "Multi-Engine guide - SQLMesh"
[7]: https://sqlmesh.readthedocs.io/en/stable/comparisons/ "Comparisons - SQLMesh"
[8]: https://sqlmesh.readthedocs.io/en/stable/concepts/metrics/definition/ "Definition - SQLMesh - Read the Docs"
[9]: https://datacoves.com/post/dbt-core-key-differences "dbt Core vs dbt Cloud – Key Differences as of 2025 - Datacoves"
[10]: https://sqlmesh.readthedocs.io/en/latest/concepts/plans/ "Plans - SQLMesh - Read the Docs"
[11]: https://sqlmesh.readthedocs.io/en/stable/concepts/overview/ "Overview - SQLMesh"
[12]: https://sqlmesh.readthedocs.io/en/latest/guides/multi_repo/ "Multi-Repo guide - SQLMesh"
[13]: https://listed.to/%40mattcarter/51660/initial-thoughts-on-sqlmesh "Initial Thoughts on SQLMesh | Matt Carter — This is my person..."
