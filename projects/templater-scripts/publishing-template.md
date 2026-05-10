remember golden rules: 
1. non code content must not exceed 2x code count
2. be less robotic and less verbose

````md
# Guide System Spec

Voice:
peer operator, not teacher.
assume technical reader.
optimize for:
- execution speed
- skimmability
- safe modification
- predictable behavior

Style:
- direct
- operational
- high-agency
- low-noise
- conversationally precise

Avoid:
- theory-first explanation
- motivational filler
- corporate wording
- abstraction without behavior

Preferred verbs:
run, trigger, register, skip, guard, prompt, insert, swap, replace, remove, chain

Avoid:
leverage, utilize, seamless, robust, scalable, elegant, comprehensive

---

# Core Writing Pattern

Always:

```text
ACTION
RESULT
CODE
BEHAVIOR
MECHANISM
MODIFICATION
LIMITS
```

Behavior before implementation.

Good:
> Enables disabled plugins, then reloads the workspace.

Bad:
> Uses `enablePluginAndSave()` to...
````

---

# Paragraph Rules

* 1–3 sentences max
* every sentence adds operational value
* no transition filler
* observable outcomes > conceptual explanation

Good:

> The key value does not matter. Presence alone enables the flag.

Bad:

> This works because JavaScript objects are evaluated...

`````

---

# Markdown Skeleton

````md
---
layout:
title:
description:
category:
tags:
date:
---

# Intro

[what to run]
[observable result]
[execution context]

```language
[real executable code]
`````

## Feature / Workflow

[behavior]

## How It Works

[mechanism]

## Customisation

* swap X for Y
* add Z
* remove guard

## Edge Cases

* excluded paths
* cancel behavior
* failure branches

## Notes

* scope
* dependencies
* limits

`````

---

# Structural Ordering

```text
1 frontmatter
2 operational summary
3 executable code
4 behavior
5 mechanism
6 customization
7 edge cases
8 notes
```

---

# Code Rules

Only executable code in fenced blocks.

Always declare language:

````md
```javascript
`````

No:

* pseudocode
* decorative snippets
* explanatory comments

Use structural comments only:

```javascript
// ── REGISTER COMMAND ───────────────
```

Avoid:

```javascript
// stores plugin names
```

---

# Naming Rules

```javascript
pluginsToEnable
headingItems
nextAction
```

Patterns:

* booleans → condition names
* arrays → plural nouns
* commands → kebab-case
* temp vars → short semantic names

---

# Explanation Rules

Explain through:

* observable behavior
* concrete branches
* inline reasoning

Use branch framing often:

```text
- invalid path
- cancelled prompt
- valid selection
```

State both:

* what happens
* what does not happen

Good:

> Inserts below `---`, not at top of file.

Good:

> Guard prevents duplicate commands on rerun.

````

---

# Metadata Rules

```yaml
---
layout: templater
title: Plugin Manager
description: Enables plugins from a single command.
category: automation
tags: [plugins, commands, settings]
date:
---
````

Rules:

* title = operationally specific
* description = observable outcome
* tags = lowercase, functional, searchable
* navigation = metadata-driven

---

# Customisation Language

Prefer:

* swap
* replace
* add
* remove
* comment out

Avoid:

* configure
* tailor
* adjust dynamically

```

---

# Reader Contract

Reader should immediately know:
- what to paste
- what changes
- expected output
- failure behavior
- safe modification points
```

---

# Done Criteria

```text
✓ frontmatter exists
✓ first paragraph explains execution + result
✓ all code executable
✓ no pseudocode
✓ behavior before mechanism
✓ edge cases documented
✓ customization actionable
✓ variable names semantic
✓ observable outcomes explicit
✓ guards documented
✓ skimmable in under 2 minutes
✓ no paragraph without operational value
```