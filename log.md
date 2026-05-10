# Session Log

---

## 2026-05-10

**Done:**
- Added future-date filtering to `inspo.html`: cards with `data-date` ahead of today are hidden client-side via `isFuture()` check in `applyInspoFilter()`
- Tab counts corrected at load via `correctInitialCounts()` to exclude future items; `dataset.defaultCount` updated so tag-clear restores accurate numbers
- Modified `yt.py` to schedule new videos/music one-per-day instead of all landing on same date: `get_occupied_dates()` reads shared date pool from both feeds, `next_free_dates()` starts from `max(occupied)+1`, assigns consecutive free dates to new items before `build_feed()` runs

**Worked:** Both features composable — future scheduling in yt.py drips content; inspo.html hides it until date arrives.

**Next:** Test with real run of yt.py to verify drip dates appear correctly in youtube.json/music.json.

---
