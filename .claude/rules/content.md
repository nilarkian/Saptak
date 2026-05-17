---
paths:
  - "notes/**/*.md"
  - "_writing/**/*.md"
  - "projects/**/*.md"
---
# Content Rules — Saptak

## Pattern A — Deep-Dives (`_writing/`)
Required fields (all mandatory):
```yaml
layout: deep-dive
title: "Title Here"
number: "001"          # Zero-padded string, not integer
category: websites     # Must match an inspo category key
date: YYYY-MM-DD
tags: [tag1, tag2]     # Inline array
blurb: "One-sentence description shown in card"
```

## Pattern B — Notes (`notes/`)
Required fields:
```yaml
layout: note-layout
title: "Title Here"
topic: "Topic Name"    # Used for topic filter grouping
date: YYYY-MM-DD
tags:
  - tag1               # Block sequence (not inline array)
  - tag2
is_note: true          # Boolean lowercase — required for notes/ dir
```
Optional: `hillPos: 0-100` (numeric, controls position on visual hill on notes page)

## Anti-Pattern: Obsidian Bleed (Pattern C/D)
NEVER add these fields to new content. Remove them when normalizing existing files:
- `id:` (Obsidian timestamp slug)
- `w-status:` (draft/published — not used by Jekyll)
- `project:`, `series:` (Obsidian grouping)
- `⬅️previous page:`, `next page➡️:` (emoji field names — YAML invalid behavior)
- Wikilinks `[[Page Name]]` anywhere in frontmatter values
- `None` values (Python None — invalid YAML for Jekyll, use empty string or omit)

## Normalization Protocol (Pattern C → Pattern B)
When touching an Obsidian-exported note:
1. Remove all anti-pattern fields above
2. Add missing required Pattern B fields
3. Convert inline tags array to block sequence if needed
4. Replace any `[[WikiLink]]` in body with plain text or relative_url links

## Tag Discipline
tags MUST exist in `_data/tags.yml` or they appear under "Other" in tag sidebar.
Check tags.yml before using a new tag. Add there first if needed.

## Playbook Files (Pattern D → Pattern B)
Existing playbooks at `notes/*-playbook.md` are missing required fields.
When touching them: add `layout: note-layout`, `title`, `is_note: true` at minimum.
