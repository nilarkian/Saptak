---
title: "Markdown Note Playbook"
topic: "Meta"
date: 2026-05-10
tags: [meta, writing]
hillPos: 90
is_note: False
---

# Markdown Note Playbook

A markdown note is a prose-first reference that lives in `notes/`. It earns its format: use it when the content is argument-driven, analytical, or factual enough to benefit from structure but doesn't need visual components like scorecards, before/afters, or drill grids. Its job is to be the clearest possible statement of what you know about a topic — not a pretty container, not a summary dump.

This document is the operational reference for building one.

---

## 1. What It's For

**A markdown note is not:**
- A blog post or diary entry
- A place to paste raw research without argument
- An HTML note with the visual components removed
- A stub you'll "finish later"

**A markdown note is:**
- A prose-first reference: argument, analysis, or structured facts
- The right format when reading linearly builds understanding
- A document that earns the reader's scroll by having a point of view or a clear data shape

**Choose markdown when your content is:**
- An argument that unfolds in paragraphs
- A policy/technology briefing with comparative tables
- A speculative or analytical piece working through implications
- A subject profile where prose carries more than components would

**Choose an HTML note instead when you need:**
- Scorecards with level progressions
- Before/after transformation blocks
- Drill grids with structured steps and outcomes
- Color-coded habit stacks or integrity rule blocks
- Any content where skimmable visual structure matters more than reading order

**Where it lives:** `notes/slug.md` with `layout: note-layout` — renders with a fixed left sidebar TOC, breadcrumb, topic pill, and styled body. Appears in the Notes index, filterable by tags.

---

## 2. The Two Archetypes

All markdown notes fall into one of two shapes. Pick before you write a word.

| Archetype | Example files | When to use |
|---|---|---|
| **Analytical Note** | `puzzle.md`, `oi.md`, `ipl-jerseys.md` | Makes a claim and argues through it; content has a thesis |
| **Reference Note** | `icet.md` | Factual lookup; reader returns to check status, definitions, comparisons |

---

### Archetype A: Analytical Note

One argument, taken seriously. The reader follows your thinking and arrives somewhere. Every section builds on the last — this is not a reference, it is a read.

**Section order:**
```
[Hook paragraph — no heading, states the premise or uncomfortable truth]
---
## [The Core Concept or Problem]
## [The Mechanism or Why It Works That Way]
## [The Implications or What Changes]
## [The Risks, Limits, or Complications — optional]
## [The Conclusion — re-arrival, not restatement]
```

**Key moves:**
- Open without a heading — the first paragraph IS the argument
- Each h2 should answer one question the previous section raised
- The conclusion re-arrives at the thesis with new weight, it does not summarise what came before
- Bold the claim the reader must not miss in each section; one or two bolds per section, no more

---

### Archetype B: Reference Note

One subject, mapped thoroughly. The reader comes back to it. Every section is a lookup unit, not a chapter.

**Section order:**
```
## What It Is
## [The Key Data, Status, or Mechanisms]
## [Sector / Category Breakdown — with table]
## [Structural Features or Design Logic]
## [Comparators or Context]
## [Strategic Implications or Why It Matters]
```

**Key moves:**
- Definitions come first — the reader needs the vocabulary before the data
- Tables carry the comparative load; prose explains what tables cannot
- Each section is self-contained — the reader should be able to jump to any section and orient themselves
- No hook paragraph needed; open directly with the definition

---

## 3. Front Matter Spec

```yaml
---
layout: note-layout
title: "Title"
topic: "Topic Name"
date: YYYY-MM-DD
tags: [tag1, tag2]
hillPos: 90
is_note: true
permalink: /notes/slug/   # optional
read_time: N              # optional
---
```

**Field rules:**

| Field | Required | Rule |
|---|---|---|
| `layout` | Yes | Always `note-layout` |
| `title` | Yes | Plain title — no subtitle here, put it in the opening paragraph |
| `topic` | Yes | Appears as breadcrumb segment and as the black pill tag above the title — must be a meaningful category name |
| `date` | Yes | ISO format: `YYYY-MM-DD` |
| `tags` | Yes | Array. Use existing tags from `_data/tags.yml` where possible. New tags appear under "Other" in the sidebar |
| `hillPos` | Yes | Keep at `90` — controls z-index or ordering; change only if you have a specific reason |
| `is_note` | Yes | Always `true` — required for the Notes index to include this file |
| `permalink` | No | `/notes/slug/` — slug is lowercase, hyphenated, no underscores. Omit to use Jekyll's default from filename |
| `read_time` | No | Integer. Shows as "⏱ N min read" in the meta line below the title |

