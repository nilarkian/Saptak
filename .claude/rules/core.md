# Core Invariants — Saptak

## baseurl (CRITICAL)
Every internal link uses `{{ site.baseurl }}` or `| relative_url`. Bare `/path` breaks GitHub Pages.
Anti-pattern: `href="/notes/slug"` → Correct: `href="{{ '/notes/slug' | relative_url }}"`

## CSS Architecture
CSS is inline in each layout's `<style>` block. No shared stylesheet. No SCSS. No `assets/css/`.
Design tokens (`--bg`, `--ink`, `--muted`, `--border`, `--pill`, `--font-head`, `--font-body`) are
redefined per-layout — read the specific layout before referencing any token.

## Dark Mode Convention
- `body` (no class) → dark (default everywhere)
- `body.light-mode` → light (home page `index.html` only)
- `body.dark` → forced dark override (notes pages)

## toc.html Ownership
`toc.html` fully owns sidebar styling. Never add `.sidebar` CSS or `<aside>` HTML in any layout
that already includes `toc.html`. Violating this duplicates the sidebar.

## Build Output
Never edit `_site/`. It is generated. All changes go to source files.

## notes/ Is Not a Collection
`notes/` is a regular directory included via `_config.yml → include: [notes]`.
It is NOT a Jekyll collection. Files need `is_note: true` frontmatter to be treated as notes.
Only `_writing/` is a formal collection (output: true).
