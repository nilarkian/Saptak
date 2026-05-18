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

## Type Incompatibility in Liquid Filters
Jekyll 3.x Document objects (from collections like `site.writing`) and Page objects (from `site.pages`) are incompatible in concat operations.
Comparing or mixing them in `sort_by` or `concat` filters throws "comparison of Array with Array failed".

**Fix:** Sort each collection independently before concatenation:
```liquid
{% assign sorted_writing = site.writing | sort: "date" | reverse %}
{% assign sorted_pages = site.pages | sort: "date" | reverse %}
{% assign combined = sorted_writing | concat: sorted_pages %}
```
NOT: `site.writing | concat: site.pages | sort: "date"`

**When:** Any Liquid template mixing site.writing (Document) with site.pages (Page) or iterating over both.

## Discriminating Collections by Type
In mixed Document/Page loops, use the `number` field:
- `item.number` exists → Document (collection item, e.g., from `site.writing`)
- `item.number` absent → Page (regular file, from `site.pages`)

Use this instead of trying to detect type via `collection_name` or `layout` which don't reliably exist in Liquid context.

## Tab Visibility Control Point
In pages with filterable tabs (like inspo.html), `matchesCategory()` in the JS filter function is the single source of truth for which items appear in which tabs.

Never duplicate category logic in both the HTML generation loop and the JS filter.
Instead, extend `matchesCategory()` with OR rules — don't add duplicate DOM elements for cross-category items.

**When:** Adding a new category to inspo or implementing cross-category display.

## Count Loop Isolation
When a page has both an "all items" count and "tab-specific" counts (e.g., inspo.html pills):
- Update ONLY the tab pills count loop when adding cross-category logic
- The all-count loop counts raw data and should not be modified — modifying both causes double-counting

**When:** Implementing category-aware filtering that spans multiple count displays.
