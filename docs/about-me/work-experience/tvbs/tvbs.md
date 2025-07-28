# Data Engineer, TVBS Media Inc.


??? note "Organization Diagram"

    ![](./assets/org.drawio.svg)

!!! abstract "Summary"

    - [x] Architected **a cost-effective, scalable ETL / ELT Modern Data Stack** (dbt, BigQuery, Airflow, Airbyte, Looker Studio, etc.) and introduced **a streamlined DataOps workflow**, processing **20M+** events daily at **TB+** scale (**300+** data models, **600+** daily quality checks), cutting cloud costs by **63%**.
    - [x] Directed **the organization-wide adoption of Data Mesh principles** to strengthen data governance and improve data availability, empowering **7 domain teams** through self-service reporting across **30+ data products**, and achieving a previously unattainable holistic brand analysis through the expansion of data sources from **4 to 9+**.
    - [x] Led **IaC implementation with Terraform** for over **500 cross-cloud data assets** (AWS, GCP, dbt Cloud, etc.) and conducted **internal DevOps workshops**, slashing provisioning lead time **from days to hours** by integrating **CI/CD pipelines** with GitHub Actions and improving team IaC adoption by **80% within 6 months**.
    - [x] Led **the migration to GA4 and BigQuery** to build a data lakehouse platform while maintaining a legacy event tracking pipeline (AWS Kinesis, MongoDB, PostgreSQL), **saving $2M** by retiring NoSQL database and **ensuring real-time analytics** for both anonymous and logged-in users.
    - [x] Championed **an organization-wide experimentation mindset**, **engaged 60+ colleagues**, and **orchestrated 20+ A/B tests** via Google Optimize and Firebase within 6 months, boosting **mobile ad revenue by 27%** and **web pageviews by 6%**.
    - [x] Built a **cross-account** data lake architecture using **AWS Glue, Athena, S3, and DMS** to power supplier analytics dashboards in a fast-paced **e-commerce** domain.

## Enabling Business-Friendly Access and Optimizing Access Control Through Customized dbt Project Configuration

### Problem Statement

By default, dbt creates all datasets in a single GCP project. This behavior does not meet our requirements due to the following reasons:

1. **Insufficient IAM isolation**: Managing all environments in one project increases the risk of permission misconfigurations.
2. **Resource conflicts**: Other GCP services used in BigQuery may conflict across environments if they share the same project.
3. **Unfriendly table naming for downstream users**: Final table names include technical prefixes like `fct` or `dim`, which may confuse non-technical users such as marketers or editors.

To address this, we customize dbt's behavior to:

- [x] Isolate each environment in its own GCP project.
- [x] Assign datasets by domain in staging and production.
- [x] Simplify final table names for easier consumption.

### Data Sink 

All raw data ingested through tools such as Airbyte, Fivetran, or custom data pipelines is initially landed in the `sink` project.

Datasets in this project are source-oriented, organized by their origin. For example, `food_ga4`, `app_store`, `google_play` etc.

This separation provides a clear boundary between raw source data and downstream transformations.

### Development Environment

- The GCP project used is the `dev` project.
- All models are deployed in the `dbt_dev` dataset in `dev` project.
- Model names **retain their original names**, such as `stg_*`, `int_*`, `fct_*`, `dim_*`.
- All models are configured to **expire after a certain duration** to reduce storage costs.

### Staging Environment

- The GCP project used is the `stg` project.
- All models are deployed in **datasets by domain** (e.g., `news`, `food`, `fashion`, etc.)
- Model names **retain their original names**, such as `stg_*`, `int_*`, `fct_*`, `dim_*`.
- All models are configured to **expire after a certain duration** to reduce storage costs.

### Production Environment

- The GCP project used is the `prod` project.
- **Final models** (data products) are deployed in **datasets by domain** (e.g., `news`, `food`, `fashion`, etc.). All its upstream models are deployed in the `hidden` dataset in the same project in order to encapsulate the implementation details.
- Model names **are simplified to aliases only**, without technical prefixes, to make them more user-friendly for non-technical stakeholders (e.g., **articles**, **app_installs**, **fb_summary_daily**).

### Implementation Summary

- Customize macros
    - [generate_database_name](https://docs.getdbt.com/docs/build/custom-databases)
    - [generate_schema_name](https://docs.getdbt.com/docs/build/custom-schemas)
    - [generate_alias_name](https://docs.getdbt.com/docs/build/custom-aliases)
- Use `if else` condition with `target.name` in `dbt_project.yml` to [dynamically configure settings based on the environment](https://docs.getdbt.com/reference/dbt-jinja-functions/target?utm_source=chatgpt.com#use-targetname-to-change-your-source-database).
    ```yml title="dbt_project.yml"
    models:
    custom_project_name:
        +materialized: view
        +hours_to_expiration: |
        {%- if target.name == "prod" -%} "{{ none }}"
        {%- else -%} 168
        {%- endif -%}
    ```

## Cost Optimization

- Partitioned tables
- Incremental model with [`insert_overwrite` strategy](https://docs.getdbt.com/reference/resource-configs/bigquery-configs#the-insert_overwrite-strategy): generates a `merge` statement that replaces entire partitions in the destination table.
    - [Static partition](https://docs.getdbt.com/reference/resource-configs/bigquery-configs#static-partitions)
        ```sql
        {% set partitions_to_replace = [
            'timestamp(current_date)',
            'timestamp(date_sub(current_date, interval 1 day))'
        ] %}

        {{
        config(
            materialized = 'incremental',
            incremental_strategy = 'insert_overwrite',
            partition_by = {
                'field': 'event_time',
                'data_type': 'timestamp',
                "granularity": "day"
            },
            partitions = partitions_to_replace
        )
        }}

        with events as (

            select * from {{ref('events')}}

            {% if is_incremental() %}
                -- recalculate yesterday + today
                where timestamp_trunc(event_timestamp, day) in ({{ partitions_to_replace | join(',') }})
            {% endif %}

        ),

        ... rest of model ...
        ```
    - [`on_schema_change`](https://docs.getdbt.com/docs/build/incremental-models): `append_new_columns`
- Materialized model as `table` if **the model is accessed multiple times** in the downstream models, to avoid recomputing the same data repeatedly.


## Data Mesh

- Domain-oriented Decentralized Data Ownership
    - work closely with
- Data Products
    - discoverable
    - addresable
    - trustworthy
    - interoperable
    - self-describing
    - secure
- Self-serve Data Platforms (Domain agnostic)
- Computational Data Governance

- From Medallion to DDD architecture 
- OWNERSHIP


## Tips

### 0 --> 1


[About Me :material-page-previous-outline:{ .lg .middle }](../../index.md){ .md-button }