# Git

Squash the last 3 commits

```bash
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
