---
name: add-writing
description: Scaffold a new deep-dive in _writing/ with correct Pattern A frontmatter.
---

When invoked as /add-writing [slug] [title] [number] [category]:

1. Create `_writing/[slug].md`
2. Write Pattern A frontmatter:
   ```yaml
   ---
   layout: deep-dive
   title: "[title]"
   number: "[number zero-padded to 3 digits]"
   category: [category]
   date: [today YYYY-MM-DD]
   tags: []
   blurb: ""
   ---
   ```
3. Add placeholder body: `## [Title]\n\n[Your deep-dive content here]`
4. Report: file created at `_writing/[slug].md`
