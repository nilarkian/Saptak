---

layout: templater
title: Random Installed Theme Switcher
description: Instantly switch your vault to a random already-installed Obsidian theme.
category: automation
tags: [templater, themes, appearance, obsidian, random]
date: 2026-05-07
---

# Shuffle your vault theme instantly

Run this script and Obsidian jumps to a random installed theme.

No browsing.
No settings menu.
Just:

```text
run template
→ random aesthetic
```

Especially good if you already hoard themes and never actually use them 😄

```javascript
<%*
const fs = require('fs');
const path = require('path');

// ── PATHS ───────────────

const base = tp.app.vault.adapter.basePath;

const appearancePath =
  path.join(base, '.obsidian', 'appearance.json');

const themesPath =
  path.join(base, '.obsidian', 'themes');

// ── WAIT FOR THEMES ───────────────

async function waitForThemeCandidates({
  timeoutMs = 15000,
  intervalMs = 300
} = {}) {

  const start = Date.now();

  while (Date.now() - start < timeoutMs) {

    try {

      if (fs.existsSync(themesPath)) {

        const list =
          fs.readdirSync(themesPath).filter(f => {

            const full =
              path.join(themesPath, f);

            try {

              const s = fs.statSync(full);

              return (
                s.isDirectory() ||
                f.toLowerCase().endsWith('.css')
              );

            } catch (err) {

              return false;
            }
          });

        if (list.length > 0) {
          return list;
        }
      }

    } catch (e) {
      // ignore and retry
    }

    await new Promise(r =>
      setTimeout(r, intervalMs)
    );
  }

  // ── FINAL ATTEMPT ───────────────

  try {

    return fs.readdirSync(themesPath).filter(f => {

      const full =
        path.join(themesPath, f);

      try {

        const s = fs.statSync(full);

        return (
          s.isDirectory() ||
          f.toLowerCase().endsWith('.css')
        );

      } catch (err) {

        return false;
      }
    });

  } catch (e) {

    return [];
  }
}

// ── WAIT FOR AVAILABLE THEMES ───────────────

const candidates =
  await waitForThemeCandidates({
    timeoutMs: 15000,
    intervalMs: 400
  });

if (!candidates || candidates.length === 0) {

  new Notice(
    'Random-theme: no themes found after waiting.'
  );

  tR = "";
  return;
}

// ── PICK RANDOM THEME ───────────────

const pick =
  candidates[
    Math.floor(Math.random() * candidates.length)
  ].replace(/\.css$/i, "");

// ── LOAD APPEARANCE SETTINGS ───────────────

let appearance = {};

try {

  if (fs.existsSync(appearancePath)) {

    appearance = JSON.parse(
      fs.readFileSync(appearancePath, 'utf8') || '{}'
    );

  } else {

    appearance = {};
  }

} catch (e) {

  appearance = {};
}

// ── SWITCH THEME ───────────────

appearance.cssTheme = pick;

// ── SAVE ───────────────

try {

  fs.writeFileSync(
    appearancePath,
    JSON.stringify(appearance, null, 4),
    'utf8'
  );

} catch (e) {

  new Notice(
    'Random-theme: failed to write appearance.json: ' +
    e.message
  );

  tR = "";
  return;
}

// ── DONE ───────────────

new Notice('theme::' + pick);

tR = "";
%>
```

## What It Does

The script scans:

```text
.obsidian/themes/
```

collects installed themes, picks one randomly, then updates:

```text
appearance.json
```

Only this key changes:

```javascripton
"cssTheme"
```

Everything else stays untouched.

That means settings like:

```javascripton
"theme": "system"
```

survive safely.

---

## Notes

* Requires:

  * [Templater Plugin](https://silentvoid13.github.io/Templater/?utm_source=chatgpt.com)
* Desktop Obsidian only
* Works best with multiple installed themes
* Safe for startup automation
* Preserves unrelated appearance settings
* No themes are deleted or modified

---

Tiny script.
Makes Obsidian feel weirdly alive ✨

Based on extracted guide structure and style patterns from your uploaded reference 
