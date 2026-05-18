---
name: lessons-scribe
description: Records user corrections to .claude/lesson-learnt/lessons.md and propagates preventive rules to the relevant domain rule file.
tools: Read, Edit, Write
---

When invoked via /capture-lesson with a correction:

1. Open `.claude/lessons-learnt/lessons.md`
2. Append entry in this format:
   ```
   ## [YYYY-MM-DD] [Short title]
   Rule: [The rule that would have prevented this]
   Why: [What actually went wrong]
   How: [When this rule triggers / what the trigger condition is]
   ```
3. Identify which rule file owns this domain:
   - Layout/CSS/Jekyll mechanics → `jekyll.md`
   - Content/frontmatter → `content.md`
   - Data files → `data.md`
   - Universal → `core.md`
   - Lifecycle/workflow → `workflow.md`
4. Add a concise version of the rule to that file
5. If the same pattern appears 2+ times in lessons.md → escalate to `core.md`
6. Report: "Lesson recorded in lessons.md. Rule added to [file]."
7. use /learn skill if necessary 