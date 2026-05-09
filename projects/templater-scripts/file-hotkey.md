---
layout: templater
title: Hotkeys for Files
description: Register global hotkeys that instantly open specific Obsidian files from a plain-text keybinding map.
category: Automation
tags: [templater, hotkeys, navigation, keybindings, workflow]
date: 2026-05-07
---

# Instant file hotkeys inside Obsidian

Paste this into a Templater startup script and run it once on launch.

After that:

* pressing `alt+i` can open your homepage
* pressing `ctrl+j` can jump to your journal
* pressing `alt+0` can open a high-priority project
* editing `Keybindings.md` reloads mappings automatically

No command palette.
No sidebar navigation.
No fuzzy search.

The script turns Obsidian into a lightweight launcher for your most-used files.

```javascript
<%*

const { vault, workspace, commands } = app; // use templater-provided global `app`

const KEYBINDINGS_PATH = "Keybindings.md";          // change if needed
const DEBOUNCE_MS = 200;                            // reload debounce
let keyMap = new Map();
let reloadTimer = null;
let lastReloadNoticeAt = 0;
const NOTICE_COOLDOWN_MS = 1500;                    // avoid Notice spam

// Named handlers so we can remove them if needed
function normalizeKeyEvent(e) {
  const parts = [];
  if (e.ctrlKey) parts.push("ctrl");
  if (e.altKey) parts.push("alt");
  if (e.shiftKey) parts.push("shift");

  let k = e.key;
  if (!k) k = e.code || "";
  if (k === " ") k = "space";
  k = k.toLowerCase();
  parts.push(k);
  return parts.join("+");
}

function onKeyDown(e) {
  const combo = normalizeKeyEvent(e);
  const page = keyMap.get(combo);
  if (!page) return;
  e.preventDefault();
  workspace.openLinkText(page, "/", false);
}

// Debounced reload: parse file contents into keyMap
async function reloadKeyBindings() {
  if (reloadTimer) clearTimeout(reloadTimer);
  reloadTimer = setTimeout(async () => {
    try {
      const abstract = app.vault.getAbstractFileByPath(KEYBINDINGS_PATH);
      if (!abstract) {
        keyMap.clear();
        const now = Date.now();
        if (now - lastReloadNoticeAt > NOTICE_COOLDOWN_MS) {
          new Notice("⚠️ Keybindings.md not found (key map cleared).");
          lastReloadNoticeAt = now;
        }
        return;
      }
      const content = await app.vault.read(abstract);
      const lines = content.split(/\r?\n/);
      const newMap = new Map();
      for (let i = 0; i < lines.length; i++) {
        let line = lines[i];
        if (!line) continue;
        const hashIdx = line.indexOf("#");
        if (hashIdx !== -1) line = line.slice(0, hashIdx);
        line = line.trim();
        if (!line) continue;

        let sepIdx = -1;
        for (let j = 0, spaceRun = 0; j < line.length; j++) {
          if (line.charCodeAt(j) === 32) {
            spaceRun++;
            if (spaceRun >= 2) {
              sepIdx = j - (spaceRun - 1);
              break;
            }
          } else {
            spaceRun = 0;
          }
        }
        if (sepIdx === -1) {
          const t = line.indexOf("\t");
          if (t !== -1) sepIdx = t;
          else {
            const s = line.indexOf(" ");
            if (s !== -1) sepIdx = s;
          }
        }
        if (sepIdx === -1) continue;

        const keyPart = line.slice(0, sepIdx).trim().toLowerCase();
        let linkPart = line.slice(sepIdx).trim();
        linkPart = linkPart.replace(/^\s+/, "");
        if (linkPart.startsWith("[[") && linkPart.endsWith("]]")) {
          linkPart = linkPart.slice(2, -2);
        }
        if (!keyPart || !linkPart) continue;
        newMap.set(keyPart, linkPart);
      }

      keyMap = newMap;

      const now = Date.now();
      if (now - lastReloadNoticeAt > NOTICE_COOLDOWN_MS) {
        new Notice("🔁 Keybindings reloaded.");
        lastReloadNoticeAt = now;
      }
    } catch (err) {
      console.error("Failed to reload keybindings:", err);
    } finally {
      reloadTimer = null;
    }
  }, DEBOUNCE_MS);
}

// Setup function (idempotent)
async function setup() {
  if (window.__templater_optimized_keybindings_installed) return;
  window.__templater_optimized_keybindings_installed = true;

  await reloadKeyBindings();

  const vaultHandler = (file) => {
    if (!file || !file.path) return;
    if (file.path === KEYBINDINGS_PATH || file.path.endsWith("/" + KEYBINDINGS_PATH)) {
      reloadKeyBindings();
    }
  };
  window.__templater_vk_handler = vaultHandler;
  app.vault.on("modify", vaultHandler);

  window.addEventListener("keydown", onKeyDown, { passive: false });

  if (!app.commands.commands["templater-enable-keybindings-optimized"]) {
    app.commands.addCommand({
      id: "templater-enable-keybindings-optimized",
      name: "🔗 Enable Keybindings (Optimized Templater)",
      callback: async () => {
        await reloadKeyBindings();
        new Notice("Keybinding listener enabled (optimized).");
      }
    });
  }
}

await setup();

%>
        
```

