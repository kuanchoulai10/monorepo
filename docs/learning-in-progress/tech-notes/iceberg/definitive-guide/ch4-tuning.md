---
tags:
  - Apache Iceberg
---

# Ch4 Optimizing the Performance of Apache Iceberg

--8<-- "./docs/disclaimer.md"

!!! tip

    - [x] Compaction
        - Binpack
        - Sorting
        - Z-order
    - [x] Partitioning
    - [x] CoR vs. MoR
    - [x] Metric Collection
    - [x] Write Distribution Mode
    - [x] Datafile Bloom Filters

## Compaction

In this scenario, we may have been streaming some data into our `musicians` table and noticed that a lot of small files were generated for rock bands, so instead of running compaction on the whole table, which can be time-consuming, we targeted just the data that was problematic. We also tell Spark to prioritize file groups that are larger in bytes and to keep files that are around 1 GB each with each file group of around 10 GB.

[A file group is an Iceberg abstraction that represents a collection of files that will be processed by a single Spark job.](https://docs.aws.amazon.com/prescriptive-guidance/latest/apache-iceberg-on-aws/best-practices-compaction.html)

```sql
-- Rewrite Data Files CALL Procedure in SparkSQL
CALL catalog.system.rewrite_data_files(
  table => 'musicians',
  strategy => 'binpack',
  where => 'genre = "rock"',
  options => map(
    'rewrite-job-order','bytes-asc',
    'target-file-size-bytes','1073741824', -- 1GB
    'max-file-group-size-bytes','10737418240' -- 10GB
  )
)
```

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098148614/files/assets/aidg_0403.png){width="500"}
/// caption
The result of having the max file group and max file size set to 10 GB and 1 GB, respectively
///


### Sorting


![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098148614/files/assets/aidg_0404.png){width="500"}
/// caption
Sorted 
///

After creating the table, you set the sort order of the table, which any engine that supports the property will use to sort the data before writing and will also be the default sort field when using the sort compaction strategy

```sql
ALTER TABLE catalog.nfl_teams WRITE ORDERED BY team;
```

```sql
CREATE TABLE catalog.nfl_teams 
    AS (SELECT * FROM non_iceberg_teams_table ORDER BY team);
    
ALTER TABLE catalog.nfl_teams WRITE ORDERED BY team;s
```

if you wanted to rewrite the entire dataset with all players sorted by team globally, you could run the following statement:

```sql
CALL catalog.system.rewrite_data_files(
  table => 'nfl_teams',
  strategy => 'sort',
  sort_order => 'team ASC NULLS LAST'
)
```

### Z Order

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098148614/files/assets/aidg_0407.png){width="500"}
/// caption
Z-order
///

```sql
CALL catalog.system.rewrite_data_files(
  table => 'people',
  strategy => 'sort',
  sort_order => 'zorder(age,height)'
)
```

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098148614/files/assets/aidg_0408.png){width="500"}
/// caption
Z-ordering based on age and height
///