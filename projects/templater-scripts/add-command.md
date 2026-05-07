---
layout: templater
title: Templater Script → Command Registration Pattern
description: Converts standalone Templater scripts into reload-safe command palette commands using Obsidian's Commands API.
category: Automation
tags: [templater, commands, obsidian, automation, patterns]
date: 2026-05-07
---

Turn any one-shot Templater script into a reusable command palette action without writing a plugin. The pattern registers commands once per session and prevents duplicates on reload.

## Minimal Pattern

```javascript
<%*
  const { commands } = app;

  if (!commands.commands["your-command-id"]) {
    commands.addCommand({
      id: "your-command-id",
      name: "✨ Your Command Name",
      callback: async () => {
        // logic here
      }
    });
  }

return "";
%>
```
## Just Copy-Paste this prompt along with your script



````js
##  Convert Any Obsidian Templater Script into a Command-Registering Script (with Example)

You are **Obsidian Oracle** — an expert in Obsidian Templater and the Obsidian Commands API.   Your job is to take **any Obsidian Templater script** and convert it into a **reload-safe, idempotent command-registering script** that adds one or more commands to the Obsidian Command Palette. 

## Rules You Must Follow (Strict)

### 1. Execution Context
- Wrap the entire result in a Templater execution block:
```js
  <%* ... %>
```

- Assume the global `app` object exists.
    

### 2. Command Registration

- Use `app.commands.addCommand`.
    
- Every command must include:
    - A **unique, kebab-case** `id`
    - A **human-readable** `name`
    - All original logic placed inside:
        ```js
        callback: async () => { ... }
        ```

### 3. Idempotency (Critical)
- Commands must **never register more than once**.
- Always guard registration like this:
    ```js
    if (!commands.commands["command-id"]) {
      commands.addCommand({ ... });
    }
    ```

### 4. Preserve Original Behavior
- The converted command must behave **exactly like the original script**:
    - Same prompts
    - Same file or vault modifications
    - Same navigation or window behavior
- Do **not** add features unless required for safety.

### 5. Safety & UX
- Handle cancellation or empty input gracefully.
- Use early `return` statements when appropriate.
- Add `new Notice()` only when it improves clarity.
- No logic should execute outside a command callback.

### 6. Structure
- Destructure only what is needed from `app`:
    ```js
    const { vault, workspace, commands } = app;
    ```
- Avoid unnecessary globals or side effects.

### 7. Output Requirements
- Output **only** the final converted script.
- Use a fenced code block with language `javascript`.
- No explanations, commentary, or prose outside the code block.

## Example

### Input (Original Templater Script)

```js
<%*
const file = app.workspace.getActiveFile();
const content = await app.vault.read(file);
await app.vault.modify(file, content + "\nHello World");
%>
```

### Output (Command-Registering Version)

```js
<%*
  const { vault, workspace, commands } = app;

  if (!commands.commands["templater-append-hello-world"]) {
    commands.addCommand({
      id: "templater-append-hello-world",
      name: "✍️ Append Hello World to Note",
      callback: async () => {
        const file = workspace.getActiveFile();
        if (!file) return;

        const content = await vault.read(file);
        await vault.modify(file, content + "\nHello World");
      }
    });
  }
%>
````




## Core Rule

Everything executable belongs inside:

```javascript
callback: async () => { ... }
```

Nothing should run outside the callback except command registration.

## Registration Guard

```javascript
if (!commands.commands["your-command-id"])
```

Prevents:
- duplicate palette entries
- multiple callbacks
- reload duplication

Wrap every command independently.

✅ Correct

```javascript
if (!commands.commands["a"]) { ... }
if (!commands.commands["b"]) { ... }
```

❌ Incorrect

```javascript
if (!commands.commands["a"]) {
  commands.addCommand(a);
  commands.addCommand(b);
}
```

## Converting Existing Scripts

Original:

```javascript
<%*
const file = app.workspace.getActiveFile();
const content = await app.vault.read(file);
await app.vault.modify(file, content + "\nHello");
%>
```

Converted:

```javascript
<%*
  const { vault, workspace, commands } = app;

  if (!commands.commands["templater-append-hello"]) {
    commands.addCommand({
      id: "templater-append-hello",
      name: "✍️ Append Hello",
      callback: async () => {

        const file = workspace.getActiveFile();
        if (!file) return;

        const content = await vault.read(file);

        await vault.modify(
          file,
          content + "\nHello"
        );
      }
    });
  }

return "";
%>
```

## Command ID Rules

Good:

```text
templater-heading-jump
vault-open-archive
plugin-enable-disabled
```

Bad:

```text
open
jump
test-command
```

Use:
- kebab-case
- namespacing
- globally unique IDs

## Standard Suggester Pattern

```javascript
const selected = await tp.system.suggester(
  items.map(i => i.display),
  items
);

if (!selected) return;
```

Keeps:
- UI labels separate
- full object access preserved

## Standard Guard Pattern

```javascript
if (!items.length) {
  new Notice("⚠️ Nothing found.");
  return;
}
```

Prefer early returns over nested conditionals.

## Recommended Structure

```javascript
<%*
  const { vault, workspace, commands } = app;

  if (!commands.commands["id"]) {

    commands.addCommand({

      id: "id",

      name: "Name",

      callback: async () => {

        try {

          // logic

        } catch (err) {

          console.error(err);

          new Notice("❌ Command failed");
        }
      }
    });
  }

return "";
%>
```

## When This Pattern Fits

Use this instead of a plugin when:
- commands are personal
- workflow is experimental
- no persistent state needed
- you just want palette actions quickly

Write a plugin instead if you need:
- event listeners
- settings tabs
- persistent lifecycle hooks
- background services

## Notes

- Commands are session-scoped
- Requires Templater
- Requires manual execution or startup loading
- `return ""` prevents note insertion
- `app.commands` is the registration source of truth
- Reload safety depends entirely on stable command IDs