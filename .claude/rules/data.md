---
paths:
  - "_data/**/*.yml"
  - "_data/**/*.json"
---
# Data Rules — Saptak

## Tag Registry — `_data/tags.yml`
Source of truth for all tags. Add here BEFORE using a tag in any frontmatter.
Tags not here appear under "Other" in the tag sidebar — not an error, but untidy.

## Inspo Data — `_data/inspo/*.json`
Schema varies by category. Before adding an entry: read 2 existing entries in that file.
Auto-generated files (DO NOT hand-edit):
- `_data/all-yt.json`
- `_data/inspo/youtube.json`
- `_data/inspo/music.json`
These are overwritten by `yt.py` / GitHub Actions daily.

## Static Data (Edit Manually)
- `_data/MD-tweets.json` — tweet content
- `_data/cookies.json` — cookie consent config

## Inspo Category Registry — `_data/inspo_categories.yml`
New category = entry here + matching `_includes/inspo/[key].html`.
Required fields per entry: `key`, `icon`, `label`, `unit`, `tint`, `card_include`.
