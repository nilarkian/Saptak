# Handoff: Pinned Resources — New Content Type + Inspo Tab + Index Link

**Generated**: 2026-05-17
**Branch**: main
**Status**: Not Started

## Goal

Create a "Pinned Resources" content type. Pinned resources are markdown files in `notes/` with `is_pinned: true` frontmatter, using `note-layout.html` as layout. They appear in three places:

1. **Inspo page** — as a new category tab (like Deep Dives, YouTube, etc.)
2. **Notes page** — listed alongside regular notes
3. **Index page** — replace the Resume nav link with a Pinned Resources link that navigates to `inspo.html?cat=pinned` (same pattern as Deep Dives quick link)

## Completed (Prior Sessions)

- [x] Reset chip extracted into `_includes/reset-chip.html` (reusable include)
- [x] Reset chip wired into both `inspo.html` and `notes.html`
- [x] Series pills + filter on `notes.html` (activeSeries, URL param, toggle)
- [x] Series pill on `note-layout.html`

## Not Yet Done

- [ ] Define `is_pinned: true` frontmatter convention for pinned resource files
- [ ] Create sample pinned resource file(s) in `notes/` with `layout: note-layout`, `is_pinned: true`
- [ ] Add `pinned` category to `_data/inspo_categories.yml`
- [ ] Create `_includes/inspo/pinned.html` card template for pinned resources in inspo grid
- [ ] Wire pinned resources into inspo.html tab system (category filter, counts)
- [ ] Show pinned resources in `notes.html` note list (they have `is_note: true` + `is_pinned: true`)
- [ ] In `index.html`: replace Resume link with Pinned Resources link → `inspo.html?cat=pinned`
- [ ] Decide: should pinned notes have a visual indicator (pin icon, badge) in notes.html rows?
- [ ] Build check + browser test both pages

## Failed Approaches (Don't Repeat These)

None yet — fresh task. But from prior sessions:

- **URL param wrapper for series filter**: Tried wrapping `applyTopicFilter` with a closure. Failed — replaced with integrated `activeSeries` variable inside `applyTopicFilter()`.
- **`opacity` on parent with interactive children**: `.note-row-meta` had `opacity: .35` which made child pill hover states invisible. Fixed with `color: #aaa`.

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Pinned resources use `note-layout.html` | User requirement — they're note-like content |
| `is_pinned: true` frontmatter flag | Distinguishes pinned from regular notes without a separate directory |
| Inspo tab pattern (not separate page) | Mirrors Deep Dives — already proven UX pattern |
| Replace Resume link, not add alongside | User explicitly wants replacement |

## Current State

**Working**: Site builds clean. Reset chip works on both inspo + notes. Series filter works. All existing inspo tabs functional.

**Uncommitted Changes**: 16 files modified + 1 new (`_includes/reset-chip.html`). Changes from prior sessions: reset chip extraction, series pills, note frontmatter updates.

## Files to Know

| File | Lines | What |
|------|-------|------|
| `_data/inspo_categories.yml` | all | Category registry — add `pinned` entry here |
| `_includes/inspo/deep-dives.html` | all | Template for deep-dive cards in inspo grid — copy this pattern for pinned |
| `inspo.html` | 557-600 | Category tab rendering + card include loop |
| `inspo.html` | 659-666 | URL param `?cat=` → auto-activates tab on load |
| `notes.html` | 141 | `{% assign all_notes = site.pages \| where_exp: "p", "p.is_note" %}` — pinned notes need `is_note: true` to appear here |
| `notes.html` | 160-174 | Note row rendering loop — may need pin indicator |
| `index.html` | 241 | Resume link to replace |
| `index.html` | 252 | Deep Dives quick link — pattern to follow for pinned |
| `_layouts/note-layout.html` | all | Layout pinned resources will use |

## Code Context

### Inspo category registration pattern (`_data/inspo_categories.yml`)

```yaml
- key: deep-dives
  icon: ""
  label: "Deep Dives"
  unit: "dives"
  tint: "#f0f0f0"
  card_include: "inspo/deep-dives"
```

### Deep Dives card include (`_includes/inspo/deep-dives.html`) — model for pinned

```html
{% for d in items %}
<a class="inspo-card deepdive-card"
   href="{{ d.url | prepend: site.baseurl }}"
   data-category="deep-dives"
   data-date="{{ d.date | date: '%Y-%m-%d' }}"
   data-tags="{% for t in d.tags %}{{ t | downcase }}{% unless forloop.last %},{% endunless %}{% endfor %}">
  <div class="deepdive-title">{{ d.title }}</div>
  {% if d.blurb %}<div class="deepdive-blurb">{{ d.blurb }}</div>{% endif %}
</a>
{% endfor %}
```

