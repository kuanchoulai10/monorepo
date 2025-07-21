---
draft: true
authors:
  - kuanchoulai10
date:
  created: 2025-07-22
  updated: 2025-07-22
categories:
  - Data
tags:
  - The Lakehouse Series
comments: true
---

# The Lakehouse Series: Delta Lake Overview

!!! info "TLDR"

    After reading this article, you will learn:

    - abc
    - def
    - ghi


<!-- more -->

Delta Lake emerged from Databricks in 2019 as the brainchild of the same team that created Apache Spark, led by Matei Zaharia and his colleagues who were tackling the reliability and performance challenges of big data pipelines at scale. Born from real-world production pain points at Databricks and their enterprise customers, Delta Lake was designed to bring ACID transactions and data versioning to the data lake ecosystem. Open-sourced under the Apache 2.0 license in 2019 and later contributed to the Linux Foundation as the Delta Lake project, it has rapidly gained traction with over 8,100 GitHub stars and contributions from over 350 developers worldwide. The project enjoys strong backing from Databricks, Microsoft, AWS, and a growing ecosystem of data platform vendors.

Delta Lake's architecture is built around **simplicity and reliability**. At its core, Delta Lake uses a **transaction log** (the `_delta_log` directory) that acts as a single source of truth, recording every change to the table as ordered, atomic commits stored in JSON files. This **log-based approach** ensures ACID guarantees while maintaining compatibility with existing Parquet-based data lakes. Delta Lake's design philosophy emphasizes **zero-copy cloning**, **automatic schema enforcement**, and **seamless integration with Apache Spark**, making it the pragmatic choice for organizations already invested in the Spark ecosystem. The format's **unified streaming and batch processing** capabilities, combined with **built-in data quality constraints** and **automatic file management**, position Delta Lake as the Swiss Army knife of lakehouse formats.

## Storage Layout

!!! info "TLDR"

    After reading this article, you will learn:

    - abc
    - def
    - ghi


<!-- more -->

Ever wondered how Delta Lake keeps track of all your data without losing its mind? The secret sauce lies in its beautifully simple yet powerful architecture that revolves around one core principle: **everything goes through the transaction log**. Think of it as your data's personal accountant who never takes a day off!

**The Transaction Log: Your Data's Single Source of Truth**

Picture the `_delta_log` directory as the ultimate diary of your table — it's where Delta Lake writes down every single thing that happens to your data, no matter how small. This isn't just any ordinary log; it's a **chronologically ordered sequence of JSON files** that captures every action like a meticulous historian.

Here's what makes this approach absolutely brilliant:

```
my_table/
├── _delta_log/
│   ├── 00000000000000000000.json  # The beginning of time
│   ├── 00000000000000000001.json  # First transaction
│   ├── 00000000000000000002.json  # Second transaction
│   └── ...
├── part-00000-xyz.parquet         # Actual data files
├── part-00001-abc.parquet
└── ...
```

Each JSON file in the transaction log is like a **commit message on steroids** — it doesn't just say "hey, something changed," it provides the complete blueprint of what the table should look like after that transaction. It's like having a GPS that not only tells you where you are, but also remembers every turn you've made to get there!

**Transaction Log Files: The Building Blocks**

Every time you perform an operation (insert, update, delete, schema change), Delta Lake creates a new numbered JSON file in the `_delta_log` directory. These files contain **actions** that describe exactly what happened:

- **Add File Actions**: "Hey, we've got a new data file joining the party! Here's where it lives and what it contains."
- **Remove File Actions**: "Time to say goodbye to this old file — it's been replaced or deleted."
- **Metadata Actions**: "The table schema just got an upgrade — here are the new rules everyone needs to follow."
- **Protocol Actions**: "We're updating the table format version — buckle up for new features!"

What's mind-blowing is that these JSON files are **immutable** — once written, they never change. It's like having a paper trail that can't be tampered with, ensuring your data's history is bulletproof.

**Checkpoints: The Smart Shortcuts**

Now, you might be thinking: "What happens when I have thousands of these JSON files? Won't reading through all of them take forever?" That's where Delta Lake's **checkpoint mechanism** comes to the rescue like a superhero!

Every 10 commits (by default), Delta Lake creates a special **checkpoint file** — think of it as a "save game" feature that captures the entire state of your table at that moment. Instead of reading through hundreds of individual transaction files, query engines can just load the latest checkpoint and then catch up with any newer transactions. It's like fast-forwarding through a movie to get to the good parts!

```
_delta_log/
├── 00000000000000000000.json
├── ...
├── 00000000000000000009.json
├── 00000000000000000010.checkpoint.parquet  # Snapshot at commit 10
├── 00000000000000000011.json
├── ...
├── 00000000000000000020.checkpoint.parquet  # Snapshot at commit 20
└── ...
```

**Data Files: Where the Magic Lives**

While the transaction log handles all the bookkeeping, your actual data lives in **Parquet files** (or other columnar formats) stored right alongside the `_delta_log` directory. These files are like the actual books in a library, while the transaction log is the card catalog that tells you exactly which books exist and where to find them.

Here's the elegant part: Delta Lake doesn't move or modify your existing data files when you perform updates or deletes. Instead, it plays a clever game of **"add and subtract"** through the transaction log:

1. **Updates**: Create new files with the updated records, mark old files as removed
2. **Deletes**: Mark files as removed without physically deleting them (until cleanup runs)
3. **Inserts**: Simply add new files and record them in the transaction log

This approach is like having a **time machine for your data** — you can always travel back to any previous version by replaying the transaction log up to that point!

**ACID Guarantees Through Atomic Commits**

The real genius of Delta Lake's design is how it achieves **ACID transactions** through atomic file operations. When you write to a Delta table, here's what happens behind the scenes:

1. **Write data files**: New Parquet files are written to the table directory
2. **Prepare transaction**: A JSON transaction file is prepared with all the changes
3. **Atomic commit**: The transaction file is atomically written to `_delta_log`
4. **Success or failure**: Either the entire transaction succeeds, or none of it does

It's like a bank transfer — either the money moves completely from one account to another, or the transaction fails entirely. No partial transfers, no inconsistent states, no sleepless nights wondering if your data is corrupted!

**Schema Evolution: Painless Progress**

One of Delta Lake's most delightful features is how it handles **schema evolution**. When you need to add a new column or change a data type, Delta Lake records these changes in the transaction log as **metadata actions**. Every subsequent read operation knows exactly how to interpret the data based on when it was written.

It's like having a universal translator that automatically adapts to new languages — your old data doesn't need to be rewritten, and your new data can use the updated schema seamlessly!

**Multi-Reader, Single-Writer (with Optimistic Concurrency)**

Delta Lake's transaction log enables **optimistic concurrency control** — multiple readers can safely access the table simultaneously, while writers coordinate through the atomic commit mechanism. If two writers try to modify the table at the same time, Delta Lake detects the conflict and asks one of them to retry with the latest state.

Think of it like a polite conversation where everyone takes turns speaking — no one talks over each other, but multiple people can listen at the same time!

This simple yet powerful architecture is what makes Delta Lake so reliable and easy to reason about. No complex metadata hierarchies, no distributed coordination nightmares — just a straightforward transaction log that keeps everything in perfect harmony.