---

## 4. What the Layout Renders

Understanding what `note-layout.html` generates tells you what NOT to write yourself.

**Auto-generated (do not write these in your content):**
- Left sidebar with "← Notes" back button and auto-built TOC
- Breadcrumb: `Notes › [topic]`
- Black pill tag with `[topic]` text
- `<h1>` with your `title` front matter value
- Meta line: date formatted as "Month YYYY" + read_time if set
- Footer: "Written by Saptak · nilarkian.github.io/Saptak"

**Author writes:** Everything inside `{{ content }}` — all prose, headings, tables, lists, images, horizontal rules.

**TOC behavior:**
- Sidebar TOC is auto-built from every `h1`, `h2`, and `h3` in your content
- `h2` entries appear at full indent; `h3` entries appear indented beneath their parent h2
- Active section highlights on scroll (IntersectionObserver, 30% threshold from bottom)
- Sidebar is hidden on mobile (≤768px) — the TOC is desktop-only
- Keep headings ≤5 words: the TOC column is 240px wide

---

## 5. Markdown Elements Guide

How each markdown element renders inside `note-layout.html`, and when to use it.

---

### Bold `**text**`

Renders: same font, full black weight. No other change.

Use for: the key term being introduced, the claim the reader must not miss, the single most important phrase in a paragraph. One or two per section. If everything is bold, nothing is.

**Do not use bold for:**
- Excitement or emphasis that isn't load-bearing
- Every definition (only the ones that matter for the argument)
- Section summaries at the end of paragraphs

---

### Italic `*text*`

Renders: italic, same size and color.

Use for: titles of works referenced in prose, qualifiers that need subtle emphasis, ironic or distancing effect. Not for general emphasis — that's bold's job.

---

### H2 `## Section Title`

