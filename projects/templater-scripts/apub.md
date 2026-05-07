---
id: 2026MayW1907Thu0826pm31
title: Auto Push Watchlist
description: Saves an Obsidian watchlist note, stages the linked repo file, commits only if changes exist, then pushes automatically to GitHub.
category: Automation
tags:
  - git
  - github
  - automation
  - watchlist
  - templater
  - symlink
date: 2026-03-05
layout: templater
---

Edit the watchlist note inside Obsidian, run the template, and the rest happens automatically:

- saves the note
- stages the file
- commits only if changes exist
- pushes to GitHub

The actual repository file is a symlink pointing into your Obsidian vault, so editing the note edits the repo file directly. No manual git workflow needed afterward.

```javascript
// pushwatchlist.js

const { exec } = require("child_process");

async function pushwatchlist() {

    return new Promise((resolve, reject) => {

        const cmd =
            'cd /d C:\\Users\\indig\\OneDrive\\Desktop\\Saptak && ' +
            'git add projects/watchlist/watchlist.md && ' +
            'git diff --cached --quiet || ' +
            '(git commit -m "watchlist update" && git push origin main)';

        exec(cmd, (error, stdout, stderr) => {

            console.log(stdout);

            if (stderr) {
                console.error(stderr);
            }

            // git diff --cached --quiet returns exit code 1 when changes exist
            // so ignore that specific case
            if (
                error &&
                !stdout.includes("nothing to commit")
            ) {
                reject(stderr || error.message);
                return;
            }

            resolve(stdout || "done");
        });
    });
}

module.exports = pushwatchlist;
```

## The Templater Trigger

Run this from Obsidian. It saves the current file, waits one second so the filesystem settles, then calls the Node.js helper.

```javascript
<%*
try {

    await app.commands.executeCommandById("editor:save-file");

    await new Promise(r => setTimeout(r, 1000));

    await tp.user.pushwatchlist();

    new Notice("✅ Watchlist pushed");

} catch (err) {

    console.error(err);

    new Notice(`❌ ${err}`, 10000);
}
%>
```

## How The System Works

The workflow depends on a symlink.

```text
Obsidian Note
      ↓
Symlink
      ↓
Git Repository File
      ↓
Git Add → Commit → Push
```

Because the repo file is linked directly into the vault:

- editing the Obsidian note edits the repository file
- no export step exists
- no sync script exists
- git operates directly on the live markdown file

The Templater script becomes the entire deployment pipeline.

---

## The Git Flow

The command chain runs in this order:

```bash
git add projects/watchlist/watchlist.md
git diff --cached --quiet
git commit -m "watchlist update"
git push origin main
```

### What Each Step Does

`git add` — stages the watchlist file only.

`git diff --cached --quiet` — checks whether staged changes exist.

- exit code `0` → no changes
- exit code `1` → changes exist

That exit code is intentionally used as control flow.

`git commit` only runs if changes exist.

`git push origin main` only runs after a successful commit.

---

## Why The Error Handling Looks Weird

This block is intentional:

```javascript
if (
    error &&
    !stdout.includes("nothing to commit")
)
```

`git diff --cached --quiet` returns exit code `1` when differences exist.

Normally that looks like an error to Node's `exec()` callback — but here it's actually expected behavior.

Without this guard:

- valid commits would incorrectly reject
- the automation would fail every time changes existed

---

## Why The Delay Exists

```javascript
await new Promise(r => setTimeout(r, 1000));
```

Obsidian saves asynchronously.

Without the delay:

- git may run before the file finishes writing
- stale content may get committed
- rapid edits can race the filesystem

The one-second pause gives the write operation time to settle.

---

## Required Setup

## 1. Create The Symlink

Windows example:

```powershell
mklink "C:\repo\projects\watchlist\watchlist.md" "C:\vault\watchlist.md"
```

After that:

- both paths point to the same physical file
- editing either updates both

---

## 2. Add The JS File To Templater Scripts

Place the JS file inside your Templater scripts folder.

Example:

```text
Vault/
└── scripts/
    └── pushwatchlist.js
```

---

## 3. Enable User Scripts In Templater

Inside Templater settings:

```text
Templater → User Scripts Folder Location
```

Point it at the scripts directory.

---

## 4. Run The Template

Run from:

```text
Cmd/Ctrl + P
```

Then:

```text
Templater: Replace templates in active file
```

Or bind it to a hotkey.

---

## Observable Outcomes

### No Changes Made

Result:

- nothing commits
- nothing pushes
- no duplicate commit spam

---

### Changes Exist

Result:

- file stages
- commit created
- pushed to `origin/main`
- success notice appears

---

### Failure

Result:

- console logs full error
- Obsidian shows persistent failure notice for 10 seconds

---

## How To Customise

**Change the target file**

Replace:

```javascript
projects/watchlist/watchlist.md
```

with any tracked file path.

---

**Change the commit message**

Replace:

```javascript
"watchlist update"
```

with your own message.

---

**Push a different branch**

Replace:

```bash
git push origin main
```

with:

```bash
git push origin dev
```

or any branch name.

---

**Handle multiple files**

Replace:

```bash
git add projects/watchlist/watchlist.md
```

with:

```bash
git add .
```

if you want full-repo automation.

---

## Notes

- Requires Git installed and available in PATH
- Requires Templater plugin
- Requires Node.js execution support in Templater
- The repository path is hardcoded
- The workflow is Windows-specific because of `cd /d`
- The automation is synchronous from the user's perspective: trigger once, everything completes in sequence
- The symlink is the core architectural piece — without it, Obsidian and the repository become separate systems again
