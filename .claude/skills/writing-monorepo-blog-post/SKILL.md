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

## Putting It All Together

!!! question "<A natural follow-up question a reader would ask>"

    <Direct answer.>

!!! question "<Another follow-up question>"

    <Direct answer, optionally with a short bullet list.>
```

Notes on structure:

- Title is either `<Series>: <Topic>` or an actionable phrase (`N Practical Ways to ...`, `What's New in ...`). Keep it concrete.
- TLDR bullets are takeaways, not a table of contents. Phrase them as "you will learn X" items.
- After `<!-- more -->`, lead with a cover figure when one exists, then an opening paragraph that states what the thing is and why it matters. Do not open with a metaphor or analogy.
- Within each `##` section: one short prose paragraph to set context, then a bulleted list of properties / steps / components. This pattern repeats throughout the post.
- The post often closes with a `Putting It All Together` (or similar) section that uses `!!! question` admonitions for FAQ-style clarifications.

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
| `table` / `tables` | 表、資料表 |
| `partition` / `partitioning` | 分區 |
| `query planning` | 查詢規劃 |
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

Headings already mix English and Chinese; body prose should follow the same register.

#### Avoid these Chinese substitutions

| Avoid | Use instead | Reason |
|---|---|---|
| 量級 (when describing scale levels) | 規模 | 量級 has a different register; 規模 reads cleaner |
| 契機 (when describing why a tech was adopted) | 動機 | 契機 is too literary for engineering writing |
| 資料表越長越大 | 「隨著資料規模越來越大」/「隨著 tables 越來越多」 | personifies the table |
| 受控的速度 | 穩定可控的速率 | "速度" is too colloquial here |

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

#### No personification of systems

Tools and formats are not "friends who finish your sentences", "data concierges", "marathon champions", or "speed demons". Describe what they do in direct terms.

#### Adoption-narrative form

When describing "team X adopts technology Y", put the verb on the engineering action, not on an abstract noun.

- ❌ "X 採用 Y 是沿著 N 階段逐步推進的"
- ✅ "X 是透過 N 階段逐步導入 Y 的"

Avoid noun-ifying the core action ("採用"/"引入"/"導入") and then using "推進"/"沿著"/"根據 X 推進" as the actual verb.

#### Be concrete about phase transitions

Don't say "起步 / 開始 / 起點" without naming what changed. Name the from→to fact.

- ❌ "先從一條 streaming pipeline 起步"
- ✅ "先從轉換 batch 到 streaming pipeline 開始"

#### SQL keywords use backticks, not bold

`MERGE`, `SELECT`, `INSERT` use backticks. **Bold** is for emphasising concept names; code style is for program syntax.

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

### 5.4 Process preferences

#### Don't list options for English-translation choices

When the author says "改成英文" / "翻成英文" / "我不知道要翻譯成什麼" without giving the term, pick a sensible English term and apply it. Don't list 2–3 options and ask. Prioritise (1) terms already in §5.1's table, (2) the standard Iceberg / data-engineering term, (3) the shortest direct word.

#### Don't over-confirm during drafting

Phase 4 of §6 already says this, but it's worth repeating here as a voice rule: once the headings and structure are locked, write a full h2 section in one pass and hand off for review. Confirmation-heavy back-and-forth in the middle of a section breaks the author's review rhythm.

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
    - Hand off to the author for review. Apply revisions until the author says to move on.
    - Only then mark the task `completed` and start the next one.
10. **Write the TLDR last, as a "why should I read this" hook.** The TLDR is not a table of contents and not a technical summary — it should be three high-level bullets answering "why does this matter to me as a reader". Keep technical terms minimal. Never write "作者" or refer to the author in third person; phrase neutrally.

### Phase 5 — Review and ship

11. **Re-read the full post against §5 and the type-specific anti-patterns.** Check §5.1–5.3 (word choice, sentence structure, paragraph patterns) and the third paragraph of the chosen article-type reference file. Rewrite anything that trips any filter.
12. **Check `mkdocs.yml`** — if it has an explicit navigation entry that lists posts, add the new post there. Otherwise the blog plugin picks it up automatically.
13. **Commit and push only the `.md` file** when the author asks to publish. Do **not** include `assets/materials.txt` or other source material — those stay local. Match the existing commit message style of sibling posts (e.g. `Publish <topic> post under {year}/{half}`).

### Common pitfalls

- **Don't skip Phase 3.** Even if the source material seems to dictate the structure, the author wants to see Options and pick one. Jumping straight to drafting forces rework.
- **Don't batch tasks.** Writing two h2 sections in one turn breaks the review rhythm. One task per turn, even if a section is short.
- **Don't pre-fill the TLDR.** A TLDR written before the body is always wrong — the body shifts during drafting, and the TLDR ends up referring to material that isn't there. Leave it as a placeholder until Phase 4's final task.
- **Don't commit `materials.txt`.** It's a working scratchpad. Stage the `.md` file explicitly rather than using `git add .`.
