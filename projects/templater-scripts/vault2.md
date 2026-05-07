---
layout: templater
title: Open Secondary Vault
description: Registers a command that jumps directly into a second Obsidian vault using an obsidian:// URI.
category: Navigation
tags: [vaults, navigation, commands]
date: 2025-05-07
---

Run once on startup. After that `📦 Open Archive Vault` appears in the command palette and instantly switches into the `.archive` vault.

```javascript
<%*
  const { commands } = app;

  if (!commands.commands["📦 Open Archive Vault"]) {
    commands.addCommand({
      id: "📦 Open Archive Vault",
      name: "📦 Open Archive Vault",
      callback: async () => {
        const vaultName = ".archive";
        const uri = `obsidian://open?vault=${encodeURIComponent(vaultName)}`;
        window.location.href = uri;
      }
    });
  }
return "";
%>
````

## How It Works

`obsidian://open?vault=` is Obsidian's URI scheme for vault switching.

```javascript
const uri = `obsidian://open?vault=${encodeURIComponent(vaultName)}`;
```

`encodeURIComponent()` safely escapes spaces and special characters in vault names.

```javascript
window.location.href = uri;
```

Triggers the vault switch immediately.

## How To Customise

**Change the vault**

Replace:

```javascript
const vaultName = ".archive";
```

with your vault name.

**Prevent duplicate commands**

```javascript
if (!commands.commands["📦 Open Archive Vault"])
```

acts as a guard so rerunning the template won't register the command twice.

## Notes

* Command is session-scoped
* Requires Templater
* Vault must already exist in Obsidian
* Works anywhere Obsidian URI schemes are supported

