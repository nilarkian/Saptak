# Workflow — Saptak

## Local Development
Serve: `bundle exec jekyll serve --livereload` (Windows, requires wdm gem)
Never run `jekyll` without `bundle exec` — version mismatch will break the build.
Preview URL: `http://localhost:4000/Saptak`

## Verification
Build check: `bundle exec jekyll build 2>&1`
PASS = exit 0, no WARN lines about invalid frontmatter or missing layouts.
FAIL = report exact error lines and file paths. Fix before committing.

## Adding a Note
1. Create `notes/[slug].md`
2. Use Pattern B frontmatter (see content.md rules)
3. Do NOT add Obsidian fields — no `id:`, `w-status:`, `series:`, `project:`, wikilinks

## Adding a Deep-Dive
1. Create `_writing/[slug].md`
2. Use Pattern A frontmatter (see content.md rules)
3. Auto-appears in Inspo "Deep Dives" tab — no registration needed

## Adding Inspo Content
Append to `_data/inspo/[type].json`. Read 2 existing entries first — schema varies per category.

## Adding a Tag
Add to `_data/tags.yml` BEFORE using in any frontmatter. Tags not in this file appear under "Other".

## Python Data Scripts
- `yt.py` → YouTube feed refresh (also runs in GitHub Actions daily at 18:00 UTC)
- `tagger.py` → tag suggestions for existing notes
- `tweet.py` → Twitter/X data fetch
- `missing-tags.py` → audit notes with missing/invalid tags

## Graphify Navigation
Use `graphify-out/wiki/index.md` as architecture entrypoint for cross-file questions.
After major structural changes: update the graph (see graphify scripts).

## Deploy
Push to main → GitHub Pages auto-builds (native Jekyll builder, no custom Actions step).
`update-feed.yml` is a data-refresh job only — not a deploy pipeline.

## Plan Mode
Enter plan mode (Shift+Tab ×2) for any task touching 3+ files or any layout change.
