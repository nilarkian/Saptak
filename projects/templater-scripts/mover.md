---
layout: templater
title: Project Mover
description: Watches every file for a project frontmatter field and moves it into the matching project folder automatically. Registers three palette commands on run.
category: automation
tags: [projects, files, watcher, commands, automation]
date: 2026-05-09
---

Run once on startup. Registers a persistent file watcher and three palette commands — any file saved with `project:` in its frontmatter moves into the matching project folder without further input.

```javascript
<%*
const { vault, workspace, commands, metadataCache } = app;

// ─────────────────────────────────────
// CONFIG
// ─────────────────────────────────────
const PROJECTS_PATH = "projects.md";
const WATCHER_DEBOUNCE_MS = 700;
const DEBOUNCE_MS = 300;
const NOTICE_COOLDOWN_MS = 1500;
const RENAME_SETTLE_MS = DEBOUNCE_MS * 2;
const FORCE_SYNC_BATCH = 10;

// ─────────────────────────────────────
// MODULE STATE
// ─────────────────────────────────────
const EPOCH = Date.now();
let projectRegistry = new Map();
let reloadTimer = null;
let lastNoticeAt = 0;
const fileDebounce = new Map();

// ─────────────────────────────────────
// HELPERS
// ─────────────────────────────────────
const stripWikiLinks = (val) => String(val).replace(/[\[\]]/g, "").trim();
const normalizeKey = (val) => stripWikiLinks(val).toLowerCase();

function normalizeProjectKeys(project) {
  if (!project) return [];
  let keys = Array.isArray(project) ? project : [project];
  return [...new Set(keys.map(k => normalizeKey(k)).filter(Boolean))].sort();
}

function createFolderSuffix(projectName) {
  return stripWikiLinks(projectName).replace(/[\\/:*?"<>|]/g, "").trim();
}

function throttleNotice(msg, duration = 4000) {
  const now = Date.now();
  if (now - lastNoticeAt > NOTICE_COOLDOWN_MS) {
    new Notice(msg, duration);
    lastNoticeAt = now;
  }
}

// ─────────────────────────────────────
// REGISTRY
// ─────────────────────────────────────
async function loadProjectRegistry() {
  try {
    const file = vault.getAbstractFileByPath(PROJECTS_PATH);
    if (!file) {
      projectRegistry.clear();
      throttleNotice("⚠️ projects.md not found (registry cleared).");
      return;
    }
    const content = await vault.read(file);
    const lines = content.split(/\r?\n/);
    const registry = new Map();
    for (let line of lines) {
      line = line.trim();
      if (!line || line.startsWith("#")) continue;
      const match = line.match(/^([^\s]+)\s+(.+)$/);
      if (!match) continue;
      registry.set(normalizeKey(match[2].trim()), {
        id: match[1].trim().toUpperCase(),
        originalName: match[2].trim()
      });
    }
    projectRegistry = registry;
  } catch (err) {
    console.error("Registry load failed", err);
  }
}

function scheduleRegistryReload() {
  if (reloadTimer) clearTimeout(reloadTimer);
  reloadTimer = setTimeout(async () => {
    try { await loadProjectRegistry(); }
    finally { reloadTimer = null; }
  }, DEBOUNCE_MS);
}

function getProjectFolderName(projectKey) {
  const entry = projectRegistry.get(normalizeKey(projectKey));
  if (!entry) return null;
  return entry.id + "-" + createFolderSuffix(projectKey);
}

// ─────────────────────────────────────
// CORE MOVER
// ─────────────────────────────────────
const runProjectMove = async (targetFile, isInteractive = false, _folderMap = null) => {
  if (!vault.getAbstractFileByPath(targetFile.path)) return { moved: false };

  const fm = metadataCache.getFileCache(targetFile)?.frontmatter;
  if (!fm || !fm.project) return { moved: false };

  const keys = normalizeProjectKeys(fm.project);
  if (keys.length === 0) return { moved: false };

  const allFolders = [vault.getRoot(), ...vault.getAllFolders()];
  const folderMap = _folderMap || new Map(allFolders.map(f => [f.name.toLowerCase(), f]));

  const unknownKeys = keys.filter(k => !getProjectFolderName(k));

  let matchedFolders = keys
    .map(k => folderMap.get(getProjectFolderName(k)?.toLowerCase()))
    .filter(Boolean);
  matchedFolders = [...new Set(matchedFolders)];

  let targetFolder = null;

  if (matchedFolders.length === keys.length) {
    matchedFolders.sort((a, b) => b.path.length - a.path.length);
    targetFolder = matchedFolders[0];
  } else if (isInteractive) {
    if (matchedFolders.length === 1 && keys.length >= 2) {
      const parent = matchedFolders[0];
      const missingKey = keys.find(k => !matchedFolders.some(f => f.name.toLowerCase() === getProjectFolderName(k)?.toLowerCase()));
      if (missingKey) {
        const name = getProjectFolderName(missingKey);
        const choice = await tp.system.suggester(["Yes", "No"], [true, false], false, `Create ${name} inside ${parent.name}?`);
        if (choice) {
          const path = parent.isRoot() ? name : `${parent.path}/${name}`;
          await vault.createFolder(path);
          targetFolder = vault.getFolderByPath(path);
        }
      }
    } else if (matchedFolders.length === 0 && keys.length === 1) {
      const name = getProjectFolderName(keys[0]);
      if (name && (await tp.system.suggester(["Yes", "No"], [true, false], false, `Create folder ${name}?`))) {
        const parent = await tp.system.suggester(allFolders.map(f => f.path || "/"), allFolders, false, "Parent Folder?");
        if (parent) {
          const path = parent.isRoot() ? name : `${parent.path}/${name}`;
          await vault.createFolder(path);
          targetFolder = vault.getFolderByPath(path);
        }
      }
    }
  }

  if (!targetFolder || targetFile.parent.path === targetFolder.path) return { moved: false, unknownKeys };

  const newPath = targetFolder.isRoot() ? targetFile.basename : `${targetFolder.path}/${targetFile.basename}`;
  if (!vault.getAbstractFileByPath(newPath)) {
    try {
      await tp.file.move(newPath, targetFile);
      new Notice(`📁 ${targetFile.basename} → ${targetFolder.path}`);
      return { moved: true };
    } catch (e) {
      console.error("Move failed", e);
      return { moved: false, unknownKeys };
    }
  }
  return { moved: false, unknownKeys };
};

// ─────────────────────────────────────
// RENAME SYNC
// ─────────────────────────────────────
async function handleRenameSync(file, oldPath) {
  if (!file.path.endsWith(".md")) return;

  const oldName = oldPath.split("/").pop().replace(".md", "");
  const newName = file.basename;
  const entry = projectRegistry.get(normalizeKey(oldName));
  if (!entry) return;

  const regFile = vault.getAbstractFileByPath(PROJECTS_PATH);
  if (regFile) {
    const raw = await vault.read(regFile);
    const eol = raw.includes("\r\n") ? "\r\n" : "\n";
    const escapedOld = oldName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const lineRegex = new RegExp(`^(${entry.id}\\s+)(?:\\[\\[${escapedOld}\\]\\]|${escapedOld})\\s*$`, "i");
    const lines = raw.split(/\r?\n/).map(line =>
      lineRegex.test(line) ? `${entry.id} [[${newName}]]` : line
    );
    await vault.modify(regFile, lines.join(eol));
  }

  const oldFolderName = entry.id + "-" + createFolderSuffix(oldName);
  const newFolderName = entry.id + "-" + createFolderSuffix(newName);
  const targetFolder = vault.getAllFolders().find(f => f.name.toLowerCase() === oldFolderName.toLowerCase());
  if (targetFolder) {
    const newFolderPath = targetFolder.path.replace(targetFolder.name, newFolderName);
    if (vault.getFolderByPath(newFolderPath)) {
      new Notice(`⚠️ Folder already exists: ${newFolderName}`);
    } else {
      await vault.rename(targetFolder, newFolderPath);
      new Notice(`Renamed folder: ${newFolderName}`);
    }
  }

  await loadProjectRegistry();
  setTimeout(() => runProjectMove(file, false), RENAME_SETTLE_MS);
}

// ─────────────────────────────────────
// SETUP
// ─────────────────────────────────────
async function setup() {
  if (window.__projectWatcher_installed === EPOCH) return;

  if (window.__projectWatcher_installed) {
    if (window.__pw_metaHandler)     metadataCache.off("changed", window.__pw_metaHandler);
    if (window.__pw_renameHandler)   vault.off("rename", window.__pw_renameHandler);
    if (window.__pw_projectsHandler) vault.off("modify", window.__pw_projectsHandler);
  }

  window.__projectWatcher_installed = EPOCH;

  await loadProjectRegistry();

  const metaHandler = async (file) => {
    if (!file?.path?.endsWith(".md")) return;
    if (fileDebounce.has(file.path)) clearTimeout(fileDebounce.get(file.path));
    const timer = setTimeout(async () => {
      fileDebounce.delete(file.path);
      const active = workspace.getActiveFile();
      const result = await runProjectMove(file, active && active.path === file.path);
      if (result?.unknownKeys?.length) {
        throttleNotice(`⚠️ Unknown project: "${result.unknownKeys[0]}" in ${file.basename}`);
      }
    }, WATCHER_DEBOUNCE_MS);
    fileDebounce.set(file.path, timer);
  };

  const renameHandler = async (file, oldPath) => { await handleRenameSync(file, oldPath); };

  const projectsHandler = (file) => {
    if (file.path === PROJECTS_PATH) scheduleRegistryReload();
  };

  window.__pw_metaHandler     = metaHandler;
  window.__pw_renameHandler   = renameHandler;
  window.__pw_projectsHandler = projectsHandler;

  metadataCache.on("changed", metaHandler);
  vault.on("rename", renameHandler);
  vault.on("modify", projectsHandler);

  new Notice("🛰️ Project Watcher Active");
}

// ─────────────────────────────────────
// COMMANDS
// ─────────────────────────────────────
commands.addCommand({
  id: "templater-project-watcher",
  name: "🚚 Project Mover: Force Sync All Files",
  callback: async () => {
    await loadProjectRegistry();

    const files = vault.getMarkdownFiles();
    const activeFile = workspace.getActiveFile();
    let moved = 0;
    const unknownProjects = new Set();

    if (activeFile) {
      const r = await runProjectMove(activeFile, true);
      if (r?.moved) moved++;
      r?.unknownKeys?.forEach(k => unknownProjects.add(k));
    }

    const folderMap = new Map(
      [vault.getRoot(), ...vault.getAllFolders()].map(f => [f.name.toLowerCase(), f])
    );

    const remaining = files.filter(f => f.path !== activeFile?.path);
    for (let i = 0; i < remaining.length; i += FORCE_SYNC_BATCH) {
      const results = await Promise.all(
        remaining.slice(i, i + FORCE_SYNC_BATCH).map(f => runProjectMove(f, false, folderMap))
      );
      for (const r of results) {
        if (r?.moved) moved++;
        r?.unknownKeys?.forEach(k => unknownProjects.add(k));
      }
    }

    let msg = `Sync complete — moved ${moved} file${moved !== 1 ? "s" : ""}`;
    if (unknownProjects.size) msg += `\n⚠️ Unknown: ${[...unknownProjects].join(", ")}`;
    new Notice(msg, 5000);
  }
});

commands.addCommand({
  id: "templater-project-watcher-show-projects",
  name: "🗂 Project Mover: Show Loaded Projects",
  callback: () => {
    if (projectRegistry.size === 0) {
      new Notice("Registry empty — run watcher or force-sync first");
      return;
    }
    const lines = [...projectRegistry.entries()]
      .map(([key, { id }]) => `${id}: ${key}`)
      .join("\n");
    new Notice(`Loaded projects (${projectRegistry.size}):\n${lines}`, 8000);
  }
});

commands.addCommand({
  id: "templater-project-watcher-reset",
  name: "🔄 Project Mover: Reset Watcher",
  callback: async () => {
    if (window.__pw_metaHandler)     metadataCache.off("changed", window.__pw_metaHandler);
    if (window.__pw_renameHandler)   vault.off("rename", window.__pw_renameHandler);
    if (window.__pw_projectsHandler) vault.off("modify", window.__pw_projectsHandler);
    window.__projectWatcher_installed = null;
    window.__pw_metaHandler     = null;
    window.__pw_renameHandler   = null;
    window.__pw_projectsHandler = null;
    projectRegistry.clear();
    fileDebounce.clear();
    if (reloadTimer) { clearTimeout(reloadTimer); reloadTimer = null; }
    await setup();
  }
});

// ─────────────────────────────────────
// INIT
// ─────────────────────────────────────
await setup();
%>
```