Renders: Arial 22px 700wt, 56px top margin, `-0.3px` letter-spacing. Appears in sidebar TOC at full indent. Scroll-margin-top: 32px (so sticky headers don't obscure it).

Use for: primary section divisions. Every note needs at least 2. Aim for 4–8.

---

### H3 `### Sub-Section Title`

Renders: Arial 17px 700wt, 36px top margin. Appears in sidebar TOC indented under its parent h2.

Use for: meaningful sub-divisions within a section that the reader might want to jump to independently. If the sub-section is short and not independently navigable, use bold prose instead.

---

### Blockquote `> text`

Renders: 4px solid #111 left border, `rgba(0,0,0,.04)` background, italic 19px, `border-radius: 0 10px 10px 0`.

Use for: direct quotes from the subject being discussed. Not for callouts, not for your own opinions, not for "important points" — those belong in prose with bold. If you're quoting yourself, don't.

---

### Horizontal Rule `---`

Renders: thin 1px `#ccc` border-top, 52px vertical margin.

Use for: major narrative breaks between acts in an Analytical Note. Not for every section — h2 headings already divide sections. Use `---` when you want a beat of silence between major shifts, or when the note's structure is acts rather than sections.

---

### Table `| col | col |`

Renders: standard browser table. No special styling beyond the note body font.

Use for: comparisons between 2–4 items, status tracking with outcomes, paradigm contrasts (Old vs New). Minimum 2 columns with a meaningful header row. Don't use tables where prose would be cleaner.

```markdown
| Framework | Coverage | Status |
|---|---|---|
| ICET | 64 technologies | Active |
| Wassenaar | Dual-use goods | Active |
```

---

### Unordered List `- item`

Renders: bulleted list, 24px left padding, 8px between items, 26px bottom margin.

Use for: enumerations where order doesn't matter — examples of a concept, risk factors, named mechanisms. Not as a substitute for prose when the items have causal or logical relationships between them.

---

### Ordered List `1. item`

Renders: numbered list, same padding as unordered.

Use for: steps in a process, ranked items where position carries meaning. If order doesn't matter, use unordered.

---

### Inline Code `` `text` ``

Renders: monospace 15px, `rgba(0,0,0,.07)` background, 4px border-radius.

Use for: file paths, field names, technical identifiers, CLI commands. Not for general emphasis.

---

### Code Block ` ```language `

Renders: dark background `#1a1a1a`, light text `#f0f0f0`, 24px padding, 12px border-radius.

Use for: multi-line code only. Not for configuration snippets you want to highlight — those should be inline code or a table.

---

### Image `![alt](url)`

Renders: full-width within the note body column (max 860px minus sidebar).

Use the Jekyll relative_url filter — never hardcode `/Saptak/assets/img/`:

```markdown
![Alt text]({{ '/assets/img/filename.png' | relative_url }})
```

---

### Link `[text](url)`

Renders: rust/orange `#c8440a`, underlined with 3px offset, 600wt, 0.2s hover fade to 55% opacity.

Use for: external references and citations. Collect all external links in a final "Read More" or "References" section — don't scatter them through prose unless the link IS the content.

---

## 6. Heading Strategy

**Default: flat h2-only structure.**

Four to eight h2 sections, no h3. This is what most notes should look like. It keeps the TOC scannable and forces each section to be self-contained.

**Add h3 when:**
- A section has 3+ sub-topics that the reader might navigate to independently
- The sub-topics are parallel in structure (e.g., multiple mechanisms, multiple case types)
- The section is long enough that a h3 provides genuine wayfinding value

**Never use h4 or deeper.** H4+ has no CSS styling in note-layout and won't appear in the TOC. If you need h4, you have a structural problem — either collapse the sub-sections or promote them to h2.

**H1 in body: rare.** The layout already renders your `title` as an h1. A second h1 in the body creates a visual double-header. Use h1 in body only for major landmark breaks between completely distinct acts (e.g., a "Bottom Line" section that summarises a long report). When you do, it appears in the TOC at full indent — keep it short.

**TOC readability test:** After writing, scan your TOC in the sidebar. Each entry should read as a clear, distinct destination. If two headings are too similar to distinguish at a glance, one of them is wrong.

---

## 7. Writing Workflow

---

**Step 1 — Pick your archetype.**

Does the content have a thesis — a single claim that the rest proves or complicates? → **Analytical Note.**

Is the content a map of a subject — definitions, data, comparisons — that the reader returns to? → **Reference Note.**

If unsure: can the reader jump to any section and orient themselves without reading the previous one? If yes → Reference. If they need the previous section to understand the current one → Analytical.

---

**Step 2 — Write front matter.**

Copy the template from §3. Set `topic` to the parent category your tags belong to (check existing notes for examples — topic is the grouping label that appears as a pill above the title). Set `date` to today. Choose 2–4 tags from `_data/tags.yml`. Set `hillPos: 90`.

---

**Step 3 — Find the argument (Analytical) or map the structure (Reference).**

Analytical: What is the single most surprising or uncomfortable claim this material supports? Write it in one sentence. If you can't, keep reading until you can. The note is not ready to write.

Reference: What are the five things a reader must know about this subject to understand how it works? List them. These become your sections.

---

**Step 4 — Sketch section headings.**

Write 4–8 h2 headings. Each heading should be completeable as: "This section tells the reader: ___." If you can't complete that sentence, the section doesn't have a purpose yet — find it before writing the prose.

---

**Step 5 — Draft the body.**

Open without a heading. The first paragraph should state the premise, the surprising fact, or the problem. This is not the place for "In this note, I will examine..." — that's throat-clearing. Start with the thing.

Build through sections in order. Each section should close by creating a question the next section answers (Analytical) or by being a complete lookup unit (Reference).

---

**Step 6 — Apply markdown elements.**

After the prose is written, add markup:
- Bold the key term or claim per section (1–2 per section)
- Add a table where you're comparing 3+ items across consistent dimensions
- Convert prose enumerations of 4+ parallel items to lists
- Add a blockquote only if you're quoting a source directly
- Add a `---` horizontal rule only between major acts (Analytical only)

---

**Step 7 — Write the closer.**

The final section is not a summary. It re-arrives at the thesis with new weight now that the reader has the full picture. Ask: what does everything above *prove* that the opening paragraph only *claimed*? Write that.

For Reference notes: the final section is "Strategic Implications" or "Why It Matters" — state what the reader should do or think differently now that they have the map.

---

**Step 8 — Run the pre-publish checklist (§8).**

---

## 8. Pre-Publish Checklist

- [ ] **Front matter:** all required fields present — `layout`, `title`, `topic`, `date`, `tags`, `hillPos`, `is_note`
- [ ] **`topic`** is a meaningful category name (check other notes for precedent)
- [ ] **`tags`** use existing values from `_data/tags.yml`; new tags go to "Other" in sidebar
- [ ] **`is_note: true`** present — without it, the note won't appear in the Notes index
- [ ] **No h4+ headings** anywhere in the file
- [ ] **No h1 in body** unless intentional major landmark — verify it looks right in the TOC
- [ ] **`permalink` slug** is lowercase, hyphenated, no underscores (if using custom permalink)
- [ ] **Opening paragraph has no heading above it**
- [ ] **Bold used for claims/terms** — not for decoration or excitement
- [ ] **Tables have a meaningful header row** and at least 2 columns
- [ ] **Any image** uses `{{ '/assets/img/...' | relative_url }}` syntax (not hardcoded `/Saptak/` path)
- [ ] **External links** collected in a References or Read More section, not scattered inline
- [ ] **File location:** `notes/slug.md` (not `_writing/`, not `notes/slug.html`)
- [ ] **Tested locally:** run `bundle exec jekyll serve` and verify sidebar TOC populates, breadcrumb shows topic, no broken image paths

---

## 9. Claude Prompts

Copy-paste ready. Fill in `[BRACKETED]` fields.

---

### Prompt A — Find the Argument

Use when: you have raw notes or research but no thesis yet.

```
Here are my raw notes on [SUBJECT]:

[PASTE NOTES]

What is the single most surprising or non-obvious claim this material supports?
State it in one sentence. Do not soften it. Do not hedge.
```

---

### Prompt B — Sketch Section Headings

Use when: you have the argument but don't know the structure yet.

```
I'm writing a markdown note about [SUBJECT].

Archetype: [Analytical Note | Reference Note]
Argument or key subject: [YOUR THESIS OR SUBJECT DESCRIPTION IN 1–2 SENTENCES]
Material I have: [BRIEF LIST OF WHAT YOU'VE COLLECTED]

Give me 4–8 h2 section headings in order. For each heading, one sentence explaining
what that section argues or maps. No filler headings ("Introduction", "Conclusion") —
every heading should name the specific move that section makes.
```

---

### Prompt C — Draft the Hook

Use when: you have the argument but can't open the piece.

```
Write a 2–3 sentence opening paragraph for a markdown note about [SUBJECT].

Rules:
- No heading above it.
- State the premise or surprising fact in sentence 1.
- Do not use "In this note, I will..." or any throat-clearing.
- Do not summarise the whole note — set up the argument.

Argument: [YOUR THESIS IN ONE SENTENCE]
```

---

### Prompt D — Write an Individual Section

Use when: you have a heading and know the section's job but are stuck on the prose.

```
Write the prose for this section of a markdown note.

Section heading: [H2 OR H3 TEXT]
What this section must argue or establish: [ONE SENTENCE]
Key facts or points to include: [LIST THEM]
What the next section covers: [BRIEF DESCRIPTION — so this section can close toward it]

Rules:
- 150–350 words.
- **Bold** the one claim the reader must not miss.
- No bullet list unless you have 4+ parallel items that genuinely need enumeration.
- End in a way that creates a question the next section answers (Analytical)
  OR as a self-contained lookup unit (Reference).
```

---

### Prompt E — Cold Review

Use when: draft is complete and you want a checklist pass before publishing.

```
Review this markdown note draft. For each item, say PASS or FAIL with one specific fix if FAIL.

CHECKLIST:
1. Opening paragraph has no heading above it and states a clear premise or surprising fact
2. Every h2 section has a distinct purpose — no two sections overlap
3. Bold used only for key claims or terms (not decoration, not excitement)
4. Tables have a meaningful header row
5. No h4+ headings
6. No hedging phrases: "arguably", "in a way", "sort of", "somewhat", "one could say"
7. No throat-clearing: "In this note, I will...", "This note explores..."
8. Final section re-arrives at the argument (Analytical) or states strategic implications (Reference)

DRAFT:
[PASTE FULL MARKDOWN]
```

---

*This playbook reflects the structure and conventions of notes in this repository as of May 2026. Update it when a new pattern appears consistently across three or more new notes.*
