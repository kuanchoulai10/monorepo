---
tags:
  - Apache Spark
---

# Ch3 Structured APIs

--8<-- "./docs/disclaimer.md"

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0302.png){width="500"}
/// caption
When errors are detected using the Structured APIs
///

At the core of the Spark SQL engine are the Catalyst Optimizer and Project Tungsten. Together, these support the high-level DataFrame and Dataset APIs and SQL queries.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0303.png){width="500"}
/// caption
Spark SQL and its stack
///

The Catalyst Optimizer takes a computational query and converts it into an execution plan. It goes through four transformational phases:

1. **Analysis**
    - any columns or table names will be resolved by consulting an internal Catalog
2. **Logical Optimization**
    - Applying a standard-rule based optimization approach
    - the Catalyst optimizer will first construct a set of multiple plans and then
    - using its cost-based optimizer (CBO), assign costs to each plan.
    - These plans are laid out as operator trees 
3. **Physical Planning**
4. **Code Generation**
    - The final phase of query optimization involves generating efficient Java bytecode to run on each machine. 

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0304.png){width="500"}
/// caption
A Spark computation's four-phase journey
///

Real Example:

```scala
// In Scala
// Users DataFrame read from a Parquet table
val usersDF  = ...
// Events DataFrame read from a Parquet table
val eventsDF = ...
// Join two DataFrames
val joinedDF = users
  .join(events, users("id") === events("uid"))
  .filter(events("date") > "2015-01-01")
```

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492050032/files/assets/lesp_0305.png){width="500"}
/// caption
An example of a specific query transformation
///
