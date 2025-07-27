# Treasure Data

## Metrics

In 2023, Treasure Data currently serves over **700 accounts** and **more than 6,000 users**. Since 2022, platform usage has doubled. Each day, the system handles **2.5 million+ Trino queries** and over **100,000 Hive queries**. It processes more than **200 trillion rows daily** and **performs over 10 billion S3 GET requests per day to read partition data from AWS S3**.



## Tech Stack

- Trino
- Hive 4 ([Hive 4.0.x comes with Iceberg 1.4.3 included.](https://iceberg.apache.org/docs/latest/hive/#feature-support))
- Plazma (Closed Source)
    - PostgreSQL (metadata)
    - S3
        - Real-time Storage
        - Archive Storage
- [fluentd](https://github.com/fluent/fluentd)
- [embulk](https://github.com/embulk/embulk): [Data Connector and Result Export](https://api-docs.treasuredata.com/blog/embulk-in-td/)

![Hive Table scan optimization](https://api-docs.treasuredata.com/static/f28b686ba570ef76e5e4598f687a8131/c6bbc/plazma-architecture.png)

![Data Architecture 2021](data-architecture-2021.png)


## Data Ingestion

- [Google Analytics Data API Import Integration](https://docs.treasuredata.com/articles/#!int/Google-Analytics-Data-API-Import-Integration)


## Questions

- Data Lakehouse Architecture? proprietary ([MPC1](https://api-docs.treasuredata.com/blog/hive-table-scan-optimization/))
- [dbt Fusion](https://www.getdbt.com/blog/new-code-new-license-understanding-the-new-license-for-the-dbt-fusion-engine)


<figure markdown="span">
  ![](https://www.treasuredata.com/wp-content/uploads/2024/12/TD-on-TD-Implementation.png){width="600"}
  [*How Treasure Data reduced ad spend and increased marketing ROI by 20%*](https://www.treasuredata.com/customers/treasure-data/)
</figure>


<figure markdown="span">
  ![Data Architecture in Treasure Data at Trino Summit 2023](./assets/architecture.png)
  [*Secure exchange SQL - Treasure Data at Trino Summit 2023*](https://www.youtube.com/watch?v=FaytoXxKXOQ)
</figure>

<figure markdown="span">
  ![CDP Intro 2022](./assets/cdp-intro-2022.png)
  [*Treasure Data Enterprise Customer Data Platform | Demo*](https://www.youtube.com/watch?v=B_UPLEtM2SE)
</figure>

<figure markdown="span">
  ![Hightouch](pros-and-cons.png)
  [*What is Treasure Data CDP?*](https://hightouch.com/blog/what-is-treasure-data-cdp)
</figure>

<figure markdown="span">
  ![](https://www.treasuredata.com/wp-content/uploads/2024/11/live-connect-diagram-ia.svg)
  [Zero-Copy Integrations Between Your CDP and Data Warehouse](https://www.treasuredata.com/product/zero-copy/)
</figure>
## Profiles

## Resources

https://trino.io/blog/2019/07/11/report-for-presto-conference-tokyo.html