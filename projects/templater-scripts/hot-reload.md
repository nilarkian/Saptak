
---
layout: templater
title: Plugin Hot Reload
description: Registers a command that disables and re-enables a plugin so you can hot reload plugins during development without restarting Obsidian.
category: Utility
tags: [plugins, development, reload, commands, hot-reload]
date: 2026-05-07
---

Run once on startup. After that `🔄 Reload Plugin` appears in the command palette and hot reloads a target plugin in-place.

Useful while developing plugins — edit code, rebuild, trigger reload, continue testing without restarting Obsidian.

```javascript
<%*
  const { commands } = app;

  if (!commands.commands["plugin-hot-reload"]) {

    commands.addCommand({

      id: "plugin-hot-reload",

      name: "🔄 Reload Plugin",

      callback: async () => {

        const p = "hill-charts";

        await app.plugins.disablePluginAndSave(p);

        await new Promise(resolve =>
          setTimeout(resolve, 1000)
        );

        await app.plugins.enablePluginAndSave(p);

        new Notice(`🔴 ${p} reloaded`);
      }
    });
  }

return "";
%>
```

## How It Works

```javascript
await app.plugins.disablePluginAndSave(p);
```

Fully unloads the plugin.

```javascript
await app.plugins.enablePluginAndSave(p);
```

Loads the rebuilt version back into memory.

The delay gives Obsidian time to fully tear down the plugin before reloading it again.

## How To Customise

**Change the target plugin**

Replace:

```javascript
const p = "hill-charts";
```

with your plugin ID.

Plugin IDs match the folder name inside:

```text
.obsidian/plugins/
```

**Change the delay**

Replace:

```javascript
1000
```

with a longer delay if the plugin has heavy teardown/setup logic.

## Notes

* Command is session-scoped
* Requires Templater
* Best used during active plugin development
* Avoid rapid repeated reloads on filesystem-heavy plugins
* Reloading preserves the current vault state but fully restarts the target plugin

