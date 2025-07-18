with recursive task_subtasks (task_id, subtask_id) as (
    select
        *
    from tasks

    union

    select
        task_id,
        subtask_id - 1
    from task_subtasks
    where subtask_id > 1
)

select
    task_id,
    subtask_id
from task_subtasks
where (task_id, subtask_id) not in (
    select
        *
    from executed
)