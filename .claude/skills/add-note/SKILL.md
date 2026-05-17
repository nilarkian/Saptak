---
name: add-note
description: Scaffold a new note in notes/ with correct Pattern B frontmatter.
---

When invoked as /add-note [slug] [title] [topic] [tags]:

1. Create `notes/[slug].md`
2. Write Pattern B frontmatter:
   ```yaml
   ---
   layout: note-layout
   title: "[title]"
   topic: "[topic]"
   date: [today YYYY-MM-DD]
   tags:
     - [tag1]
   is_note: true
   ---
   ```
3. Add placeholder body: `## Overview\n\n[Your content here]`
4. Verify all tags exist in `_data/tags.yml`
5. Report: file created at `notes/[slug].md`
