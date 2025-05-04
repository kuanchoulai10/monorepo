---
draft: true
authors:
  - kuanchoulai10
date:
  created: 2025-05-05
  updated: 2025-05-05
categories:
  - MkDocs
  - CI/CD
tags:
  - github-actions
  - git-submodules
  - mkdocs
comments: true
---


# 如何使用MkDocs整合GitHub Actions與Git Submodule建立Cross-repo Docs

!!! info "TLDR"
    看完這篇文章，你可以
    
    - ABC
    - STU
    - XYZ

<!-- more -->
說明痛點（假設情境）

- 公司內，有前後端，有數據團隊，有機器學習團隊，SRE團隊等，分別使用各自不同的repos，也有各自的文件，分別部署
- 雖然公司有在討論是否要整合成monorepo，但考量了一些事，決定還是各自維護。
- 但還是想要有一定的整合，至少在文件上，希望能整合在同一個repo，一起用mkdocs，把開發者文件build起來。為什麼？因為可以有些系統整合的說明是跨repo的，希望能reference到所有跨repo的文件和codebases

這時候，透過這篇文章，就可以很好地的幫助你。透過這篇文章，你可以學到

1. 使用Git Submodule，整合多repo
2. 使用GitHub Actions 跨repo呼叫
3. GitHub Actions Reusable Workflow
4. MkDocs Monorepo Plugin

![](./static/cross-repo-docs-mkdocs-workflow/flow.svg)

## Git Submodules

```bash
git submodule add git@github.com:path_to/submodule.git path-to-submodule
```

```bash
git submodule add https://github.com/kuanchoulai10/data2ml-ops.git data2ml-ops

Cloning into '{==/Users/kcl/projects/monorepo/data2ml-ops'==}...
remote: Enumerating objects: 197, done.
remote: Counting objects: 100% (197/197), done.
remote: Compressing objects: 100% (110/110), done.
remote: Total 197 (delta 78), reused 183 (delta 66), pack-reused 0 (from 0)
Receiving objects: 100% (197/197), 1.04 MiB | 1.94 MiB/s, done.
Resolving deltas: 100% (78/78), done.
```

```bash
git status

On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   {==.gitmodules==}
	new file:   {==data2ml-ops==}

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
```

```bash
git push

Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 404 bytes | 404.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/kuanchoulai10/monorepo.git
   6c36b76..c1e29ff  main -> main
```

![](./static/cross-repo-docs-mkdocs-workflow/submodule.png)

點進去後就會進入到[kuanchoulai/data2ml-ops](https://github.com/kuanchoulai10/data2ml-ops/)

## GitHub Actions - Reusable Workflow

[kuanchoulai10/reusable-workflows](https://github.com/kuanchoulai10/reusable-workflows)

```yaml linenums="1" hl_lines="4 6 19 21 22" title="trigger-monorepo-to-build-doc.yml"
--8<-- "https://raw.githubusercontent.com/kuanchoulai10/reusable-workflows/refs/heads/main/.github/workflows/trigger-monorepo-to-build-doc.yml"
```

## Monorepo

```yaml
--8<-- "./.github/workflows/publish-docs.yml:on"
```

```yaml
--8<-- "./.github/workflows/publish-docs.yml:checkout"
```

```yaml
--8<-- "./.github/workflows/publish-docs.yml:submodules"
```

## Sub-repo

1. Setup secret: Personal Access Token
    - The fine-grained token must have the following permission set: "Contents" repository permissions (write)

![](./static/cross-repo-docs-mkdocs-workflow/pat.png){ width=600 }

2. set repo secrets

![](./static/cross-repo-docs-mkdocs-workflow/repo-secret.png)


3. write workflow to use reusable workflow

```yaml
name: Trigger Monorepo to Build Docs

on:
  ...

jobs:
  trigger_monorepo:
    {==uses: kuanchoulai10/reusable-workflows/.github/workflows/trigger-monorepo-to-build-doc.yml@main==}
    secrets:
      PAT: {==${{ secrets.PAT }}==}
```


## References

- [Git Submodules Basic Explanation | gitaarik GitHub](https://gist.github.com/gitaarik/8735255)
- [Creating a reusable workflow | GitHub Docs](https://docs.github.com/en/actions/sharing-automations/reusing-workflows#creating-a-reusable-workflow)
- [Calling a reusable workflow | GitHub Docs](https://docs.github.com/en/actions/sharing-automations/reusing-workflows#calling-a-reusable-workflow)
- [`repository_dispatch` Event | GitHub Docs](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#repository_dispatch)
- [Create a repository dispatch event | GitHub Docs](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [Creating a fine-grained personal access token | GitHub Docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)
- [backstage/mkdocs-monorepo-plugin | GitHub](https://github.com/backstage/mkdocs-monorepo-plugin)