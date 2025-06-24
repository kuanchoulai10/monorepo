# Data

!! question "What are The Similarities and Differences Between Apache Spark and Apache Flink?"

    ??? tip "Answer"

        Apache Spark and Apache Flink are both powerful distributed data processing frameworks, but they have some key similarities and differences.

        In terms of **similarities**, both frameworks support batch and stream processing, and they both provide high-level APIs in multiple languages, like Java, Scala, and Python. They also focus on fault tolerance, scalability, and exactly-once processing semantics.

        When it comes to **differences**, One of the main differences is that **Flink is often considered to have a more native stream processing capability**, meaning it was designed from the ground up to handle real-time data streams with very low latency. Spark, on the other hand, started primarily as a batch processing framework and later introduced Structured Streaming, which provides micro-batch processing.
        
        This means that **while both can handle streaming data, Flink often achieves lower latency**.


!! question "What is Trigger Types in Apache Spark Structure Streaming"

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