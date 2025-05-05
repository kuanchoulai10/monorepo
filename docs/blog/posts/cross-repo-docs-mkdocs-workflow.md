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
    看完這篇文章，你可以學會如何
    
    - 使用**Git Submodule**統一管理多個專案的文件來源  
    - 設定**GitHub Actions**跨專案自動觸發與整合流程  
    - 使用**Reusable Workflows**重複利用CI/CD腳本、減少維護成本  
    - 透過**MkDocs Monorepo Plugin**將多個專案文件合併為單一網站

<!-- more -->

在你的組織中，是否有前端、後端、數據、機器學習、SRE 等不同團隊，各自擁有獨立的 Git Repository 與文件系統？雖然這樣的架構有助於職責劃分與專案管理，但當需要撰寫橫跨多個系統與團隊的整合性文件時，往往會陷入難以協作與資訊分散的困境。舉例來說，若你們正在開發一項涵蓋 API、資料同步與監控設定的新服務，相關文件可能散落在多個 Repo 裡，導致沒有人能一眼掌握整體架構與流程。這不僅拉高了文件維護成本，也拖慢了跨部門溝通效率。

試著想像這個場景：一位新人剛加入團隊，卻得花上好幾天，在不同 Repo 之間搜尋資料、追問前輩、試著拼湊出整體架構——這樣的 Onboarding 體驗，效率低落、學習曲線陡峭，對團隊的產能與信心都是傷害。你應該很難不同意，若能有一個整合且清晰的文件平台，新人不僅能快速理解整個系統的設計與邏輯，還能更快上手、主動參與，團隊整體的運作也會更順暢。

在過去的經驗中，我就曾面臨這樣的挑戰。當時我們雖然曾考慮導入 Monorepo 來解決問題，但考量到授權邊界、部署彈性與版本獨立性等因素，最終仍維持多 Repo 架構。為了彌補其缺點，我嘗試整合 Git Submodule、MkDocs Monorepo Plugin，以及 GitHub Actions，自動化構建一個集中式的文件平台。這篇文章將分享我如何一步步建立這套機制，過程中踩過的坑，以及最後總結出來的實用經驗。

![](./static/cross-repo-docs-mkdocs-workflow/flow.svg)

具體來說，這次會有三個repos