### Inspo tab count logic — Deep Dives uses `site.writing` collection

```liquid
{% if cat.key == 'deep-dives' %}
  {% assign cat_count = site.writing | size %}
{% else %}
  {% assign cat_count = site.data.inspo[cat.key] | size %}
{% endif %}
```

Pinned resources are pages (not a collection, not data files), so count logic needs a new branch:

```liquid
{% if cat.key == 'pinned' %}
  {% assign cat_count = site.pages | where_exp: "p", "p.is_pinned" | size %}
```

### URL param auto-filter (`inspo.html`)

```javascript
const urlCat = params.get('cat');
if (urlCat) { activeCategory = urlCat; }
```

This already works — `inspo.html?cat=pinned` will auto-select the Pinned tab. No JS changes needed.

### Index.html — Resume link to replace (line 241)

```html
<a href="assets/files/resume_v2.pdf" target="_blank" rel="noopener noreferrer">Resume ↗</a>
```

Replace with:

```html
<a href="{{ '/inspo.html?cat=pinned' | relative_url }}">Pinned</a>
```

### Notes query — pinned notes included automatically

```liquid
{% assign all_notes = site.pages | where_exp: "p", "p.is_note" | sort: "date" | reverse %}
```

If pinned files have `is_note: true`, they appear in notes list with no changes. If ONLY `is_pinned: true` (no `is_note`), the query needs updating to include both.

## Resume Instructions

1. Add entry to `_data/inspo_categories.yml`:
   ```yaml
   - key: pinned
     icon: "📌"
     label: "Pinned"
     unit: "resources"
     tint: "#fdf3e8"
     card_include: "inspo/pinned"
   ```

2. Create `_includes/inspo/pinned.html` — card template for inspo grid. Model on `deep-dives.html`. Items come from `site.pages | where_exp: "p", "p.is_pinned"`, not from `_data/inspo/`.

3. Update `inspo.html` count logic (around line 557-566) — add a branch for `pinned` alongside `deep-dives`:
   ```liquid
   {% if cat.key == 'deep-dives' %}
     {% assign cat_count = site.writing | size %}
   {% elsif cat.key == 'pinned' %}
     {% assign cat_count = site.pages | where_exp: "p", "p.is_pinned" | size %}
   {% else %}
     {% assign cat_count = site.data.inspo[cat.key] | size %}
   {% endif %}
   ```
   Same for the card rendering loop (line 593-600) — pinned items come from pages, not data.

4. Create 1-2 sample pinned resource files in `notes/`:
   ```yaml
   ---
   layout: note-layout
   permalink: /notes/sample-pinned-resource
   title: "Sample Pinned Resource"
   date: 2026-05-17
   tags: [example]
   is_note: true
   is_pinned: true
   ---
   ```

5. In `index.html` line 241: replace Resume link with Pinned link using `relative_url` filter

6. Build: `bundle exec jekyll build 2>&1` — must be clean

7. Test at `localhost:4000/Saptak/`:
   - `inspo.html` → Pinned tab shows, count correct, cards render
   - `inspo.html?cat=pinned` → auto-selects Pinned tab
   - `notes.html` → pinned notes appear in list (with `is_note: true`)
   - `index.html` → Pinned link in nav works, redirects to inspo pinned tab
   - All other inspo tabs still work (regression)

## Warnings

- **Pinned resources are pages, not collection docs or data files**: The inspo system has two data sources — `site.data.inspo[key]` (JSON files) and `site.writing` (collection). Pinned resources are a THIRD source: `site.pages`. The count logic and card rendering loop in `inspo.html` both need special handling (like deep-dives already has).
- **`notes/` is NOT a Jekyll collection**: Files need explicit `is_note: true` to appear in notes index. See `.claude/rules/core.md`.
- **baseurl**: All links must use `{{ site.baseurl }}` or `| relative_url`. Bare `/path` breaks GitHub Pages.
- **Don't rename DOM IDs**: `#note-list`, `#inspo-body` are used by `tags.html` for page detection.
- **CSS is inline per layout**: No shared stylesheet. Reset chip include uses `var()` with fallbacks.
- **Resume link removal**: User wants replacement, not addition. Don't keep both.
