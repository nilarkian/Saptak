# Color Catalog

Seed combos for the `/palette` skill. Each row is **inspiration only** — Claude generates a full
design.md-compliant 18-token `:root` palette *derived from* the seeds. Seeds guide hue, mood, and
contrast direction; they are not applied verbatim to CSS.

## Schema

| id | name | seeds | mood |
|----|------|-------|------|
| id | Catalog key passed to `/palette`. | 2–4 inspo hex values, comma-separated. | Short phrase guiding tone, contrast, atmosphere. |

## Catalog

| id | name    | seeds                                    | mood                                               |
|----|---------|------------------------------------------|----------------------------------------------------|
| 01 | paper   | `#f7f4ee, #1c1a14, #c8860a, #1a1f1c`   | Warm editorial, ink-on-paper, amber accent          |
| 02 | slate   | `#f0f2f5, #111827, #2f6fb0, #0f1724`   | Cool technical, calm blue accent, high contrast     |
| 03 | ember   | `#1a1614, #f2e9e0, #e8743b, #0f0c0a`   | Dark warm, glowing orange accent, near-black ground |
| 04 | forest  | `#f2f5f0, #1a2418, #3a7d44, #141f18`   | Organic green, earthy ink, natural depth            |
| 05 | mono    | `#f5f5f5, #111111, #6b4fbb, #0d0d0d`   | High-contrast neutral, single bold purple accent    |
| 06 | dusk    | `#fdf6ee, #2d1f3d, #c0608e, #1a1028`   | Warm cream surface, deep plum ink, rose accent      |
| 07 | arctic  | `#edf6fb, #0d2030, #1eb8d0, #061420`   | Icy pale surface, deep navy ink, cyan accent        |
| 08 | sepia   | `#f5ede0, #2c1e0f, #9b5d27, #1a1208`   | Old-paper tones, deep brown ink, bronze accent      |

## Usage

```
/palette paper notes/feyn.html           → apply catalog combo 'paper'
/palette ember notes/triple-stack.html   → apply catalog combo 'ember'
/palette "warm rose, soft" notes/feyn.html → free description → generates + saves new row
```

New combos (free descriptions not in catalog) are appended here automatically after generation.
