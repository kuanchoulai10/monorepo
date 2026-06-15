---
name: writing-monorepo-blog-post
description: Use when drafting, scaffolding, or editing a blog post under docs/blog/posts/ in this monorepo (kuanchoulai10's MkDocs Material blog). Helps the author judge which type of article they are writing (實戰經驗型 / 趨勢觀察型 / 技術新聞解析型, or a new type), then applies the matching narrative arc on top of the shared file layout, frontmatter conventions, article skeleton, and MkDocs Material syntax. Also enforces a short list of voice-level and type-specific writing anti-patterns. Trigger whenever the user mentions writing a new blog post, adding a post to the blog, drafting an article for the lakehouse series, summarising a YouTube talk or paper into a post, reacting to a product/version announcement, or editing posts under docs/blog/posts/, even if they don't say the word "skill".
---

# Writing a Blog Post in this Monorepo

This skill encodes the author's own conventions for posts under `docs/blog/posts/`. It assumes the post will be rendered by MkDocs Material. Follow the structural and syntactic conventions below; on writing voice, follow the author's tone (see the anti-patterns section — do **not** introduce metaphors, personification, or em-dash sentence breaks the author hasn't asked for).

## 0. Pick the article type first

Before touching the file structure or the skeleton, identify which kind of article the author is writing. Different types answer different reader questions and demand different structures, hooks, and anti-patterns. The skeleton in §3 is a **shared baseline** (frontmatter, TLDR, `<!-- more -->`, figure, section pattern) — the article-type reference adds the **narrative arc** on top.

The author has defined three types so far (the list is open-ended; new types may be added later):

| Type | Reference file | Answers the question |
|---|---|---|
| 實戰經驗型 (Implementation Article) | [`references/article-type-implementation.md`](references/article-type-implementation.md) | 我做了什麼，以及我是怎麼做到的。 |
| 趨勢觀察型 (Trend Analysis Article) | [`references/article-type-trend-analysis.md`](references/article-type-trend-analysis.md) | 我看到了什麼，以及這些事情之間有什麼關聯。 |
| 技術新聞解析型 (Technical News Analysis Article) | [`references/article-type-news-analysis.md`](references/article-type-news-analysis.md) | 最近發生了什麼，以及這件事情為什麼重要。 |
| 借鏡反推型 (Case Study Synthesis Article) | [`references/article-type-case-study-synthesis.md`](references/article-type-case-study-synthesis.md) | 別人在用這項技術時都遇到了什麼共同問題，這些問題反映該技術本身有什麼設計挑戰。 |

**Workflow:**

1. Ask the author which type fits — or infer it from the source material they share (e.g. "a YouTube talk + my own bottleneck experience" → implementation; "I've been reading several papers and noticed a pattern" → trend; "X just released version N" → news analysis). When inferring, state your guess and let them confirm.
2. Read the matching reference file in full. It contains three paragraphs: (1) what the type is and why it matters to readers, (2) the recommended narrative arc, (3) the anti-patterns specific to that type.
3. Apply that narrative arc *inside* the shared skeleton from §3. The TLDR bullets, section sequence, and closing should reflect the type's arc — not just generic "overview → details → summary".
4. If the post genuinely doesn't fit any existing type, tell the author and propose adding a new reference file rather than forcing a bad fit.

The type-specific anti-patterns in each reference file are **in addition to** the voice-level anti-patterns in §5 of this SKILL.md, not a replacement.

## 1. File and directory layout

Posts live under `docs/blog/posts/{year}/{half}/{slug}/` where `{half}` is either `01-06` (Jan–Jun) or `07-12` (Jul–Dec). Each post is its own directory containing the markdown file and an `assets/` subdirectory.

```
docs/blog/posts/
└── 2026/
    └── 01-06/
        └── my-new-post/
            ├── my-new-post.md
            └── assets/
                ├── diagram.drawio.svg
                └── chart.excalidraw.svg
```

- The markdown filename matches the slug exactly (`my-new-post.md`, not `index.md`).
- Drafts live under `docs/blog/posts/{year}/drafts/{slug}/` and are promoted into a half-year folder when published.
- Image assets are kept local to the post in `assets/`. Preferred formats: `*.drawio.svg`, `*.excalidraw.svg`, `*.png`. Reference them with relative paths (`./assets/foo.drawio.svg`).
- Pick the half-year folder by the `date.created` value, not by when you started drafting.

## 2. Frontmatter

Every post starts with this YAML block. Keep the field order consistent so diffs stay clean.

```yaml
---
authors:
  - kuanchoulai10
date:
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
categories:
  - Data
tags:
  - <Series Name>          # e.g. "The Lakehouse Series"
  - <Specific Topic>       # e.g. "Apache Iceberg"
links:
  - blog/posts/.../related-post.md
  - "Human Title: https://external.url"
comments: true
---
```

Conventions:

- `authors` is always `kuanchoulai10`.
- `date.created` and `date.updated` are the same on first publish; bump only `updated` on later edits.
- `categories` is high-level (mostly `Data`). Use one category.
- `tags` is where the series name and specific tech go. If the post is part of a series, the series name is the first tag.
- `links` lists related internal posts (as repo-relative paths from `docs/`) and curated external references. External links use the `"Title: https://url"` string form so MkDocs renders them with a readable label.
- `comments: true` is always present.

When the post belongs to an established series (e.g. "The Lakehouse Series"), cross-link to the other entries in `links` so the MkDocs Material related-posts block stays connected. Look at sibling posts in the same series to copy the link set.

## 3. Article skeleton

Use this exact skeleton. The TLDR admonition and `<!-- more -->` marker are required — MkDocs Material uses `<!-- more -->` to cut the home-page excerpt, and the TLDR is the author's standard opening.

```markdown
# <Series Name>: <Post Title>          ← or a standalone title like "5 Practical Ways to ..."

!!! info "TLDR"

    After reading this article, you will learn:

    - <Concrete takeaway 1>
    - <Concrete takeaway 2>
    - <Concrete takeaway 3>

<!-- more -->

<figure markdown="span">
  ![<alt text>](./assets/<cover>.drawio.svg){width="600"}
  *<short caption>*
</figure>

<Opening paragraph: history / motivation / problem statement. No metaphor opener.>

## <First major section>

<Prose paragraph that introduces the section.>

- **<Key term>**: <Explanation.>
- **<Key term>**: <Explanation.>

### <Subsection>

<...>
```

Notes on structure:

- Title is either `<Series>: <Topic>` or an actionable phrase (`N Practical Ways to ...`, `What's New in ...`). Keep it concrete.
- TLDR bullets are takeaways, not a table of contents. Phrase them as "you will learn X" items.
- After `<!-- more -->`, lead with a cover figure when one exists, then an opening paragraph that states what the thing is and why it matters. Do not open with a metaphor or analogy.
- Within each `##` section: one short prose paragraph to set context, then a bulleted list of properties / steps / components. This pattern repeats throughout the post.
- The post ends after its final substantive `##` section. Do **not** add a generic closing section (e.g. `Putting It All Together`, `Conclusion`, `Wrapping Up`) by default — only include one when the author explicitly asks for it. If they do, two valid forms exist: (1) an FAQ-style block using `!!! question` admonitions; (2) a short `Future Plans`-style outlook section. The outlook form must be **short flowing prose with references embedded inline as markdown links — never a bulleted list of references**. It should end with an explicit forward-looking sentiment (「我非常看好」/「期待這個方向最終會延伸到什麼位置」 etc.), not a flat observation. The goal is "next-stop recommendations for readers who want to dig further", framed as a hopeful close, not an info dump.

## 4. MkDocs Material syntax used in this blog

These are the elements the author actually uses. Prefer them over inventing new patterns.

**Admonitions** — `info` for TLDR, `question` for Q&A, `failure`/`success` for slow-vs-fast code comparisons, `warning` sparingly:

```markdown
!!! info "TLDR"

    ...

!!! question "Can one X reference multiple Ys?"

    Yes. ...

!!! failure "Slow Query"

    ```python
    users.join(events, on="user_id").filter(...)
    ```

!!! success "Fast Query"

    ```python
    filtered = events.filter(...)
    users.join(filtered, on="user_id")
    ```
```

**Figures with captions** — always use `<figure markdown="span">` so the caption renders:

```markdown
<figure markdown="span">
  ![Iceberg Storage Layout](./assets/iceberg.drawio.svg){width="600"}
  *Iceberg Storage Layout*
</figure>
```

For external images with a clickable caption, wrap the caption in a link:

```markdown
<figure markdown="span">
  ![Data Lakehouse](https://example.com/img.png)
  [*Data Architecture Evolution*](https://example.com/source)
</figure>
```

**Inline emphasis** — `**bold**` for key terms (used heavily, multiple per paragraph), `*italic*` for filenames, captions, and softer emphasis. Inline code with backticks for identifiers, paths, SQL keywords.

**Code blocks** — always fence with a language tag. When showing multiple dialects of the same thing, use one fenced block per dialect with a top-of-block comment naming the dialect:

````markdown
```sql
-- Spark SQL
SELECT * FROM prod.db.table.history;
```
```sql
-- Trino SQL
SELECT * FROM "test_table$history";
```
````

**Bullet lists inside lists** — when a bullet introduces a code snippet, indent the fenced block four spaces under the bullet so it nests correctly.

**Embedded video** — for YouTube references, use the standard iframe snippet (copy from any existing post; the attribute list is long and stable).

**Star History charts** — for comparing open-source projects by popularity:

```markdown
![Star History Chart](https://api.star-history.com/svg?repos=org1/repo1,org2/repo2&type=Date)
```

## 5. Writing voice and language preferences

These preferences have converged across multiple posts. They are organised into three layers — **用字 (word choice)**, **句子構造 (sentence structure)**, and **段落安排 (paragraph patterns)** — plus a short **process** note at the end. Every rule has a short reason; understanding the *why* lets you handle edge cases instead of mechanically pattern-matching.

The general voice to match: direct second-person ("you"), heavy bolding of key terms, concrete examples, and a tendency to finish each section with a sentence that sets up the next one.

### 5.1 用字 (Word choice)

#### Keep these English terms verbatim — do not translate

In Chinese prose, these terms read more precisely in English. Translating them weakens the technical register the author wants.

| English term | Do NOT write |
|---|---|
| `metadata` | 元數據 |
| `table` / `tables` (including compounds like `wide table`, `SQL table`, `Iceberg table`) | 表、資料表、寬表、SQL 表、Iceberg 表 |
| `Reader` / `Writer` / `Serializer` / `Compactor` and similar software component names (capitalize as if proper noun) | 讀取器、寫入器、序列化器、壓縮器 |
| `index` (including compounds like `inverted index`, `secondary index`, `vector index`) | 索引、倒排索引、二級索引、向量索引 |
| `background` (when paired with `thread` / `process` / `job` / `fetch` etc.) | 背景線程、背景行程 |
| `partition` / `partitioning` | 分區 |
| `query planning` | 查詢規劃 |
| `metadata planning` | 中繼資料規劃 |
| `cache` / `caching` | 快取 |
| `table format` | (translate) |
| `Catalog` (Iceberg/Hive Catalog) | 目錄、編目 |
| `Compute Engine` | 計算引擎 |
| `Data Mesh` | (translate) |
| `Data Lakehouse` | 數據湖倉 |
| `level` (e.g. partition/file level) | 級別 |
| `centralized` | 集中式、中心化 |
| `batch` / `batch processing` | 批次、批次處理 |
| `batch-stacked` | 批次堆疊 |
| `append-only` | 純追加、僅追加 |
| `compound` (e.g. cost compounds) | 複合式增長 |
| `rollback` | 回滾 |
| `lock` | 鎖 |
| `parallelism` | 並行能力、平行能力 |
| `Primary Key` | 主鍵 |
| `edge case` | 邊角案例、特殊案例、邊緣情況 |
| `resource pool` | 資源池 |
| `orchestration tool` | 編排工具 |
| `required` / `optional` (paired) | 必要 / 選用 |
| `snapshot` / `manifest files` / `pointer` (scale-related) | (translate) |
| `Data Freshness` (kept as English title-case noun in body prose) | 資料新鮮度 |
| `ElasticSearch` (author's preferred spelling; overrides the official one-word "Elasticsearch") | Elasticsearch / 彈性搜尋 |

Headings already mix English and Chinese; body prose should follow the same register.

#### Avoid these Chinese substitutions

| Avoid | Use instead | Reason |
|---|---|---|
| 量級 (when describing scale levels) | 規模 | 量級 has a different register; 規模 reads cleaner |
| 契機 (when describing why a tech was adopted) | 動機 | 契機 is too literary for engineering writing |
| 資料表越長越大 | 「隨著資料規模越來越大」/「隨著 tables 越來越多」 | personifies the table |
| 受控的速度 | 穩定可控的速率 | "速度" is too colloquial here |
| 引擎 (e.g. OLAP 引擎、查詢引擎、資料庫引擎) | 產品 — or keep the technical term in English (`Compute Engine`, `query engine`) | the author dislikes 引擎 in body prose; use 產品 when referring to a vendor/product, keep English when naming the technical role |
| 兆級 / 兆級資料 | `trillion-row` / `trillion-scale` / `trillion rows` | scale descriptors stay in English; 兆級 reads as overly translated |
| 自研 (e.g. 自研 reader) | 自行研發 | the spelled-out form matches the author's prose register; 自研 reads as a hurried abbreviation |
| 對讀 / 對讀之後 | 仔細研究 / 仔細研究之後 | 對讀 carries a literary register that doesn't match engineering prose |
| 刷新 (when describing cache / metadata refresh) | 更新 | 刷新 evokes browser-page-refresh; 更新 is the standard technical register |
| 缺口 / 空缺 (when describing gaps in a spec or design) | 不足 | the author prefers the analytical "insufficiency" framing; 缺口 carries a breach-like, structurally-judgmental tone |
| 線 / 條線 (when used as a metaphor for "thematic thread" / "work stream") | 面向 (e.g. 「在 metadata 這個面向上」) | the author dislikes 線 as a thematic-thread metaphor; 面向 reads as a flat structural noun |
| 位置 (when used as a metaphor for "area / aspect of design", e.g. 「在同樣幾個位置」) | 層面 (e.g. 「在同樣幾個層面」) | 位置 is too spatial / literal for an abstract aspect; 層面 reads as a flat structural noun. Note: 位置 in concrete senses (a spec slot, a UI position) is fine; only the metaphorical "area-of-work" sense should swap |
| 展開 (when meaning "elaborate again on something already covered") | 贅述 (e.g. 「這裡不再贅述」) | 展開 in this rhetorical sense is filler; 贅述 explicitly acknowledges that further explanation would be redundant. Note: 展開 in technical senses (e.g. 「tree 展開」, 「rollout」) is fine |
| 邊界 (when used as a metaphor for "workload boundary / area where a limit shows up") | 情境 / 面向 | 邊界 is uncommon in tech prose and reads as forced metaphor; 情境 (situation) and 面向 (aspect) are flat structural nouns. Note: 邊界 in concrete senses (geographic, set-theoretic) is fine; only the metaphorical "workload boundary" sense should swap |
| 補 / 補丁 (when describing what teams build around a technology to fill a gap) | 涵蓋 / 處理 / 承擔 / 「做了哪些努力」 | 補 / 補丁 carry a band-aid / hotfix tone that downplays the engineering work; flat verbs like 承擔 / 處理 describe what teams actually did without judgmental framing |
| 案例 | `use case` / `use cases` | author prefers the English term; 案例 reads as formal/academic |
| 反映 (in the sense of "X reflects / reveals Y") | 反應 | author preference; both convey the meaning, 反應 reads more direct in their voice |
| 使用者 (when referring collectively to "all users of a technology", e.g. 「Iceberg 使用者」) | 使用 X 的公司 (e.g. 「使用 Iceberg 的公司」) | 使用者 as a collective group reads as abstract individual users; 使用 X 的公司 is concrete and matches the organisational scale the author writes about. Note: 使用者 in singular per-user contexts (e.g. 「對使用者而言」) is fine |
| 提速 | 加快 / 「加快查詢 Nx」 | 提速 reads as marketing copy or spec-sheet shorthand; 加快 is plainer and matches the narrative voice |
| 資料點 (when used as a metaphor for "one more instance of a pattern") | 「同一回事」/「另一個例子」/「也呈現出同一個 pattern」 | 資料點 is data-science jargon; everyday phrasing fits the author's conversational register. Note: 資料點 in literal sense (a real data point in a chart) is fine |
| 意味著 | 代表著 | 意味著 has a slightly literary / inferential tone; 代表著 reads as everyday spoken Chinese and matches the author's conversational register |
| 擴散 (when used as abstract metaphor for "proliferation / spreading", e.g. 「資料來源的擴散」/「消費者的擴散」) | 「越來越多」/「越來越分歧」/「種類越來越雜」 — plain spoken phrasing | 擴散 is abstract translation-ese; the author wants plain spoken Chinese for these qualitative descriptions. Note: 擴散 in literal physics / chemistry / epidemiology contexts is fine |
| 技術 X (used as a label-noun for "the technical/quantitative side", e.g. 「技術 scale」/「技術指標」) | name the axis directly (e.g. 「資料規模」/「資料量、tables 數、metadata 大小」) | 「技術 X」 as a category label reads as forced and unspecific in Chinese; naming the actual axis is clearer and more concrete |

#### Avoid body / physical-action verbs for abstract technical behaviour

When describing systems, proposals, workloads, structures, problems, or challenges, do not reach for verbs that imply a physical body or object motion. These read as 擬人化 / 感性 and break the grounded technical voice.

| Don't write | Write instead |
|---|---|
| 攤 (spread out) — e.g. 攤了出來 | 介紹、完整介紹 |
| 浮上來 / 冒出來 / 跳出來 (surface, emerge, jump out) | 出現、變得常見、逐漸變得常見 |
| 踩到 (step on) — e.g. 踩到的挑戰 | 遇到、面對 |
| 撐起 (hold up) | 足以支撐 |
| 站穩 (stand firm) — e.g. pipeline 站穩了 | 完成、穩定、上線 |
| 拉進 / 拉起來 (drag in / pull up) | 大規模採用、擴展 |
| 推 / 拉 / 扯 / 塞 / 扛 / 扶 / 托 / 捧 | technical-neutral verbs |

When you catch yourself writing one of these (or a near-cousin not on the list), pause and pick a flat technical verb: 介紹、說明、出現、遇到、面對、支撐、處理、導入.

#### Don't make technology the subject of doing things to people

The team / engineers are the agents; the tools are what they reach for. Flip the subject if it slipped.

- ❌ "Iceberg 把 Slack 從 Hive 時代的瓶頸帶了出來"
- ✅ "Slack 導入 Iceberg table format 改善了 Hive 時代的問題"

Don't write "Iceberg 拯救了 X" / "Kafka 接管了 Y" / "Hive 困住了 Z".

#### Describe sequences in words, not with arrows

Don't use `→` in prose to show a sequence of layers, steps, or transformations. Spell it out so it reads as a sentence. Arrows are spec / diagram shorthand and feel out of place in narrative paragraphs.

- ❌ "Iceberg 把資訊串在 metadata file → manifest list → manifest files → data files 這個 tree 上"
- ✅ "Iceberg 把資訊串成一個 tree：metadata file 指向 manifest list，manifest list 列出 manifest files，每份 manifest file 再列出 data files"

Arrows are fine inside code blocks, diagrams, or admonitions that quote a literal spec; the anti-pattern is arrow-as-prose-glue.

### 5.2 句子構造 (Sentence structure)

#### No 「並不是 X，而是 Y」 / 「不只是 X，而是 Y」 contrast constructs

These read as 說書腔 — they manufacture tension instead of stating the fact. State the actual position directly.

- ❌ "讀取端最大的成本，並不是 stitch 邏輯本身，而是 row group 不對齊"
- ✅ "讀取端的主要成本來自 row group 不對齊。stitch 邏輯本身相對便宜。"

The same anti-pattern applies to the English form *"this is not just X, it is Y"*.

#### No metaphor-first openings

Don't open a section with "Picture this:", "Imagine a...", a coffee-shop analogy, a detective analogy, or similar. Open with the actual subject — what it is, where it came from, what problem it solves.

#### No em-dash sentence breaks for rhetorical effect

Don't use ` — ` to deliver a punchline, contrast, or aside. End the sentence and start a new one, or use a comma / parenthesis / colon. Em-dashes inside compound noun phrases or quoted source material are fine; the anti-pattern is em-dash-as-rhetorical-pause.

#### No double-negative framing

Don't write 「不是 X 沒看見的」 / 「不是不知道」 / 「並非沒有意識到」 or similar double negatives. State the position directly.

- ❌ "這三個不足都不是 Iceberg community 沒看見的"
- ✅ "面對先天上的不足，Iceberg community 也正積極著手這些面向"

Double negatives force the reader to mentally invert twice and feel like 說書腔 hedging. Direct positive framing is shorter and lands harder.

#### No personification of systems

Tools and formats are not "friends who finish your sentences", "data concierges", "marathon champions", or "speed demons". Describe what they do in direct terms.

The same rule applies to abstract subjects like queries, requests, jobs, events: they don't 「到達」 ("arrive"), 「等候」 ("wait"), 「跑進來」 ("come in"), 「跑掉」 ("leave"). Use temporal phrasing instead.

- ❌ "查詢到達時 metadata 已在記憶體裡"
- ✅ "到時候查詢時 metadata 已在記憶體裡" / "查詢發生時 metadata 已在記憶體裡"

#### Prefer agentive verb constructions over nominalized abstractions

When describing a new capability or what something can now do, write it as a direct agent-verb-object sentence ("X 現在可以 Y") rather than as a noun-equation ("把 Y 做 Z 已經是 X 內的能力"). The nominalized form reads as translation-ese: it forces the reader to mentally re-expand the noun phrase back into action terms.

- ❌ "把原本由 query engine client 負責的 metadata traversal 與 scan planning 搬一部分到 catalog side 已經是 spec 內的能力"
  (Long descriptive noun clause + abstract "已經是 X 內的能力" predicate — reads as a translated machine output.)
- ✅ "query engine client 原本要做的 metadata traversal 與 scan planning，現在可以交由 catalog 處理"
  (Direct subject-verb-object, reads as natural Chinese.)

The same principle applies elsewhere:
- 「X 是 Y 的能力 / X 屬於 Y 的範圍 / X 是 Y 提供的功能」 → 「Y 可以做 X / Y 現在能 X」
- 「N 類問題包含 A、B、C」 → 「第一類問題是…, 像是 A?B?C?」 (see also the "promise N items, deliver them as such" rule above)

If a sentence reads awkwardly out loud, it's almost always because a noun has eaten a verb. Restore the verb to fix it.

#### Long compound noun phrases need either wrapping or rewriting

Long compound noun phrases — especially Chinese+English mixes like 「原本由 query engine client 負責的 metadata traversal 與 scan planning」— are hard to parse. The reader can't tell where the noun ends and the verb begins, and gives up halfway through. Two fixes, and you must apply one of them:

1. **Wrap the noun with 「...」** to mark its boundary explicitly:
   - ❌ "把原本由 query engine client 負責的 metadata traversal 與 scan planning 搬一部分到 catalog side"
   - ✅ "把「原本由 query engine client 負責的 metadata traversal 與 scan planning」搬一部分到 catalog side"
2. **Rewrite** to split the long noun across two short clauses, restoring verb agency:
   - ✅ "query engine client 原本要做的 metadata traversal 與 scan planning，現在可以交由 catalog 處理"

Option 2 is usually better because it also fixes the noun-eating-the-verb problem (see rule above). Use option 1 (wrap) only when the compound noun is genuinely the natural way to phrase it — e.g. quoting a question, a column name, or a defined term.

Rule of thumb: if a noun phrase before the main verb runs longer than ~10 characters and mixes English + Chinese, either wrap or rewrite. Never let it sprawl unwrapped through a long sentence.

#### "第 X 個判斷 / 原因 / 重點是 ___" — the blank must carry meaning by itself

When opening a section or paragraph with 「第 X 個 Y 是 ___」, the blank has to be either (a) a concrete term the reader can interpret immediately given the surrounding text, or (b) accompanied by an inline expansion in the same sentence. A bare English abstract noun like "layer" / "scope" / "context" / "framework" usually fails (a) — the reader sees the word and translates it to a single Chinese character ("層" / "範圍") but can't tell what specific judgment / reason / point it actually points to.

- ❌ "第二個判斷是 layer。如果需求是 batch analytics，Iceberg 很適合。但如果需求進入 sub-second latency..."
  (What is "layer" pointing at? The reader has to skim ahead to guess. The word does no work.)
- ✅ "第二個判斷是哪些 workload 該交給 Iceberg、哪些得用別的系統處理。如果需求是 batch analytics，Iceberg 很適合。但如果需求進入 sub-second latency..."
  (The opening directly states the judgment in concrete terms; the body just gives the answer.)

This rule pairs with the parallel "第一個判斷是 scale" / "第二個判斷是 layer" structure — parallelism is fine, but each parallel item must individually carry its meaning. If one slot in the parallel set ends up empty (a word that doesn't communicate), the parallelism becomes a tic rather than a clarifying device.

Quick test: read the framing sentence aloud in isolation. If a reader who hasn't read the rest of the section would have no idea what you're pointing at, expand or replace it.

#### Adoption-narrative form

When describing "team X adopts technology Y", put the verb on the engineering action, not on an abstract noun.

- ❌ "X 採用 Y 是沿著 N 階段逐步推進的"
- ✅ "X 是透過 N 階段逐步導入 Y 的"

Avoid noun-ifying the core action ("採用"/"引入"/"導入") and then using "推進"/"沿著"/"根據 X 推進" as the actual verb.

#### Be concrete about phase transitions

Don't say "起步 / 開始 / 起點" without naming what changed. Name the from→to fact.

- ❌ "先從一條 streaming pipeline 起步"
- ✅ "先從轉換 batch 到 streaming pipeline 開始"

#### Limit the "spec 定義了 X，但 Y 沒有規定" sentence pattern — vary or omit

When the central thesis is "the spec defines structure but leaves operational policy unspecified", it's tempting to express it as 「Iceberg spec 對 X 規定得很清楚，但對 Y 沒有規定」/「Iceberg 提供了 X，但 Y 是平台的事」 in *every* section. Reading the post end-to-end, this pattern shows up over and over and starts to feel like a tic.

Rule: use the pattern at most 2–3 times per post — once to establish the thesis, once or twice in the strongest evidence sections. Elsewhere, either omit (the reader has internalised the framing by then) or vary the form. Acceptable substitutes when you need to make the same point:

- "Y 由平台自己決定 / Y 是平台的事"
- "Y 沒被寫進 spec / Y 不在 spec 範圍內"
- "X 完整，Y 留白"
- "X 寫得很清楚，Y 各家自己處理"
- 或直接把這個前提當作隱含背景，省略整句

If you've already said it in this section, don't say it again at the end of the section as a summary line — that's where the over-counting tends to happen.

#### No announcement-style preambles ("這篇文章的順序是", "在進入 X 之前")

Don't open a paragraph or section with meta-narration like 「這篇文章的順序是」, 「在進入三個 use cases 之前」, 「下面三節要看的」, or 「先把 X 整理出來，後面才有對應的尺度可以參照」. State what you're doing directly, or lead with the actual content / source.

- ❌ "這篇文章的順序是：先看 A、接著看 B、最後看 C"
- ✅ "這篇文章我們會先看 A、接著看 B、最後看 C"
- ❌ "在進入三個 use cases 之前，先把 Netflix 的 Iceberg 規模整理出來，後面才有對應的尺度可以參照"
- ✅ "Netflix 在 2023 年 AWS re:Invent 的分享中陸續揭露了規模..." (lead with the source/content)

These preambles read as 預告片話術 — they spend words narrating *what's about to happen* instead of just doing it. The reader is already here; just start.

#### Cite talks by title, never by conference internal code

When referencing a talk in body prose, use the talk's title (or a short paraphrase of it) — not the conference's internal session code (e.g. `NFX306`, `STG214`, `NFX303`). Internal codes carry no meaning for the reader and feel like project shorthand leaking into prose. Linking by title is enough.

- ❌ "Netflix 在 [NFX306](https://...) 中提到..."
- ✅ "Netflix 在 [Netflix's journey to an Apache Iceberg-only data lake](https://...) 中提到..." / "Netflix 在 [Iceberg-only data lake 的分享](https://...) 中提到..."

Conference codes are fine in `links:` frontmatter where they sit alongside the full talk title.

#### SQL keywords and engine-specific identifiers use backticks, not bold

`MERGE`, `SELECT`, `INSERT` use backticks. The same applies to engine-specific metadata table identifiers like `$files`, `$partitions`, `$history`, `$snapshots` (Trino's Iceberg connector) and `prod.db.table.history`, `prod.db.table.files` (Spark SQL). **Bold** is for emphasising concept names; code style is for program syntax and identifier names.

### 5.3 段落安排 (Paragraph patterns)

#### Each h3: 承接句 + problem recap → solution

Do not jump straight into the solution. Open each h3 with:

1. A short **承接句** that bridges from the previous h3 or section.
2. A brief **problem recap** specific to this h3 — what is the concrete pain this h3's mechanism addresses?
3. Then the **solution / mechanism / detail**.

This pacing was developed during `rethinking-iceberg-metadata-v4.md` and is the author's standard h3 shape. Skipping straight to mechanism reads as abrupt.

#### No 「伏筆」 narrative tricks

Avoid phrases like "這也是後來 X 的伏筆之一", "為日後埋下伏筆", "這就是後來 X 的起點". These are 說書腔 / 預告片話術. Let the reader connect the dots; don't add 旁白.

#### Each h2: short prose intro before details

Open each h2 with one short prose paragraph that introduces the section's purpose and how it connects to what came before. Then move into h3 subsections or bullet lists. Don't lead with bullets directly under an h2.

#### Object references must be explicit

When writing "重寫整份檔案", say *which* file. `data file`, `manifest file`, `metadata file`, `column update file` all behave differently and the reader can't infer which one from context. The same rule applies to `row` vs `column`, `entry` vs `data file`, etc. — pick the precise term, not the generic one.

#### Don't over-cross-link to your own previous posts

Cross-linking to sibling / related posts in this blog is valuable — but each cross-link should sit at the place where it adds the most context for the reader, not at every place where the connection happens to be true. If you've already linked to a sibling post once earlier in this article (e.g. in an opening framing or a synthesis paragraph), do not also link to it from a mid-section "this is similar to what I wrote in [other post]" sentence — that reads as self-promotion and pads the prose. The end-of-post "further reading" close is also fine; what's excessive is mid-section repeated nods.

Rule of thumb: one earlier in-line cross-link + one end-of-post recommendation = enough. Extra references in between get cut.

#### When you promise N "questions" / "examples" / "reasons", actually write them as such — and signpost each one

Don't promise readers "two types of questions" and then just list bare noun phrases. If the sentence says 「兩類問題」/「三個例子」/「幾個原因」, the body should deliver actual questions (with `？`), actual examples (concrete and self-contained), or actual reasons (explanatory sentences). Always signpost the boundary between items with explicit ordinal connectors so the reader can see the structure.

- ❌ "所以要問清楚兩類問題。資料規模上：資料量、tables 數、metadata 大小；use case 規模上：未來會有多少不同類型的使用者、需求差異、原生支援程度。"
  (Where are the question marks? These are bare nouns, not questions. And there's no connector between 「兩類問題」 and 「資料規模上」.)
- ✅ "所以要問清楚兩類問題。第一類問題是資料規模上的，像是：資料量會不會很大？tables 數會不會很多？metadata 會成長到什麼程度？第二類問題是 use case 規模上的，像是：未來會有多少不同類型的使用者用這些 tables？他們的需求差異有多大？"
  (Now they're actual questions with `？`, and 「第一類問題是...」/「第二類問題是...」 signpost the structure.)

The principle is structural integrity: whatever the framing sentence promises, the body must concretely deliver, and the boundaries between promised items must be visible.

#### Make semantic transitions between adjacent sentences explicit

If two sentences sit next to each other in the same paragraph, the reader should be able to see the logical link between them without inferring it: cause-and-effect, contrast, elaboration, qualification. Don't write "Statement A. Statement B." and rely on the reader to figure out the relationship — write "Statement A. 但 / 所以 / 也就是說 / 之所以 X 是因為 Y. Statement B."

- ❌ "當然這只是 N=1 的觀察。Netflix 是一家做這件事做得特別徹底、又把過程公開出來的公司"
  (Why are you telling me about Netflix's transparency? The reader has to guess the link.)
- ✅ "當然這只是針對一家公司的觀察而已。但 Netflix 之所以值得這樣觀察，是因為他們在這件事上做得特別徹底、又把過程公開得最完整。"
  (Now the link is explicit: "Yes, it's one company; but here's *why* that one company still tells us something.")

Particularly important right after caveats, at section transitions, or anywhere the next sentence might otherwise feel like a non-sequitur. Also: avoid jargon-shorthand like "N=1" in body prose — write it out in plain Chinese (「只是針對一家公司的觀察」).

### 5.4 Process preferences

#### Don't list options for English-translation choices

When the author says "改成英文" / "翻成英文" / "我不知道要翻譯成什麼" without giving the term, pick a sensible English term and apply it. Don't list 2–3 options and ask. Prioritise (1) terms already in §5.1's table, (2) the standard Iceberg / data-engineering term, (3) the shortest direct word.

#### Don't over-confirm during drafting

Phase 4 of §6 already says this, but it's worth repeating here as a voice rule: once the headings and structure are locked, write a full h2 section in one pass and hand off for review. Confirmation-heavy back-and-forth in the middle of a section breaks the author's review rhythm.

#### Read every source you cite — never write from the URL alone

When the author hands you a new URL (case study, blog post, paper) to incorporate, fetch and read it **before** writing the section that cites it. Don't paraphrase from the title or guess what's inside. The article will have specific framings, named engineers, exact metrics, and direct quotes that determine what's accurate to attribute to it; without reading you will conflate speakers, misattribute claims, or invent generic statements that don't appear in the source.

Concrete failure mode that has happened: claiming "the same Netflix engineer Pablo Delgado" appeared in two talks when he was actually only in one — the 2024 talk speakers were Roshi + Dao Mi, the 2025 talk was Pablo + Lei Xu, and the case study quoted Dao Mi. Source diligence would have caught this.

When the source is paywalled or unfetchable, say so and ask the author for the relevant passage rather than guessing.

## 6. Workflow when drafting a new post

The author has converged on a specific iterative workflow across multiple posts (most recently `lessons-from-slack-iceberg.md` and `rethinking-iceberg-metadata-v4.md`). Follow it phase by phase — do **not** try to compress phases together or jump straight to drafting. Each phase has an explicit handoff to the author.

### Phase 1 — Set up the workspace

1. **Confirm the slug, target half-year folder, and rough topic.** Ask the author if any of these aren't already given.
2. **Create the directory `docs/blog/posts/{year}/{half}/{slug}/` and `assets/materials.txt`.** Leave `materials.txt` empty (or with a placeholder). The author will paste in the raw source material — YouTube link, speaker names, talk notes, papers, links, screenshots — directly. Do **not** try to fetch or summarise sources unprompted. Stop after creating the folder and wait for the author to fill `materials.txt`.

### Phase 2 — Identify the article type

3. **Identify the article type** per §0 — confirm with the author, then read the matching reference file. The type determines the narrative arc; the rest of this skill provides the shared chassis.

### Phase 3 — Plan the headings interactively (do not write prose yet)

4. **Propose the full h1 / h2 / h3 heading tree as Options.** Based on `materials.txt`, draft 2–3 candidate heading trees (different ways to slice the topic) and present them via `AskUserQuestion` so the author can pick one. Each Option is a complete h1 + all h2 + their h3s — not just the top level.
5. **Propose 2–3 heading style options.** Once the structure is picked, offer concrete style variants for the heading wording itself — e.g. 主題陣述式 (subject-first declarative), 動詞開頭式 (verb-led), 問句式 (question-form). Show the same heading tree rewritten in each style so the author can compare. The author strongly prefers **declarative, content-revealing headings** over questions, but always confirm.
6. **Iterate on headings line by line until the author is satisfied.** Expect detailed feedback: English vs. Chinese term choices, verb refinement (avoid stale verbs like 導入 / 改善 if they repeat), demanding that a heading expose the actual problem rather than name a structure (e.g. "三層 Sequential I/O 拖高 Latency" instead of "固定三層結構開銷"). When the author rejects a heading, offer 2–3 alternatives rather than one replacement. When the author says "改成英文" / "翻成英文" without giving the term, pick one yourself — don't list options (see §5.4).
7. **Lock in the opening and closing structure.** Before tasks start, agree on what the opening paragraph introduces and what closing structure the post uses (e.g. sandwich 肯定 → 隱憂 → 看好 for news analysis; a `Putting It All Together` Q&A block; etc.).

### Phase 4 — Draft the post as sequential tasks

8. **Break the draft into tasks at h2-section granularity** using `TaskCreate`. The standard breakdown is:
    - One task for the **opening** (the paragraph between the cover figure and the first h2).
    - One task **per h2 section** — each task covers that h2 plus all its h3 subsections as a single deliverable.
    - One **final TLDR task** that updates the TLDR bullets to match the body that was actually written.
9. **Complete tasks strictly in order.** For each task:
    - Mark the task `in_progress` before starting.
    - Write the full h2 section in one pass — do not stop mid-section to confirm wording (see §5.4: the author wants direct writing, not confirmation-heavy back-and-forth).
    - Hand off by pointing the author to the file — do **not** re-paste the full drafted section into the conversation. The author reads from disk. When asking about a specific change mid-iteration, quote only the contested phrase (or describe the proposed change inline), never the surrounding paragraph. Re-pasting the full draft wastes the author's context budget.
    - Do **not** narrate your own writing decisions back to the author. No "conscious choices I made" trailers, no listing of voice-rule compliance, no rationalising of structural decisions. The author reacts to the output text itself, not to your meta-explanation.
    - When the author gives concrete feedback ("change X to Y", "I dislike Z"), treat it as evidence of an **abstract preference** that probably applies more broadly. Reverse-infer the rule, confirm the inferred abstraction with the author inline (e.g. "so the rule is: prefer flat technical verbs over body-action verbs — is that right?"), and once they confirm, write the rule into the appropriate section of this skill (§5.1, §5.2, or §5.3 most often). One piece of feedback should turn into one persistent skill update — never just a one-off in-conversation fix.
    - Apply revisions until the author says to move on.
    - Only then mark the task `completed` and start the next one.
10. **Write the TLDR last, as a "why should I read this" hook.** The TLDR is not a table of contents and not a technical summary — it should be three high-level bullets that each *gesture at* an insight without revealing it. The reader should finish the TLDR thinking "there's something interesting here I want to find out", not "I already know the answer, no need to read on". Keep technical terms minimal. Never write "作者" or refer to the author in third person; phrase neutrally.

    Hook phrasings that work well: 「為什麼 X 反而 Y」 / 「X 反應出 Y 在哪些 Z 仍有不足」 / 「可以從哪兩個角度想清楚」 / 「哪些是目前 X 的三個 Y」. These all signal "the answer is in the article" without giving it away.

    Summary phrasings to avoid: 「X 的取捨方式都是 Y、Z、W」 / 「X 適合做 A，但當 B 時就需要 C」 / 「可以從 A 與 B 兩個角度想清楚」 — these give away the conclusion and remove the reader's reason to read on.

    Concrete contrast from a real review:

    - ❌ Summary form: "Netflix 在 Trino、ClickHouse、LanceDB 三個情境上遇到 Iceberg 不足時，共同的取捨方式都是讓 Iceberg 維持原樣、在它外面另外加一層系統來處理"
    - ✅ Hook form: "為什麼 Netflix 這種大規模採用 Iceberg 的公司，反而在好幾個情境下還要在 Iceberg 外面另外建立新的系統"

    The second tells you the *topic* (Netflix + paradox of building around Iceberg) but withholds the *answer* (the consistent shape of those external systems). That withheld answer is what the article delivers.

### Phase 5 — Review and ship

11. **Re-read the full post against §5 and the type-specific anti-patterns.** Check §5.1–5.3 (word choice, sentence structure, paragraph patterns) and the third paragraph of the chosen article-type reference file. Rewrite anything that trips any filter.
12. **Check `mkdocs.yml`** — if it has an explicit navigation entry that lists posts, add the new post there. Otherwise the blog plugin picks it up automatically.
13. **Commit and push only the `.md` file** when the author asks to publish. Do **not** include `assets/materials.txt` or other source material — those stay local. Match the existing commit message style of sibling posts (e.g. `Publish <topic> post under {year}/{half}`).

### Common pitfalls

- **Don't skip Phase 3.** Even if the source material seems to dictate the structure, the author wants to see Options and pick one. Jumping straight to drafting forces rework.
- **Don't batch tasks.** Writing two h2 sections in one turn breaks the review rhythm. One task per turn, even if a section is short.
- **Don't pre-fill the TLDR.** A TLDR written before the body is always wrong — the body shifts during drafting, and the TLDR ends up referring to material that isn't there. Leave it as a placeholder until Phase 4's final task.
- **Don't commit `materials.txt`.** It's a working scratchpad. Stage the `.md` file explicitly rather than using `git add .`.
