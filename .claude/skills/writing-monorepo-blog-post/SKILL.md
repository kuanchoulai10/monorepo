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

## 5. Writing voice — anti-patterns to avoid

The author has explicitly excluded the following. Do not introduce them when drafting or editing:

- **No metaphor-first openings.** Do not open a section with "Picture this:", "Imagine a...", a coffee-shop analogy, a detective analogy, or similar. Open with the actual subject — what it is, where it came from, what problem it solves.
- **No personification of systems.** Tools and formats are not "friends who finish your sentences", "data concierges", "marathon champions", or "speed demons". Describe what they do in direct terms.
- **No em-dash sentence breaks for rhetorical effect.** Do not use ` — ` to deliver a punchline, contrast, or aside. If a sentence needs a break, end it and start a new one, or use a comma / parenthesis / colon as appropriate. (Em-dashes inside compound noun phrases or inside quoted source material are fine; the anti-pattern is em-dash-as-rhetorical-pause.)

Beyond avoiding the above, match the existing posts: direct second-person ("you"), heavy bolding of key terms, concrete examples, and a tendency to finish each section with a sentence that sets up the next one.

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
6. **Iterate on headings line by line until the author is satisfied.** Expect detailed feedback: English vs. Chinese term choices, verb refinement (avoid stale verbs like 導入 / 改善 if they repeat), demanding that a heading expose the actual problem rather than name a structure (e.g. "三層 Sequential I/O 拖高 Latency" instead of "固定三層結構開銷"). When the author rejects a heading, offer 2–3 alternatives rather than one replacement. When the author says "改成英文" / "翻成英文" without giving the term, pick one yourself — don't list options (see `feedback_blog_voice_anti_patterns.md` §流程偏好).
7. **Lock in the opening and closing structure.** Before tasks start, agree on what the opening paragraph introduces and what closing structure the post uses (e.g. sandwich 肯定 → 隱憂 → 看好 for news analysis; a `Putting It All Together` Q&A block; etc.).

### Phase 4 — Draft the post as sequential tasks

8. **Break the draft into tasks at h2-section granularity** using `TaskCreate`. The standard breakdown is:
    - One task for the **opening** (the paragraph between the cover figure and the first h2).
    - One task **per h2 section** — each task covers that h2 plus all its h3 subsections as a single deliverable.
    - One **final TLDR task** that updates the TLDR bullets to match the body that was actually written.
9. **Complete tasks strictly in order.** For each task:
    - Mark the task `in_progress` before starting.
    - Write the full h2 section in one pass — do not stop mid-section to confirm wording (the author wants direct writing, not confirmation-heavy back-and-forth; see memory `feedback_blog_voice_anti_patterns.md` §流程偏好 and prior decision: "以一組 h2+h3 段落為單位，依照順序完成 tasks").
    - Hand off to the author for review. Apply revisions until the author says to move on.
    - Only then mark the task `completed` and start the next one.
10. **Write the TLDR last, as a "why should I read this" hook.** The TLDR is not a table of contents and not a technical summary — it should be three high-level bullets answering "why does this matter to me as a reader". Keep technical terms minimal. Never write "作者" or refer to the author in third person; phrase neutrally.

### Phase 5 — Review and ship

11. **Re-read the full post against the anti-patterns.** Check both §5 (voice-level anti-patterns), the type-specific anti-patterns in the third paragraph of the chosen reference file, and the per-author memories (`feedback_blog_voice_anti_patterns.md`, `feedback_blog_vocabulary.md`). Rewrite anything that trips any filter.
12. **Check `mkdocs.yml`** — if it has an explicit navigation entry that lists posts, add the new post there. Otherwise the blog plugin picks it up automatically.
13. **Commit and push only the `.md` file** when the author asks to publish. Do **not** include `assets/materials.txt` or other source material — those stay local. Match the existing commit message style of sibling posts (e.g. `Publish <topic> post under {year}/{half}`).

### Common pitfalls

- **Don't skip Phase 3.** Even if the source material seems to dictate the structure, the author wants to see Options and pick one. Jumping straight to drafting forces rework.
- **Don't batch tasks.** Writing two h2 sections in one turn breaks the review rhythm. One task per turn, even if a section is short.
- **Don't pre-fill the TLDR.** A TLDR written before the body is always wrong — the body shifts during drafting, and the TLDR ends up referring to material that isn't there. Leave it as a placeholder until Phase 4's final task.
- **Don't commit `materials.txt`.** It's a working scratchpad. Stage the `.md` file explicitly rather than using `git add .`.