## Sample `Keybindings.md`

Create a file named `Keybindings.md`.

Each line maps:

```text
hotkey  [[note]]
```

Example:

```text
alt+i              [[2025 (Homepage🏡)]]
alt+n              [[blank page]]
alt+m              [[🌄PROJECTS.base]]
alt+l              [[tp.tasks tomorrow & agenda]]

alt+0              [[(⚡blitz)__ get a job]]
alt+1              [[predict using markov]]
alt+2              [[links to add]]
alt+3              [[payoff stability]]

alt+shift+p        [[projects]]

ctrl+shift+d       [[journal📁 & MEMOS.base]]
ctrl+shift+p       [[H🔢__ daily Morning & Night writing]]
ctrl+shift+q       [[NEW PAGES.base]]
ctrl+shift+f       [[📁FOLDERS.base]]
ctrl+shift+e       [[Keybindings]]

ctrl+\             [[Master Base.base]]
ctrl+j             [[2025 Journal]]
```

## What It Does

The script watches a single markdown file and builds an in-memory hotkey map.

When a key combo matches:

```text
alt+i
```

it instantly opens:

```text
[[2025 (Homepage🏡)]]
```

No Obsidian command registration needed for each file.

The mappings stay editable as plain text.

---

## Supported Combos

Works with combinations like:

```text
ctrl+j
alt+1
ctrl+shift+p
alt+shift+m
```

The script normalizes keys to lowercase internally.

So:

```text
CTRL+J
ctrl+j
Ctrl+J
```

all resolve identically.

---

## Comment Support

Anything after `#` is ignored.

Example:

```text
ctrl+j   [[2025 Journal]]   # daily journal
```

Useful for labeling workflows without affecting parsing.

---

## How It Works

The system has 3 moving parts.

### 1. Key Normalization

Browser keyboard events are converted into stable strings:

```text
ctrl+shift+p
alt+1
ctrl+\
```

That becomes the lookup key.

---

### 2. Markdown Parsing

The script reads `Keybindings.md` line-by-line and extracts:

```text
hotkey → note target
```

Then stores them in:

```javascript
Map()
```

for constant-time lookup.

---

### 3. Global Listener

A single `keydown` listener waits for matching combos.

If a match exists:

```javascript
workspace.openLinkText()
```

opens the note immediately.

---

## Customisation

### Change the bindings file

Swap:

```javascript
const KEYBINDINGS_PATH = "Keybindings.md";
```

for:

```javascript
const KEYBINDINGS_PATH = "System/Hotkeys.md";
```

---

### Reduce reload delay

Swap:

```javascript
const DEBOUNCE_MS = 200;
```

for:

```javascript
const DEBOUNCE_MS = 50;
```

Lower values feel more responsive but increase reload frequency.

---

### Disable reload notices

Remove:

```javascript
new Notice("🔁 Keybindings reloaded.");
```

This keeps reloads silent.

---

### Add aliases

You can map multiple keys to the same file:

```text
ctrl+j   [[2025 Journal]]
alt+j    [[2025 Journal]]
```

---

## Failure Behavior

### Missing file

If `Keybindings.md` does not exist:

* mappings clear
* listener stays active
* warning notice appears

---

### Invalid lines

Malformed entries are skipped silently.

Example:

```text
this-is-invalid
```

does nothing.

---

### Duplicate mappings

Last mapping wins.

Example:

```text
ctrl+j   [[Journal A]]
ctrl+j   [[Journal B]]
```

opens:

```text
[[Journal B]]
```

---



## Notes

* Requires:

  * [Templater Plugin](https://silentvoid13.github.io/Templater/?utm_source=chatgpt.com)
* Designed for startup templates
* Uses one global keyboard listener
* Prevents duplicate installation with a window-scoped guard
* Hotkeys work anywhere inside the Obsidian window
* Markdown links are optional — raw note names also work
* Parsing supports tabs or spaces as separators

---

## Suggested High-Leverage Bindings

Good candidates:

| Hotkey         | Purpose                  |
| -------------- | ------------------------ |
| `ctrl+j`       | daily journal            |
| `alt+i`        | homepage                 |
| `alt+x`        | inbox                    |
| `ctrl+shift+p` | project dashboard        |
| `alt+0`        | highest-priority project |
| `alt+n`        | blank note               |
| `ctrl+\`       | master dashboard         |

The best bindings reduce repeated navigation friction dozens of times per day.

That is where the quality-of-life gain compounds. 🚀

Based on extracted guide structure and style patterns from your uploaded reference 
