---
tags:
  - RisingWave
---

# RisingWave

![Overview](https://mintlify.s3.us-west-1.amazonaws.com/risingwavelabs/images/architecture_20250609.jpg)

## Execution Modes

- **Streaming**: RisingWave allows users to predefine SQL queries with `CREATE MATERIALIZED VIEW` statement. RisingWave continuously listens changes in upstream tables (in the `FROM` clause) and incrementally update the results automatically.
- **Ad-hoc**: Also like traditional databases, RisingWave allows users to send `SELECT` statement to query the result. At this point, RisingWave reads the data from the current snapshot, processes it, and returns the results.

![](https://mintlify.s3.us-west-1.amazonaws.com/risingwavelabs/images/stream_processing_vs_batch_processing.png)


- [Overview of data processing | RisingWave Docs](https://docs.risingwave.com/processing/overview#understanding-execution-modes)

## RisingWave vs. Apache Flink

![RisingWave vs. flink](risingwave-vs-flink.png)

> *For an easy **on-ramp to real-time processing**, RisingWave is an excellent choice. It offers a **simple**, **cost-efficient**, **SQL-based** solution that can be quickly deployed. This makes it ideal for data-driven businesses of any size that require real-time processing capabilities.*
> *Alternatively, if you require **low-level API** access that integrates seamlessly into your **JVM-based technical stack**, Apache Flink is the preferred option. Flink is well-suited for businesses with large teams that prefer building custom solutions tailored to their specific needs.*


![RisingWave vs. flink - Venn Diagram](https://mintlify.s3.us-west-1.amazonaws.com/risingwavelabs/images/current/risingwave-flink-comparison/RisingWave-vs-Flink.png)

![Without RisingWave](https://mintlify.s3.us-west-1.amazonaws.com/risingwavelabs/images/current/risingwave-flink-comparison/stream_processing_without_risingwave.jpeg)

![With RisingWave](https://mintlify.s3.us-west-1.amazonaws.com/risingwavelabs/images/current/risingwave-flink-comparison/stream_processing_with_risingwave.jpeg)

### Architecture

![Architecture](https://mintlify.s3.us-west-1.amazonaws.com/risingwavelabs/images/current/risingwave-flink-comparison/architecture_comparison.png)

- **Apache Flink** adopts a big-data style, **coupled-compute-storage architecture** that is optimized for **scalability**; 
- **RisingWave** in contrast implements a **cloud-native, decoupled compute-storage architecture** that is optimized for **cost efficiency**.


![Architecture Deep dive](https://mintlify.s3.us-west-1.amazonaws.com/risingwavelabs/images/rw-architecture-v2.png)

RisingWave comprises several key components:

- **Serving node**: handles user requests and is designed to be compatible with the PostgreSQL wire protocol, allowing tools like psql to connect seamlessly
- **Streaming node**: executes streaming queries. This involves managing their state and performing computations such as aggregations and joins.
- **Meta node**: manages cluster metadata by interacting with a meta store, which serves as the persistence layer for metadata. RisingWave supports Postgres, MySQL, and SQLite as meta store options. 
- **Compactor**: RisingWave employs a Log Structured Merge (LSM) Tree storage model, meaning that all data operations are handled in an append-only manner, even deletions are represented as tombstone records.

- [Architecture | RisingWave Docs](https://docs.risingwave.com/reference/architecture)
