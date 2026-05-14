# Handoff: note-layout — TOC + Code Block Fixes

**Generated**: 2026-05-15
**Branch**: main
**Status**: Ready for Review / Visual QA pending

## Goal

Fix three UX issues in `_layouts/note-layout.html`:
1. Collapsing the TOC sidebar does not widen note content (freed space wasted as right margin)
2. Long code lines overflow and require horizontal scrolling
3. Code blocks invisible in dark mode (same bg color as page body)

## Completed

- [x] **TOC collapse expansion** — added `max-width:1060px` to `body.toc-collapsed .main` rule; content now grows up to 1060px when sidebar collapses from 200px to 44px
- [x] **Code block wrapping** — changed `overflow-x:auto` → `overflow-x:hidden`, added `white-space:pre-wrap` + `word-break:break-word` to `.note-body pre`; long lines wrap instead of scroll
- [x] **Dark mode code block visibility** — changed `body.dark .note-body pre { background:#1e1e1e }` (same as body bg) → `background:#252526; border:1px solid #3e3e42`; code blocks now visibly distinct

Also present (from prior session, not yet committed):
- [x] Full dark mode system (`body.dark` class, theme toggle button, localStorage persistence)
- [x] Reading progress bar, back-to-top button
- [x] Prism.js syntax highlighting (JS/Python/Bash/YAML/JSON/TS)
- [x] Complete markdown element styling (tables, images, kbd, dl, footnotes, task lists, etc.)
- [x] `toc.html` extracted as reusable include with collapsible sidebar + auto-width measurement

## Not Yet Done

- [ ] Visual browser test — `bundle exec jekyll serve` not run this session; all changes are CSS only
- [ ] Test note with long code lines to verify wrap behavior
- [ ] Confirm collapsed TOC width expansion looks right at various viewport sizes

## Failed Approaches

**TOC expand — why not JS?**
`syncMainMargin()` in `toc.html` only writes `marginLeft` inline. Adding `maxWidth` there would work but mixes layout logic into the include. CSS `body.toc-collapsed .main` rule is cleaner since JS doesn't touch `maxWidth`, so no override conflict.

**Code wrap — `overflow-wrap:anywhere` instead of `word-break:break-word`?**
`overflow-wrap:anywhere` only fires on unbreakable sequences. `word-break:break-word` more aggressively breaks identifiers and file paths within code. Chosen for reliability.

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| `max-width:1060px` on collapsed (not `none`) | 860 (expanded) + 156 (freed px) = 1016; 1060 gives breathing room; prevents text stretching to full viewport on wide screens |
| `#252526` for dark pre background | Matches existing dark mode surface color (`th`, `kbd`, `topic-tag`); consistent design token |
| Border on dark pre (`#3e3e42`) | Matches all other dark mode borders; adds contrast without a new color |

## Current State

**Working**: All three CSS fixes applied. Layout is functional.

**Broken**: Nothing known.

**Uncommitted Changes**:
- `_layouts/note-layout.html` — large diff (multiple sessions); includes dark mode, theme toggle, typography, markdown elements, and this session's 3 fixes
- `_includes/toc.html` — collapsible sidebar include (prior session)
- `_data/inspo/youtube.json` — unrelated youtube data update
- `notes/triple-tier-llm-router.md` — unrelated note edit
- `yt.py` — unrelated youtube script
- `notes/How Consistency Became One of the Biggest Problems with LLMs.md` — untracked new note
- `plan.md` — new file at root (this session's plan doc)

## Files to Know

| File | Why It Matters |
|------|----------------|
| `_layouts/note-layout.html` | All note page CSS + JS. Inline styles only — no shared stylesheet. All three fixes are here. |
| `_includes/toc.html` | Collapsible TOC sidebar. Manages `body.toc-collapsed` class and `margin-left` inline style via `syncMainMargin()`. Does NOT touch `maxWidth`. |
| `_layouts/blank.html` | Parent layout note-layout extends — minimal wrapper, don't touch |

## Code Context

**The three changed CSS rules** in `_layouts/note-layout.html`:

```css
/* Fix 1 — was: margin-left:44px only */
body.toc-collapsed .main{ margin-left:44px; max-width:1060px; }

/* Fix 2 — was: overflow-x:auto, no white-space or word-break */
.note-body pre{
  overflow-x:hidden;
  white-space:pre-wrap;
  word-break:break-word;
  /* ...other existing props unchanged... */
}

/* Fix 3 — was: background:#1e1e1e (identical to body.dark background) */
body.dark .note-body pre{background:#252526;border:1px solid #3e3e42;}
```

**Why `max-width` is separate from `margin-left`**: `.main` has `flex:1` + `margin-right:auto`. On wide viewports, flex:1 grows past max-width, and margin-right:auto absorbs the overflow. Changing `margin-left` without changing `max-width` just shifts content left — doesn't widen it. The explicit `max-width:1060px` override on `.toc-collapsed` breaks the cap and lets flex:1 use the freed space.

**TOC state flow** (`_includes/toc.html`):
```
click toggle → applyTocState() → toggles body.toc-collapsed class
             → syncMainMargin() → sets main.style.marginLeft (inline)
```
CSS `body.toc-collapsed .main { max-width:1060px }` applies because JS never sets inline `maxWidth`.

## Resume Instructions

1. Start dev server: `bundle exec jekyll serve` (from repo root)
2. Open `http://localhost:4000/Saptak/notes/` → click any note with code blocks
3. Verify code wrap: paste a note with a long single-line code snippet (100+ chars); should wrap inside block, no scrollbar
4. Verify dark mode code block: click theme toggle → code blocks should have visibly distinct `#252526` surface with border
5. Verify TOC expand: click `‹` to collapse sidebar → main content area should shift left AND get wider (up to 1060px); click `›` to expand → should shrink back to 860px

## Warnings

- CSS is **inline per layout** — no shared stylesheet. Changes here only affect `notes/` pages. `deep-dive`, `watchlist-layout` are separate.
- `body.toc-collapsed` class is set by JS in `toc.html` (which runs before `<main>` exists in DOM). The CSS rule handles initial collapsed state; JS sets `margin-left` inline on subsequent toggles. Both must agree.
- `notes/` pages need `is_note: true` in front matter to appear in notes index. `layout: note-layout` alone is insufficient.
- Prism.js loads at bottom of `note-layout.html` — re-highlight is automatic on load. If adding new language support, add the component script from the same CDN version (`1.29.0`).
