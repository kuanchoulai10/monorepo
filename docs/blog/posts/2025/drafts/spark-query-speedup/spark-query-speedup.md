---
authors:
  - kuanchoulai10
date:
  created: 2025-08-07
  updated: 2025-08-07
categories:
  - Data
tags:
  - Apache Spark
links:
  - 7 pillars of Apache Spark performance tuning: https://www.instaclustr.com/education/apache-spark/7-pillars-of-apache-spark-performance-tuning/
  - How Spark Works: https://www.youtube.com/watch?v=nKM4f1olwsI
  - Spark Join and shuffle: https://www.youtube.com/watch?v=vswrfVkP10Y
  - Spark Basics | Shuffling: https://www.youtube.com/watch?v=ffHboqNoW_A
  - Shuffle Partition Spark Optimization - 10x Faster!: https://www.youtube.com/watch?v=q1LtBU_ca20
comments: true
---

# 5 Practical Ways to Speed Up Your Apache Spark Queries


!!! info "TLDR"

    After reading this article, you will learn how to:

    - Apply filters before joins to reduce data shuffling
    - Avoid premature `collect()` actions that cause memory bottlenecks
    - Replace UDFs with built-in functions for better performance
    - Optimize duplicate removal using efficient methods
    - Implement broadcast joins for small table operations


<!-- more -->

Apache Spark is a powerful data processing framework that allows you to handle both batch and streaming data. It also provides high-level APIs that make it easier to work with datasets intuitively, without needing to worry too much about the underlying details of distributed systems.

However, as your data scales up significantly, you eventually have to start thinking about how those operations are actually executed under the hood.

So in this article, I'd like to share five commonly used tips that can help you write more efficient Spark queries and avoid consuming excessive Spark resources. For each tip, I'll start by explaining what an inefficient query looks like and why it performs poorly. Then, I'll walk through how you can rewrite it for better performance. That way, you'll get a clearer sense of the difference between the two approaches.


## Filter Early Before Joins

Let's say you're working with an e-commerce platform where you have two main tables: a `users` table containing customer information (around 1 million records) and an `events` table that logs all user activities like page views, clicks, and purchases (potentially billions of records). Your goal is to **find all users who have made purchases**, so you need to join these tables and filter for purchase events specifically.

!!! failure "Slow Query"

    ```python
    users.join(events, on="user_id").filter(events["event_type"] == "purchase")
    ```

This code performs a full join operation first before applying the filter condition. When `events` contains a large amount of data, this approach causes **excessive shuffle operations and memory consumption**. The filter condition could have been applied earlier through **predicate pushdown optimization**, but this optimization doesn't occur in this scenario.

!!! success "Fast Query"

    ```python
    purchase_events = events.filter(events["event_type"] == "purchase")
    users.join(purchase_events, on="user_id")
    ```

By filtering `events` before the join operation, we significantly reduce the amount of data that needs to be shuffled during the join. This technique implements filter pushdown and early pruning concepts, which minimize the computational overhead and improve query performance.


## Avoid Premature `collect()` Actions

One of the most common mistakes in Spark development is using `collect()` when you only need to inspect or sample your data. This operation forces all data from distributed executors back to the driver node, creating a severe bottleneck and potentially causing out-of-memory errors.

Let's say you're analyzing customer purchase patterns in your e-commerce platform. You have a large `orders` table with millions of records, and you want to quickly examine some sample data to understand the structure before writing more complex analytics queries.

!!! failure "Slow Query"

    ```python
    # This brings all data back to the Driver
    orders.collect()
    ```

The `collect()` operation pulls the entire DataFrame data back to the Driver's memory, which can cause out-of-memory errors. This approach prevents distributed execution and creates a bottleneck at the Driver node, negating the benefits of Spark's distributed computing architecture.

!!! success "Fast Query"

    ```python
    # Use aggregation or sampling instead
    orders.sample(fraction=0.1).show()
    ```

The `show()` operation only displays the first few records and completes the computation on the Executors. By using operations like `limit()`, `sample()`, or other batch processing methods, we can examine data incrementally while reducing pressure on the Driver node.


## Use Built-in Functions Over UDFs

Let's say you want to calculate discounted prices for your e-commerce orders. You have an `orders` table with `price` and `discount_rate` columns, and you need to compute the final price after applying the discount.

!!! failure "Slow Query"

    ```python
    from pyspark.sql.functions import udf
    from pyspark.sql.types import DoubleType

    @udf(DoubleType())
    def calculate_discounted_price(price, discount_rate):
        return price * (1 - discount_rate)

    orders.withColumn("final_price", calculate_discounted_price(orders["price"], orders["discount_rate"]))
    ```

User Defined Functions (UDFs) act as black boxes that the Spark Catalyst Optimizer **cannot optimize**. During execution, there's **significant overhead from switching between the JVM and Python environments**. Additionally, UDFs bypass Spark's native optimization mechanisms, often resulting in much slower performance.

!!! success "Fast Query"

    ```python
    from pyspark.sql.functions import col

    orders.withColumn("final_price", col("price") * (1 - col("discount_rate")))
    ```

Using built-in functions allows the Catalyst Optimizer to recognize and optimize operations through **vectorized computations**. This approach eliminates the need for JVM-Python context switching and leverages Spark's internal optimization capabilities.



## Choose Broadcast Joins for Small Tables

!!! failure "Slow Query"

    ```python
    df1.join(df2, "id")
    ```

Spark doesn't know which Data Frame is smaller, so it defaults to using **shuffle hash join**. Even when `df2` is clearly small, the absence of broadcast hints forces Spark to perform unnecessary shuffle operations, impacting performance significantly.

!!! success "Fast Query"

    ```python
    from pyspark.sql.functions import broadcast
    df1.join(broadcast(df2), "id")
    ```

Using broadcast join sends the smaller table directly to each executor, eliminating shuffle operations entirely. This approach is ideal for tables smaller than 10MB or the configured `spark.sql.autoBroadcastJoinThreshold` value.

Spark 會根據 `spark.sql.autoBroadcastJoinThreshold`，自動判斷是否廣播：

## Optimize Duplicate Removal

<!-- TODO -->

!!! failure "Slow Query"

    ```python
    df.select("user_id").distinct().count()
    ```

The `distinct()` operation is equivalent to a `groupBy` with aggregation, which triggers shuffle operations. When dealing with large datasets, this can cause severe **network I/O bottlenecks** and **memory pressure** across the cluster.

!!! success "Fast Query"

    ```python
    df = df.repartition("user_id").dropDuplicates(["user_id"])
    ```

Using `repartition()` with a specific key reduces the shuffle volume by creating local data ordering. The `dropDuplicates()` method provides more semantic clarity for multi-column operations compared to `distinct()`, enabling better optimization by the Catalyst optimizer.


<!-- ## Summary: Spark Query Acceleration Principles

| Category | Performance Issue | Fast Approach Principle |
| -------- | ------------ | ------------------------------ |
| filter   | Applied after join    | Apply filter early to reduce join data volume         |
| collect  | Returns all data to driver | Use show/sample/limit for batch processing         |
| UDF      | Cannot be optimized        | Use built-in functions                          |
| distinct | Causes shuffle operations   | Use dropDuplicates with repartition |
| join     | Default shuffle join | Use broadcast join when appropriate               |
from pyspark.sql.functions import broadcast
df1.join(broadcast(df2), "id")
``` -->