## The Commands

**🚚 Force Sync All Files** — scans every markdown file in the vault and moves each one to its project folder. Runs the active file first (interactive mode), then processes the rest in parallel batches. Reports total moved count and any unknown project keys.

**🗂 Show Loaded Projects** — prints the current registry contents as `ID: key` pairs. Use this to verify the registry loaded correctly after editing `projects.md`.

**🔄 Reset Watcher** — tears down all registered event handlers and reinitializes from scratch. Use this after plugin crashes or when the watcher stops responding — no Obsidian restart required.

## How It Works

Registry loads from `projects.md` (one entry per line: `ID ProjectName`). Folder name is built as `ID-ProjectName` with special characters stripped. The watcher fires on every metadata change, debounced 700 ms — the active file runs in interactive mode (prompts to create missing folders), background files run silently.

Rename sync triggers when any project note is renamed: `projects.md` gets the new name, and the corresponding folder is renamed to match. A fresh move runs after a short settle delay to catch any in-flight debounce.

## Customisation

- swap `PROJECTS_PATH` for a different registry file location
- raise `WATCHER_DEBOUNCE_MS` to reduce move noise while typing frontmatter
- lower `FORCE_SYNC_BATCH` on slow hardware or large vaults
- remove the `isInteractive` branches in `runProjectMove` to make all moves fully silent

## Edge Cases

- unknown `project:` value → throttled warning notice, file stays in place
- file already in correct folder → no move, no notice
- file deleted during debounce window → skipped silently (guard checks path before moving)
- `project:` array with multiple keys → file moves to the deepest folder that matches all keys
- folder collision on rename → warning notice, old folder preserved

## Notes

- Handlers are session-scoped — re-run on next startup or chain into a startup template
- Hot-reload safe: epoch guard detects prior run and tears down stale handlers before re-registering
- Requires Templater plugin
