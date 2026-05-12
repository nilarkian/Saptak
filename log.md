# Session Log

---

## 2026-05-10 — triple-stack-router overhaul + playbook copyable-code sections

**Done:**
- Extracted copyable-code-block pattern from `publishing-template.md`; appended §11 to `html-notes-playbook.md`, §10 to `markdown-notes-playbook.md`, §10 to `deep-dive-playbook.md`; each section has format-specific gate ("only if reader must copy and run")
- Full overhaul of `notes/triple-stack-router.html` (v1 → v2): rewrote content from `3-Layer-llm-router.md`, added §03 Usage (new) with 3 copyable JS/CLI blocks, split setup into interleaved protocol+code phases, tightened heuristics to 20 one-sentence laws (5 clusters), added clipboard copy-button component

**Worked:** Interleaving setup steps with their code blocks (vs. prose-then-code) significantly reduced cognitive load; one-sentence laws per expanded-drill are far more scannable than paragraph-per-step format.

**Didn't work:** Output token limit mid-session forced a context break; file had to be written in resumed session.

**Next:** Visual QA pass on rendered note (`bundle exec jekyll serve`); verify copy buttons functional in browser.

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
