# Session Log

---

## 2026-05-10 — triple-stack-router note audit

**Done:**
- Audited `notes/triple-stack-router.html` (v1) against all three source files: `95-token-reduction.md`, `TRIPLE-MODEL-ROUTER-PROMPT.md` (v2), `TRIPLE-STACK LLM ROUTER — CLAUDE CODE SETUP.md` (v1)
- Fixed critical routing bug: note incorrectly labeled T2 as "default (no purpose)"; actual classifier defaults to T3 (precision). Fixed lead text + T2/T3 cards.
- Added missing `AbortError` to T2 retry policy list
- Added prompt-heuristic routing note to T1 card (short greeting/ack < 40 chars → T1 even without purpose)
- Added 6th habit card: Tool-Call Economy (§6 of doctrine — significant omission for agent-loop users)
- Expanded Honest Accounting drill with explicit 3-delta template (−X compression / +Y permanent-memory / +Z doctrine-install, never net)

**Worked:** Cross-referencing code in `tiered-ask.cjs` caught the default-routing bug that prose alone missed.

**Next:** Visual QA pass on rendered note; consider whether Tool-Call Economy warrants its own section vs. habit card.

---

## 2026-05-10

**Done:**
- Added future-date filtering to `inspo.html`: cards with `data-date` ahead of today are hidden client-side via `isFuture()` check in `applyInspoFilter()`
- Tab counts corrected at load via `correctInitialCounts()` to exclude future items; `dataset.defaultCount` updated so tag-clear restores accurate numbers
- Modified `yt.py` to schedule new videos/music one-per-day instead of all landing on same date: `get_occupied_dates()` reads shared date pool from both feeds, `next_free_dates()` starts from `max(occupied)+1`, assigns consecutive free dates to new items before `build_feed()` runs

**Worked:** Both features composable — future scheduling in yt.py drips content; inspo.html hides it until date arrives.

**Next:** Test with real run of yt.py to verify drip dates appear correctly in youtube.json/music.json.

---
