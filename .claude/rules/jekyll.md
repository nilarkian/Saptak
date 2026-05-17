---
paths:
  - "_layouts/**/*.html"
  - "_includes/**/*.html"
  - "_config.yml"
---
# Jekyll Rules — Saptak

## Layout Inheritance Chain
- `page.html` → extends `default.html`
- `note-layout.html` → extends `blank.html`
- `deep-dive.html`, `watchlist-layout.html`, `templater.html` → STANDALONE (full <html><head><body>)

Never extend `note-layout` or `deep-dive` from `default` — they own their full document structure.

## Font Loading (per layout — do not cross-contaminate)
| Layout | Fonts | Code libraries |
|--------|-------|----------------|
| `default.html` | Syne, DM Sans (Google) + Font Awesome 6.5.1 | none |
| `deep-dive.html` | Syne, DM Sans (Google) | none |
| `note-layout.html` | EB Garamond (Google) | Prism.js (syntax highlight) |
| `templater.html` | (inherit from blank) | Prism.js |
| `blank.html`, `page.html`, `watchlist-layout.html` | none | none |

## toc.html Parameters
Accepts: `body_selector` (querySelector string), `back_url`, `back_label`.
Host layout MUST have:
- `.main` class with `margin-left: 200px`
- `body.toc-collapsed .main { margin-left: 44px }` responsive rule

## tags.html Context Detection
Auto-detects page type by DOM element presence:
- `#timeline-body` → watchlist mode
- `#note-list` → notes mode
- `#inspo-body` → inspo mode
- `#catalogue` → templater mode
Host pages must implement matching filter hook (`window.applyTopicFilter`, `window.applyInspoFilter`, etc.)

## localStorage Behavior
- `index.html` (home) → does NOT persist theme. Every load defaults to dark.
- `note-layout.html` → persists via `localStorage['note-theme']`

## Inspo Category Registration
New inspo category needs two things:
1. Entry in `_data/inspo_categories.yml` (fields: key, icon, label, unit, tint, card_include)
2. Matching include file at `_includes/inspo/[key].html`

## Reusable Include Pattern
Include owns: CSS, HTML, event listener wiring. Host page owns: logic functions.
Communication: include calls `window.fnName()`, host page defines `window.fnName = ...`.

## CSS in Shared Includes
Always use `var(--token, fallback)` in includes used across multiple pages.
Pages define different CSS custom properties — fallbacks prevent breakage.

## kramdown Features Available
Footnotes, definition lists, task lists. Use them — they render correctly on GitHub Pages.
