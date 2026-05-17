# Handoff: Smart Back-Navigation for Pinned Resources

**Generated**: 2026-05-17
**Branch**: main
**Status**: Not Started

## Goal

When a user opens a pinned resource (or any note) from different source pages, the back/breadcrumb navigation should return them to where they came from — not always to `notes.html`. If entered from inspo, go back to inspo. If entered from notes, go back to notes.

## Completed (Prior Sessions)

- [x] Pinned Resources content type (`is_pinned: true` frontmatter convention)
- [x] Inspo tab: `pinned-resources` category in `_data/inspo_categories.yml`
- [x] Card template: `_includes/inspo/pinned-resources.html`
- [x] CSS for `.pinned-card` in `inspo.html` (lines 529-580)
- [x] Liquid count + render logic in `inspo.html` (3 `elsif` branches for `pinned-resources`)
- [x] Index nav: Resume link replaced with "Resources" → `inspo.html?cat=pinned-resources`
- [x] Index nav: Deep Dives link fixed from hardcoded `/Saptak/` to `relative_url`
- [x] Notes page: 📌 emoji prefix for pinned notes in note row
- [x] Notes page: "Resources" topic auto-appears in filter bar
- [x] Existing file `notes/intereting claude skills & other github repos.md` normalized (Obsidian anti-patterns removed, `title`, `topic: "Resources"`, `blurb` added)
- [x] Reset chip extracted into `_includes/reset-chip.html` (reusable)
- [x] Series pills + filter on `notes.html`
- [x] Build passes clean

## Not Yet Done

- [ ] Make back-navigation source-aware in `note-layout.html`
- [ ] Two navigation elements need updating:
  1. **TOC sidebar back link** (line 551-552) — currently hardcoded to `notes.html`
  2. **Breadcrumb** (lines 580-584) — currently hardcoded `Notes > Topic`
- [ ] When entering from inspo → back should go to `inspo.html` (or `inspo.html?cat=pinned-resources`)
- [ ] When entering from notes → back should go to `notes.html` (current behavior, keep as default)
- [ ] Build check + browser test

## Failed Approaches (Don't Repeat These)

From prior sessions (not this task, but relevant context):
- **`opacity` on parent with interactive children**: Made child hover states invisible. Use `color` to dim instead.
- **URL param wrapper for series filter**: Closure approach failed. Integrated `activeSeries` directly into `applyTopicFilter()`.

For the back-navigation task specifically: None yet — fresh task.

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Pinned resources use `note-layout.html` | User requirement — note-like content |
| `is_pinned: true` flag (not separate directory) | Minimal, no new collection needed |
| Back-nav should be source-aware | User explicitly requested: "if we enter from notes we go back to notes, if we enter from inspo we go back to inspo" |

## Current State

**Working**: Full pinned resources feature functional. Inspo tab shows, card renders, notes page lists with 📌, index nav link works, `?cat=pinned-resources` URL param auto-selects tab. Site builds clean.

**Problem**: `note-layout.html` always navigates back to `notes.html` regardless of entry source. Two hardcoded locations.

**Uncommitted Changes**: 6 files (4 modified + 2 new):
- `M _data/inspo_categories.yml` — added pinned-resources entry
- `M index.html` — replaced Resume with Resources link, fixed Deep Dives baseurl
- `M inspo.html` — CSS for pinned cards + 3 Liquid elsif branches
- `M notes.html` — 📌 emoji prefix in note row title
- `?? _includes/inspo/pinned-resources.html` — new card template
- `?? notes/intereting claude skills & other github repos.md` — existing file, frontmatter normalized

## Files to Know

| File | Lines | What |
|------|-------|------|
| `_layouts/note-layout.html` | 551-552 | TOC include with hardcoded `back_url` to notes.html |
| `_layouts/note-layout.html` | 580-584 | Breadcrumb: `Notes > Topic` — hardcoded to notes.html |
| `_includes/toc.html` | 119 | Back link render: `<a class="back" href="{{ include.back_url }}">{{ include.back_label }}</a>` |
| `inspo.html` | 5752-5760 (built) | Pinned card links to note pages — source of inspo traffic |
| `notes.html` | 160-174 | Note row links to note pages — source of notes traffic |
| `index.html` | 241 | Resources nav link → `inspo.html?cat=pinned-resources` |
| `.claude/rules/core.md` | all | baseurl rules, CSS architecture, dark mode convention |
| `.claude/rules/jekyll.md` | all | Layout inheritance, toc.html params, JS window binding |

## Code Context

### Current back-navigation in note-layout.html (hardcoded)

