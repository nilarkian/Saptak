---

layout: templater
title: Random Community Theme Installer
description: Download and instantly apply a random Obsidian community theme directly from the official theme index.
category: automation
tags: [templater, themes, appearance, obsidian, automation]
date: 2026-05-07
---

# One-command random theme switching

Run this Templater script once.

It:

* downloads a random community theme
* installs it into `.obsidian/themes/`
* updates `appearance.json`
* immediately switches your vault to the new theme

Useful for:

* theme discovery
* visual refreshes
* inspiration sessions
* “slot machine” UI exploration

```javascript
<%*
/*
Templater script: Download a random community theme from Obsidian's official list
- Fetches the community themes index from obsidian-releases
- Picks one at random
- Attempts to download theme.css (tries "main" then "master")
- Writes files into .obsidian/themes/<themeName>/
- Sets appearance.cssTheme to the installed folder name and refreshes UI

Notes / assumptions:
- Desktop Obsidian with network access.
- Most authors put theme.css at repo root; script tries that first.
- If manifest.json exists in the repo it will be fetched; otherwise a minimal manifest is created.
*/

const fs = require("fs");
const path = require("path");

const base = tp.app.vault.adapter.basePath;
const appearancePath = path.join(base, ".obsidian", "appearance.json");
const themesDir = path.join(base, ".obsidian", "themes");

const indexUrl =
  "https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-css-themes.json";

async function fetchJson(url) {
  const r = await fetch(url);

  if (!r.ok) {
    throw new Error(`Fetch failed ${url} -> ${r.status}`);
  }

  return await r.json();
}

async function fetchText(url) {
  const r = await fetch(url);

  if (!r.ok) return null;

  return await r.text();
}

try {

  // ── ENSURE THEMES FOLDER ───────────────

  if (!fs.existsSync(themesDir)) {
    fs.mkdirSync(themesDir, { recursive: true });
  }

  // ── FETCH COMMUNITY INDEX ───────────────

  const idxResp = await fetch(indexUrl);

  if (!idxResp.ok) {
    throw new Error("Could not download community themes index.");
  }

  const index = await idxResp.json();

  // ── PICK RANDOM THEME ───────────────

  const entry =
    index[Math.floor(Math.random() * index.length)];

  const repo = entry.repo;

  const displayName =
    entry.name || repo.split("/").pop();

  // ── SANITIZE FOLDER NAME ───────────────

  const folderName = displayName.replace(
    /[<>:"\/\\|?*\x00-\x1F]/g,
    "_"
  );

  const destFolder =
    path.join(themesDir, folderName);

  // ── FETCH THEME FILES ───────────────

  const branches = ["main", "master"];

  let themeCss = null;
  let manifestJson = null;

  for (const br of branches) {

    if (!themeCss) {

      const cssUrl =
        `https://raw.githubusercontent.com/${repo}/${br}/theme.css`;

      themeCss = await fetchText(cssUrl);
    }

    if (!manifestJson) {

      const manifestUrl =
        `https://raw.githubusercontent.com/${repo}/${br}/manifest.json`;

      const manifestText =
        await fetchText(manifestUrl);

      if (manifestText) {

        try {
          manifestJson = JSON.parse(manifestText);
        } catch (e) {
          manifestJson = null;
        }
      }
    }

    if (themeCss && manifestJson) break;
  }

  // ── FALLBACK CSS LOCATIONS ───────────────

  if (!themeCss) {

    const altNames = [
      "obsidian.css",
      `${folderName}.css`,
      "dist/theme.css",
      "dist/obsidian.css"
    ];

    outer:
    for (const br of branches) {

      for (const alt of altNames) {

        const altUrl =
          `https://raw.githubusercontent.com/${repo}/${br}/${alt}`;

        const txt = await fetchText(altUrl);

        if (txt) {
          themeCss = txt;
          break outer;
        }
      }
    }
  }

  if (!themeCss) {
    throw new Error(
      "Could not find theme.css in the selected repo."
    );
  }

  // ── WRITE THEME FILES ───────────────

  if (!fs.existsSync(destFolder)) {
    fs.mkdirSync(destFolder, { recursive: true });
  }

  fs.writeFileSync(
    path.join(destFolder, "theme.css"),
    themeCss,
    "utf8"
  );

  // ── WRITE MANIFEST ───────────────

  if (manifestJson) {

    fs.writeFileSync(
      path.join(destFolder, "manifest.json"),
      JSON.stringify(manifestJson, null, 2),
      "utf8"
    );

  } else {

    const minimal = {
      "name": folderName,
      "id": folderName
        .toLowerCase()
        .replace(/\s+/g, "-"),
      "author": entry.author || "",
      "version": "1.0.0",
      "description": `Imported from ${repo}`,
      "isTheme": true
    };

    fs.writeFileSync(
      path.join(destFolder, "manifest.json"),
      JSON.stringify(minimal, null, 2),
      "utf8"
    );
  }

  // ── UPDATE APPEARANCE ───────────────

  let appearance = {};

  try {

    appearance = JSON.parse(
      fs.readFileSync(appearancePath, "utf8") || "{}"
    );

  } catch (e) {

    appearance = {};
  }

  appearance.cssTheme = folderName;

  fs.writeFileSync(
    appearancePath,
    JSON.stringify(appearance, null, 4),
    "utf8"
  );

  // ── DONE ───────────────

  new Notice(
    `Downloaded & installed theme: ${folderName}`
  );

} catch (err) {

  new Notice(
    "Random theme install failed: " +
    (err.message || err)
  );
}

tR = "";
return "";

%>
```

## What Happens

The script pulls from Obsidian’s official community theme index:

```text
obsidian-releases/community-css-themes.json
```

Then:

```text
pick random theme
→ download CSS
→ install locally
→ switch vault theme
```

No manual browsing required.

---

## How It Works

### 1. Fetch official theme registry

Downloads the public community theme list from:

```text
obsidianmd/obsidian-releases
```

---

### 2. Pick random entry

Chooses one theme using:

```javascript
Math.random()
```

---

### 3. Download theme files

Attempts:

```text
/theme.css
```

from:

```text
main branch
→ master branch
```

Then falls back to common alternative paths.

---

### 4. Install locally

Writes files into:

```text
.obsidian/themes/<themeName>/
```

including:

* `theme.css`
* `manifest.json`

---

### 5. Activate theme

Updates:

```text
.obsidian/appearance.json
```

by changing:

```javascripton
"cssTheme"
```

to the downloaded theme folder.

---


## Notes

* Requires:

  * [Templater Plugin](https://silentvoid13.github.io/Templater/)
* Desktop Obsidian only
* Requires internet access
* Uses Obsidian’s official theme registry
* Existing themes are not deleted
* Safe to rerun repeatedly
* Folder names are sanitized for filesystem safety

---

Tiny automation. Surprisingly high dopamine value 🎲✨

Based on extracted guide structure and style patterns from your uploaded reference 
