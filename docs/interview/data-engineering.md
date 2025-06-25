# Data

## Apache Spark

!!! question "What are The Similarities and Differences Between Apache Spark and Apache Flink?"

    ??? tip "Answer"

        Apache Spark and Apache Flink are both powerful distributed data processing frameworks, but they have some key similarities and differences.

        In terms of **similarities**, both frameworks support batch and stream processing, and they both provide high-level APIs in multiple languages, like Java, Scala, and Python. They also focus on fault tolerance, scalability, and exactly-once processing semantics.

        When it comes to **differences**, One of the main differences is that **Flink is often considered to have a more native stream processing capability**, meaning it was designed from the ground up to handle real-time data streams with very low latency. Spark, on the other hand, started primarily as a batch processing framework and later introduced Structured Streaming, which provides micro-batch processing.
        
        This means that **while both can handle streaming data, Flink often achieves lower latency**.

!!! question "What is Trigger Types in Apache Spark Structure Streaming"

    ??? tip "Answer"

        In Apache Spark Structured Streaming, trigger types determine **how often the streaming query processes data and produces results**. There are a few different trigger types you can use:

        - **Default Trigger**: This is the default mode where Spark continuously processes data in **micro-batches** as soon as it arrives.
        - **Fixed Interval Trigger**: You can specify a fixed processing interval (for example, every 10 seconds). Spark will wait for that interval to pass before processing the next micro-batch.
        - **One-Time Trigger**: This trigger **processes all available data once and then stops**. It's useful for scenarios where you want to run a streaming job **as a batch job**.
        - **Continuous Trigger**: This is an **experimental** trigger where Spark processes data continuously **with very low latency**, though it's still in development


!!! question "What is Output Mode in Apache Spark Structured Streaming?"

    ??? tip "Answer"

        In Apache Spark Structured Streaming, the output mode basically defines **how the processed data is written to the output sink**. There are three main output modes:

        1. **Append Mode**: **Only the new rows that were added to the result table since the last trigger** are written to the sink. This is the default mode for most sinks.

        2. **Complete Mode**: **The entire updated result table** is written to the sink every time there's a trigger. This mode is useful for aggregations where you want to keep updating the whole result.

        3. **Update Mode**: **Only the rows that were updated since the last trigger** are written to the sink. This is kind of a middle ground between Append and Complete modes.


!!! question "What is Watermarking in Apache Spark Structured Streaming?"

    ??? tip "Answer"

        Watermarking in Apache Spark Structured Streaming is **a way to handle late data** in event-time based processing. Essentially, it allows you to define how late data can arrive and still be considered for processing. You set a watermark on an event-time column, and Spark will use that to **manage state and clean up old data**, ensuring that the system doesn't hold onto too much state for too long. It's really useful for managing streaming data efficiently.


!!! question "What is Time Window in Apache Spark Structured Streaming?"

    ??? tip "Answer"


## Apache Kafka

!!! question "What is Apache Kafka?"

    ??? tip "Answer"

        Apache Kafka is an open-source distributed event streaming platform. It's designed to handle real-time data feeds, allowing you to publish, subscribe to, store, and process streams of records in a **fault-tolerant** way. It's often used for building **real-time data pipelines**, **streaming applications**, and **event-driven architectures**. It was originally developed by LinkedIn and later became part of the Apache Software Foundation.


!!! question "What's the difference between Apache Kafka and the Message Queue?"

    ??? tip "Answer"

        Apache Kafka and traditional message queues, like RabbitMQ, both deal with messaging, but they have different architectures and use cases.
        
        Kafka is designed for high-throughput, distributed event streaming and can handle huge volumes of data with fault tolerance and scalability in mind. It uses a distributed log as its storage layer, which allows it to retain messages for a configurable amount of time, making it great for reprocessing and long-term storage of events.
        
        Traditional message queues, on the other hand, are usually designed for simpler point-to-point or pub-sub scenarios with a focus on delivering messages to consumers as quickly as possible, and they might not have the same level of built-in storage or scalability as Kafka.


## Data Lakehouse

!!! question "What is Apache Iceberg?"

    ??? tip "Answer"

        Apache Iceberg is a high-performance Data Lakehouse table format designed for huge analytic datasets. It was originally developed by Netflix and later became an open-source Apache project. It supports features like **schema evolution**, **hidden partitioning**, and **time travel**, making it easier to manage large datasets efficiently!

        one cool feature of Apache Iceberg is **schema evolution**, which allows you to change your table's schema—like adding or renaming columns—without having to rewrite or recreate the table.
        
        Another feature is **hidden partitioning**, which means you can partition your data without having to expose those partitions in your query logic, making queries simpler and faster. Iceberg also supports **partition evolution** through hidden partitioning, which decouples logical columns from physical layout by tracking partition transforms in metadata.
        
        And then there's **time travel**, which lets you query historical versions of your data, so you can basically go back in time and see what the data looked like at any previous point.  A really common use case for time travel is data auditing and debugging.
        
        It's all about making data management a lot more flexible and efficient! 