- [`monorepo`](https://github.com/kuanchoulai10/monorepo)(Main Repo) 是我用來架設個人網站的Repo，使用MkDocs並部署於 GitHub Pages，內部已經有事先定義好的`publish-docs.yml`的GitHub Actions Workflow。
- [`data2ml-ops`](https://github.com/kuanchoulai10/data2ml-ops)(Sub Repo) 則是我用來練習 DataOps 與 MLOps個人專案，裡頭也有使用MkDocs，用來建置文件。
- [`reusable-workflows`](https://github.com/kuanchoulai10/reusable-workflows)，用於存放可重複使用的workflows

我希望將 [`data2ml-ops`](https://github.com/kuanchoulai10/data2ml-ops) 中的學習筆記整合進 [`monorepo`](https://github.com/kuanchoulai10/monorepo)，這樣就能在單一網站上呈現不同專案的內容與心得，讓維護與分享更集中、更有系統。

實際完成後的自動化流程就會像是： `data2-mlops`有任何文件更新並推送至GitHub後，就會觸發`monorepo`的文件建置和部署流程，再也不必擔心跨專案的文件與線上實際在瀏覽的文件脫鉤。

本篇文章將一步步說明我如何完成這項整合，包括實作方式與注意事項。

1. **新增Submodule**  
  在`monorepo`中新增`data2ml-ops`作為Git Submodule。

2. **建立文件部署流程**  
  在`monorepo`中新增GitHub Actions Workflow，負責建置並部署文件到GitHub Pages。

3. **建立可重複使用的Workflow**  
  在`reusable-workflow`中建立Reusable Workflow，負責觸發第二步的文件部署流程。

4. **設定Sub-repo Workflow**  
  在`data2ml-ops`中建立Workflow，使用第三步的Reusable Workflow，觸發`monorepo`的文件部署流程。

5. **整合MkDocs Monorepo Plugin**  
  在`monorepo`中加入MkDocs Monorepo Plugin，整合多個文件來源。

6. **測試與驗證**  
  提交新變更，測試整體流程是否正常運作，並檢查文件是否成功部署。


## 1. 新增Submodule

!!! info "[kuanchoulai10/monorepo](https://github.com/kuanchoulai10/monorepo)"

Git Submodule 是 Git 提供的一種功能，讓你能在一個儲存庫中嵌入另一個儲存庫（子模組），並將其當作子目錄來管理。每個子模組都有獨立的版本控制歷史[^1]。適合用於以下情境：

1.	模組化管理：可將大型專案拆分為多個獨立儲存庫，例如前端與後端分開維護，透過子模組統一整合。
2.	版本獨立性：主儲存庫會鎖定子模組的特定 commit，不會受子模組的最新變更干擾，有助於穩定性控管。
3.	重複利用：共用工具庫或框架可作為子模組嵌入多個專案，避免重複維護相同代碼。

首先，在`monorepo`中透過`git submodule add`加入`data2ml-ops`並查看有新增、修改了哪些檔案

```bash
git submodule add https://github.com/kuanchoulai10/data2ml-ops.git data2ml-ops
```

```bash
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
```

```bash
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

有兩個檔案新增、修改：

1. `.gitmodules`：負責紀錄submodules要去哪裡找
    ```.gitmodules
    [submodule "data2ml-ops"]
      path = data2ml-ops
      url = https://github.com/kuanchoulai10/data2ml-ops.git
    ```
2. `data2-mlops`：負責紀錄sub-module要指向 哪個repo的哪個commit

接著將這兩個檔案推上遠端。完成後，在GitHub就可以看到`data2ml-ops @ 7369c16`，點進去後就會進入到[kuanchoulai/data2ml-ops](https://github.com/kuanchoulai10/data2ml-ops/)。由於Git Submodule功能，只紀錄submodule的commit紀錄，並不是真的要在monorepo維護submodule的code，因此只是一個reference。

```bash
git push
```

```bash
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

## 2. 建立文件部署流程

!!! info "[kuanchoulai10/monorepo](https://github.com/kuanchoulai10/monorepo)"

第二步就是要來使用GitHub Actions，建立文件的部署流程。在Github public repo使用github actions是免費的[^2]。在 GitHub Actions 中，事件是觸發整個流程的開關，像是`Push`、`Pull Request`, `Merge`等都是一種事件類型；它會觸發一個workflow，也就是一系列自動化的執行任務。每個workflow由一或多個 jobs 組成；每個 job 都是一個獨立的執行單位，在一個 runner（即虛擬機或容器）中執行；而 steps 是 job 裡依序執行的操作，每個 step 共用同一個 runner 環境，彼此可共享檔案與狀態[^3]。

不會著墨過多實際文件部署的github actions workflow怎麼寫，只針對跟git subomdules有關的。

目前這個workflow的觸發點有兩個

1. 第一個是`monorepo`有新的`push`時，就觸發文件部署的流程
2. 另個則是listen update-submodules這類的`repository_dispatch` WebHook事件。`repository_dispatch`事件是由`monorepo`外部透過GitHub API觸發而產生，[^4][^5]。update-submodules可以自行定義。那什麼時候會有這種事件發生呢？我們打算在其它submodules的repo中的文件有變動時，就觸發這個文件部署流程


```yaml linenums="1" hl_lines="5 6" title=".github/workflows/publish-docs.yml"
--8<-- "./.github/workflows/publish-docs.yml:on"
```

而這個workflow裡頭只有一個job，job的第一步通常會是先將codebase checkout到我們想要的狀態，在使用`actions/checkout@v4`時，記得加上`submodules: recursive`的設定，如果你的 repo 有 Git Submodules（子模組），就會遞迴地把所有子模組也一起 checkout 下來。沒這個選項的話，子模組資料夾會是空的。

```yaml linenums="1" hl_lines="4" title=".github/workflows/publish-docs.yml"
--8<-- "./.github/workflows/publish-docs.yml:checkout"
```

接下來，由於這個workflow有可能是由其它submodule的workflow觸發而產生，因此需要加上以下幾件事

1. 在monorepo中更新並合併 submodules，並嘗試把這些變更，合併到目前的`monorepo`中
2. 如果有變更就 commit & push 回主 repo

```yaml linenums="1" hl_lines="3 6-12" title=".github/workflows/publish-docs.yml"
--8<-- "./.github/workflows/publish-docs.yml:submodules"
```

如此一來，就可以每次在submodule有更新時，即時更新文件。完成後記得commit & push

## 3. 建立可重複使用的Workflow

!!! info "[kuanchoulai10/reusable-workflows](https://github.com/kuanchoulai10/reusable-workflows)"

第三步就是要來建立可以讓多個submodules重複使用的workflow。邏輯蠻簡單的，只有一個步驟：就是透過`curl`去觸發`monorepo`的 `repository_dispatch` webhook事件[^5]，並帶有`event_type`為`update-submodules`的data。由於是reusable workflow，所以觸發點為`workflow_call`事件[^6]

```yaml linenums="1" hl_lines="4 6 19 21 22" title=".github/workflows/trigger-monorepo-to-build-doc.yml"
--8<-- "https://raw.githubusercontent.com/kuanchoulai10/reusable-workflows/refs/heads/main/.github/workflows/trigger-monorepo-to-build-doc.yml"
```

為什麼要用reusable workflow?以後要擴充workflow時，就不必去到每個sub repos去修改

完成後記得commit & push

## 4. 設定Sub-repo Workflow

!!! info "[kuanchoulai10/data2ml-ops](https://github.com/kuanchoulai10/data2ml-ops)"

第四步則是要來真的建立呼叫reusable workflow的workflow了。首先要先去到GitHub右上角個人大頭貼 > Settings > Developer Settings > Personal access tokens > Fine-grained tokens 建立新PAT，目的是要用來讀取monorepo的metadata和讀寫code的push submodule的new commit，The fine-grained token must have the following permission set: "Contents" repository permissions (write)[^5]。建立完成後記得複製token


![](./static/cross-repo-docs-mkdocs-workflow/pat.png){ width=600 }

回到`data2ml-ops`，建立repo secrets `PAT`，將剛剛複製的token貼上

![](./static/cross-repo-docs-mkdocs-workflow/repo-secret.png)


完成後就來write workflow to call reusable workflow[^8]。只需要在job底下使用`uses`並指定workflow所在位置和分支即可

```yaml  linenums="1" hl_lines="4 6-8 12 14" title=".github/workflows/trigger-monorepo-to-build-doc.yml"
--8<-- "https://raw.githubusercontent.com/kuanchoulai10/data2ml-ops/887a9a0361e4f4b4c2491f470c49d25bd28c7243/.github/workflows/trigger-monorepo-to-build-doc.yml"
```

完成後記得git commit & push

## 5. 整合MkDocs Monorepo Plugin

!!! info "[kuanchoulai10/monorepo](https://github.com/kuanchoulai10/monorepo)"

倒數第二步就是要來使用`mkdocs-monorepo-plugin`這個MkDocs套件，這是由Backstage團隊所開發出來的套件，專門用來整合多個codebases文件的Plugin。Backsstage是由spotify開源並在2020年進入CNCF的專案，是一個內部開發平台，用於集中呈現組織所有微服務、文檔、CI/CD 狀態、API等重要資訊，幫助軟體工程團隊更有效率地工作。

首先先安裝`mkdocs-monorepo-plugin`

```
pip install mkdocs-monorepo-plugin
```

安裝完後，只要在plugins加上`monorepo`，那麽在`nav` section就有新的語法`!include`，用來讀取sub repo的`mkdocs.yml`
```yaml
...

nav:
  - Data2ML Ops: "!include ./data2ml-ops/mkdocs.yml"

...

plugins:
  - monorepo
```

完成後記得git commit & push

## 6. 測試與驗證

!!! info "[kuanchoulai10/data2ml-ops](https://github.com/kuanchoulai10/data2ml-ops)"

已經完成所有的設置，最後就是要來測試和驗證了。假設我們現在繼續在`data2ml-ops`更新文件，並推送新的一版上GitHub。去到網頁可以看到確實觸發了gihhub actions workflow。

![alt text](./static/cross-repo-docs-mkdocs-workflow/data2ml-ops-run-history.png)

[`data2ml-ops` run history](https://github.com/kuanchoulai10/data2ml-ops/actions/runs/14824960685)

workflow裡頭會使用`reusable-workflows`的`trigger-monorepo-to-build-doc.yml`，實際透過`curl`去打GitHub API，在`monorepo`建立`repository_dispatch`事件，也接著因此觸發了`monorepo`的`publish-docs.yml`

切換到`monorepo`的網頁查看，也可以發現確實觸發了文件部署的流程

![alt text](./static/cross-repo-docs-mkdocs-workflow/monorepo-run-history.png)

[`monorepo` run history](https://github.com/kuanchoulai10/monorepo/actions/runs/14824961637)

從原本的`data2ml-ops @ 7369c16`更新成`data2ml-ops @ 887a9a0`了

![alt text](./static/cross-repo-docs-mkdocs-workflow/monorepo-updated.png)



## References

[^1]: [Git Submodules Basic Explanation | gitaarik GitHub](https://gist.github.com/gitaarik/8735255)
[^2]: [About billing for GitHub Actions | GitHub Docs](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions)
[^3]: [The components of GitHub Actions | GitHub Docs](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions#the-components-of-github-actions)
[^4]: [`repository_dispatch` Event | GitHub Docs](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#repository_dispatch)
[^5]: [Create a repository dispatch event | GitHub Docs](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
[^6]: [Creating a reusable workflow | GitHub Docs](https://docs.github.com/en/actions/sharing-automations/reusing-workflows#creating-a-reusable-workflow)
[^7]: [Creating a fine-grained personal access token | GitHub Docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)
[^8]: [Calling a reusable workflow | GitHub Docs](https://docs.github.com/en/actions/sharing-automations/reusing-workflows#calling-a-reusable-workflow)
[^9]: [backstage/mkdocs-monorepo-plugin | GitHub](https://github.com/backstage/mkdocs-monorepo-plugin)