# Data


## Data Lakehouse

!!! question "What is Apache Iceberg?"

    ??? tip "Answer"

        Apache Iceberg is a high-performance Data Lakehouse table format designed for huge analytic datasets. It was originally developed by Netflix and later became an open-source Apache project. It supports features like **schema evolution**, **hidden partitioning**, and **time travel**, making it easier to manage large datasets efficiently!

        one cool feature of Apache Iceberg is **schema evolution**, which allows you to change your table's schema—like adding or renaming columns—without having to rewrite or recreate the table.
        
        Another feature is **hidden partitioning**, which means you can partition your data without having to expose those partitions in your query logic, making queries simpler and faster. Iceberg also supports **partition evolution** through hidden partitioning, which decouples logical columns from physical layout by tracking partition transforms in metadata.
        
        And then there's **time travel**, which lets you query historical versions of your data, so you can basically go back in time and see what the data looked like at any previous point.  A really common use case for time travel is data auditing and debugging.
        
        It's all about making data management a lot more flexible and efficient! 

