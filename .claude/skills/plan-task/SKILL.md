---
name: plan-task
description: Interview user then write an approved task plan to .claude/plans/.
---

When invoked as /plan-task [topic]:

Interview the user with these questions (one at a time):
1. Goal: What does success look like in 1 sentence?
2. Constraints: Which files must not be touched? Any invariants to preserve?
3. Acceptance: How will we verify this is done? (Name the verification method.)
4. Scope: Which files will be touched? (List them.)

After answers received:
- Write plan to `.claude/plans/YYYY-MM-DD-[slug]-plan.md`
- Do NOT start implementation until user confirms the plan
- Plans are never overwritten — each task gets a new dated file
