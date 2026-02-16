# `gh`

This document lists some useful `gh` shortcuts for GitHub CLI.

## Creating a new public repository and pushing the current directory

To create a new public repository and push the current directory to it:

```bash
gh repo create <repo> \
  --source=. \
  --remote=origin \
  --push \
  --public
```

## Changing the visibility of an existing repository

To change the visibility of an existing repository to public:

```bash
gh repo edit \
  --visibility public \
  --accept-visibility-change-consequences
```

Other visibility options include `private` and `internal`.

## Authentication

To login to GitHub CLI:

```bash
gh auth login
```

To switch between accounts:

```bash
gh auth switch
```

To set up Git to use GitHub CLI for authentication:

```bash
gh auth setup-git
```

Behind the scenes, this command configures Git to use `gh` as a credential helper, allowing Git to delegate authentication to GitHub CLI when interacting with GitHub repositories.

## Workflows

```bash
gh workflow list --json name \
| jq -r ".[].name" \
| gum choose \
| xargs -I {} gh run list --workflow "{}" --json displayTitle,conclusion,url,startedAt,status
```