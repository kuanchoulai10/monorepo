# Git

## Publish

```bash
git push -u origin $(git branch --show-current)
```

## Pull + Rebase

```sh
git pull --rebase origin
```

## Squash

Squash the last 3 commits

```shell
git rebase -i HEAD~3
```

```
pick aaaaaaa commit message 1
pick bbbbbbb commit message 2
pick ccccccc commit message 3
```

```
pick aaaaaaa commit message 1
squash bbbbbbb commit message 2
squash ccccccc commit message 3
```

If pushed to the remote branch, then you should push 

```
git push -f
```

## Rebase Feature Branch onto latest Main Branch

First, make sure you are currently on your feature branch, then fetch the latest changes from the remote repository:

```bash
git fetch origin
```

Next, rebase your feature branch onto the updated `main` branch:

```bash
git rebase origin/main
```

If conflicts occur during the rebase, resolve them manually, stage the resolved files, and continue the rebase process:

```bash
git add <resolved-files>
git rebase --continue
```

After the rebase is completed, push the updated branch to the remote repository. Since rebasing rewrites commit history, use a safe force push:

```bash
git push --force-with-lease
```

If you need to stop the rebase process at any point, you can abort it:

```bash
git rebase --abort
```

**Note:** Avoid rebasing branches that are shared with other developers. Instead, consider merging the `main` branch into your feature branch by using:

```bash
git merge origin/main
```

## Delete local branches that are not used in remote

```bash
git fetch --prune

git branch -vv \
| grep ': gone]' \
| awk '{print $1}' \
| xargs git branch -d
```

??? note "Detail"

    This command sequence does the following:

    - `git fetch --prune`: Fetches the latest changes from the remote repository and removes any references to branches that have been deleted on the remote.
    - `git branch -vv`: Lists all local branches along with their tracking information and the latest commit message. then `grep ': gone]'` filters out branches that are marked as "gone", which indicates that the corresponding remote branch has been deleted. Finally, `awk '{print $1}'` extracts the branch names from the filtered list, and `xargs git branch -d` deletes those local branches that are no longer present on the remote repository.

## Worktrees

Create a worktree folder under `<path/to/worktree>` and create a branch named `<branch-name>` from `main` branch.

```bash
git worktree add <path/to/worktree> main -b <branch-name>
```

Move worktree folder from `<path/to/old/worktree>` to `<path/to/new/worktree>`

```bash
git worktree move <path/to/old/worktree> <path/to/new/worktree>
```

To show worktree list, in `main` worktree, run:

```bash
git worktree list
```

In worktree folder, run:

```
git branch --show-current
git status
```

!!! warning

    同一個 branch 不能同時在兩個 worktree 被 checkout

To prevent a working tree from being pruned:

```bash
git worktree lock
```

To allow working tree to be pruned, moved or deleted:

```bash
git worktree lock
```

To remove a working tree:

```bash
git worktree remove <path/to/worktree>
git worktree prune
```
