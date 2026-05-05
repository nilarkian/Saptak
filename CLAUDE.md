# CLAUDE.md

## Context Navigation
When you need to understand the codebase, docs, or any files in this project:
1. ALWAYS query the knowledge graph first: `/graphify query "your question"`
2. Only read raw files if I explicitly say "read the file" or "look at the raw file"
3. Use `graphify-out/wiki/index.md` as your navigation entrypoint for browsing structure

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal portfolio/website for Saptak Banerjee, built with Jekyll and deployed to GitHub Pages at `https://nilarkian.github.io/Saptak`. The `_site/` directory is the compiled output — don't edit files there directly.

## Commands

```bash
bundle install                  # install dependencies (first time)
bundle exec jekyll serve        # local dev server at http://localhost:4000/Saptak
bundle exec jekyll build        # build to _site/
bundle exec jekyll serve --livereload  # auto-refresh on changes
```

## Architecture

### Key config (`_config.yml`)
- `baseurl: "/Saptak"` — all internal links must use `{{ site.baseurl }}` or `relative_url`
- `permalink: pretty` — URLs like `/notes/oi/` not `/notes/oi.html`
- `_writing` is a Jekyll collection (deep-dive essays), output enabled
- `notes/` pages are regular pages included via `include: [notes]`; they become notes by setting `is_note: true` in front matter

### Pages and layouts

| File | Layout | Purpose |
|------|--------|---------|
| `index.html` | `layout: null` (standalone) | Home — animated starfield, dark/light toggle |
| `notes.html` | standalone | Notes index with topic filter + tag sidebar |
| `inspo.html` | standalone | Swipefile: YouTube, music, tweets, tools, writing, deep-dives |
| `projects.html` | standalone | Projects listing (static HTML) |
| `about.html` | `default` | About page |
| `watchlist.html` | `watchlist-layout` | Tech news tracker |
| `notes/*.md` | `note-layout` | Individual notes with left TOC sidebar |
| `_writing/*.md` | `deep-dive` | Long-form essays appearing in the Inspo "Deep Dives" tab |

**Layout chain**: `note-layout` extends `blank`; `blank` is a minimal wrapper.

### Includes

- `bg-stars.html` / `bg-rainbow.html` — CSS-only animated backgrounds. Both are loaded on `index.html`; dark mode shows stars (default), `body.light-mode` switches to rainbow. Drop both into any page `<body>` that needs the animated background.
- `theme-toggle.html` — Toggles `body.light-mode`. **No localStorage** — every page load defaults to dark mode.
- `tags.html` — Universal right-side tag sidebar. Auto-detects context by checking for `#timeline-body` (watchlist), `#note-list` (notes), `#inspo-body` (inspo), or `#catalogue` (templater scripts). Exposes `window.applyTopicFilter`, `window.applyInspoFilter`, or `window.applyScriptFilter` hooks that the host page must define.
- `connect.html` — Social/contact section included at the bottom of the home page.
- `inspo/yt.html`, `inspo/mu.html`, `inspo/tweet.html`, `inspo/tools.html`, `inspo/writing.html`, `inspo/website.html`, `inspo/deep-dives.html` — Card renderers for each inspo category.

### Data files

- `_data/tags.yml` — Tag hierarchy tree (parent → children). Consumed by `tags.html` to build the sidebar.
- `_data/inspo_categories.yml` — Registry of inspo categories: `key`, `icon`, `label`, `unit`, `tint`, `card_include`. Adding a new category here automatically adds it to the tab grid and masonry.
- `_data/inspo/*.json` — Content for each inspo category (tools, tweets, websites, music, writing, youtube).

### Adding content

**New note**: Create `notes/slug.md` with:
```yaml
---
layout: note-layout
title: "Title"
topic: "Topic Name"
date: YYYY-MM-DD
tags: [tag1, tag2]
is_note: true
---
```

**New deep-dive**: Create `_writing/slug.md` with `layout: deep-dive` — it will appear in the Inspo "Deep Dives" tab automatically.

**New inspo item**: Add an entry to the relevant `_data/inspo/*.json` file. Each card type has its own schema — check existing entries for the expected fields.

**New tag**: Add to `_data/tags.yml`. Tags not in the tree appear under "Other" in the sidebar.

### Design system

CSS is inline in each page/layout — there is no shared stylesheet. Design tokens via CSS variables:

```css
--bg, --ink, --ink-soft, --muted, --border
--hover-shadow, --hover-border
--pill: 999px        /* border-radius for pill shapes */
--font-head: 'Syne'
--font-body: 'DM Sans'
```

Dark mode is the default state (no class on body). Light mode adds `body.light-mode`. Most pages are light-only (notes, projects, inspo) — the dark/light toggle + starfield only appear on the home page.

Deep-dive cards use a separate serif aesthetic: `EB Garamond` + `--paper`/`--ink-warm`/`--ink-burgundy` tokens defined locally in `inspo.html`.

Max content widths: 950px (home, inspo) · 900px (notes, projects) · 860px (note body).

## graphify

A knowledge graph of this codebase lives in `graphify-out/graph.json` (if it has been built).

**Before answering architecture or codebase questions**, check the graph:
```
/graphify query "<your question>"
```

**After making code changes**, rebuild the graph to keep it current:
```
/graphify . --update
```

Use `/graphify path "ConceptA" "ConceptB"` to trace how two parts of the site connect, and `/graphify explain "NodeName"` for a plain-language breakdown of any node.
