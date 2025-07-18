-- Write your PostgreSQL query statement below
with cte as (
    select
      fail_date as date,
      'failed' as period_state
    from failed
    union
    select
      success_date as date,
      'succeeded' as period_state
    from succeeded
),
cte2 as (
  select
    date,
    period_state,
    rank() over (partition by period_state order by date asc) as rank
  from cte
  where date between '2019-01-01' and '2019-12-31'
),
cte3 as (
  select 
    *,
    date - rank * interval '1 day' AS grp
  from cte2
)

select
  period_state,
  min(date) as start_date,
  max(date) as end_date
from cte3
group by grp, period_state
order by start_date