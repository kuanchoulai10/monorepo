# Github Actions - Reusable Workflows

- A workflow that uses another workflow is referred to as a "caller" workflow.
- The reusable workflow is a "called" workflow.
- One caller workflow can use multiple called workflows.
- Each called workflow is referenced in a single line.
- If you reuse a workflow from a different repository, any actions in the called workflow run as if they were part of the caller workflow.
- When a reusable workflow is triggered by a caller workflow, the github context is always associated with the caller workflow.
- Workflow templates allow everyone in your organization who has permission to create workflows to do so more quickly and easily. When people create a new workflow, they can choose a workflow template and some or all of the work of writing the workflow will be done for them.


- [Reusing workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows)
- []