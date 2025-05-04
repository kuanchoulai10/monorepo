---
draft: true
authors:
  - kuanchoulai10
date:
  created: 2025-05-05
  updated: 2025-05-05
categories:
  - python
tags:
  - github-actions
  - git-submodules
  - mkdocs
comments: true
---

<!-- more -->

# 如何使用MkDocs Monorepo Plugin整合GitHub Actions與Git Submodules打造跨Repo文件系統

說明痛點（假設情境）

- 公司內，有前後端，有數據團隊，有機器學習團隊，SRE團隊等，分別使用各自不同的repos，也有各自的文件，分別部署
- 雖然公司有在討論是否要整合成monorepo，但考量了一些事，決定還是各自維護。
- 但還是想要有一定的整合，至少在文件上，希望能整合在同一個repo，一起用mkdocs，把開發者文件build起來。為什麼？因為可以有些系統整合的說明是跨repo的，希望能reference到所有跨repo的文件和codebases

這時候，透過這篇文章，就可以很好地的幫助你。透過這篇文章，你可以學到

1. 使用Git Submodule，整合多repo
2. 使用GitHub Actions 跨repo呼叫
3. GitHub Actions Reusable Workflow
4. MkDocs Monorepo Plugin

## Git Submodules

![](./git-submodule.drawio.svg)

```
git submodule add git@github.com:path_to/submodule.git path-to-submodule
```

```
git submodule init
```


- https://gist.github.com/gitaarik/8735255
- https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#repository_dispatch
- https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#create-a-repository-dispatch-event
- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token

## 