```liquid
{% comment %} LINE 551-552: TOC sidebar back link {% endcomment %}
{% assign notes_back = site.baseurl | append: "/notes.html" %}
{% include toc.html body_selector=".note-body" back_url=notes_back back_label="← Notes" %}

{% comment %} LINES 580-584: Breadcrumb {% endcomment %}
<div class="breadcrumb">
  <a href="{{ site.baseurl }}/notes.html">Notes</a>
  <span>›</span>
  {{ page.topic }}
</div>
```

### toc.html back link (line 119)

```html
<a class="back" href="{{ include.back_url | default: site.baseurl }}">{{ include.back_label | default: "← Home" }}</a>
```

The `back_url` and `back_label` are passed as include parameters from the host layout.

### How pinned resource cards link (from inspo)

```html
<a class="inspo-card pinned-card"
   href="/Saptak/notes/intereting%20claude%20skills%20&%20other%20github%20repos/"
   data-category="pinned-resources" ...>
```

### How note rows link (from notes)

```html
<a class="note-row"
   href="/Saptak/notes/intereting%20claude%20skills%20&%20other%20github%20repos/" ...>
```

Both link to the same URL — the difference is only the referrer page.

### Approach Options

**Option A: URL parameter (`?from=inspo`)**
- Inspo card links append `?from=inspo` to href
- `note-layout.html` reads the param via JS or Liquid (JS since it's client-side)
- JS on page load: check `?from=inspo`, update breadcrumb href and TOC back link
- Pro: Explicit, reliable, bookmarkable
- Con: Pollutes URL, needs JS to override server-rendered Liquid

**Option B: `document.referrer` (JS-only)**
- JS checks `document.referrer` on page load
- If referrer contains `inspo.html`, update back links to inspo
- Pro: No URL pollution, no link changes needed
- Con: Referrer can be empty (direct nav, bookmarks), less reliable

**Option C: `sessionStorage` breadcrumb trail**
- Source pages write their identity to sessionStorage on link click
- Note layout reads sessionStorage to determine back target
- Pro: Survives page navigation, no URL changes
- Con: More complex, state management

**Recommended: Option A** — most reliable, simplest to implement. The `?from=` param is standard UX pattern.

## Resume Instructions

1. **Decide approach** — Option A (URL param) recommended. If using Option A:

2. **Modify card links to pass source** — In `_includes/inspo/pinned-resources.html`, append `?from=inspo` to href:
   ```liquid
   href="{{ r.url | prepend: site.baseurl }}?from=inspo"
   ```
   Consider: should ALL inspo cards (deep-dives too) do this? Or only pinned resources?

3. **Update `note-layout.html`** — Add JS at bottom to read `?from` param and update:
   - TOC back link (`a.back` in sidebar)
   - Breadcrumb link (`.breadcrumb a`)
   - Keep `notes.html` as default fallback when no param

4. **Test these flows**:
   - From `inspo.html` → click pinned card → back should go to inspo
     - Expected: breadcrumb says "Inspo > Resources", back link goes to inspo.html
   - From `notes.html` → click note row → back should go to notes
     - Expected: breadcrumb says "Notes > Topic", back link goes to notes.html (unchanged)
   - Direct URL access (no `?from`) → default to notes.html
     - Expected: current behavior preserved
   - From `inspo.html?cat=pinned-resources` → click card → back should return to pinned tab
     - Expected: back link goes to `inspo.html?cat=pinned-resources` (preserves tab state)

5. **Build**: `bundle exec jekyll build 2>&1` — must be clean

6. **Browser test** at `localhost:4000/Saptak/`

## Warnings

- **baseurl is critical**: All links must use `{{ site.baseurl }}` or `| relative_url`. Bare `/path` breaks GitHub Pages.
- **notes/ is NOT a Jekyll collection**: Files need `is_note: true` frontmatter.
- **CSS is inline per layout**: No shared stylesheet. `note-layout.html` has its own `<style>` block.
- **JS window binding**: Use `window.fn = fn;` explicitly. Never rely on sloppy-mode auto-binding.
- **Don't rename DOM IDs**: `#note-list`, `#inspo-body` used by `tags.html` for page detection.
- **toc.html ownership**: `toc.html` fully owns sidebar styling. Don't duplicate `.sidebar` CSS in layouts.
- **The `?from=inspo` approach may need to also encode the active category** so back goes to `inspo.html?cat=pinned-resources` not just `inspo.html`. Consider `?from=inspo&cat=pinned-resources` or `?from=inspo%3Fcat%3Dpinned-resources`.
- **Deep-dive notes also open via inspo** — consider whether deep-dives should also get source-aware back-nav (would require changes to `_includes/inspo/deep-dives.html` and potentially `_layouts/deep-dive.html`).
