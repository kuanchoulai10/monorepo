# Git

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

**Note:**
Avoid rebasing branches that are shared with other developers.


# Vim

`dd` + `P`
