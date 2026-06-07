---
description: Research a frontier-tech development, dedup-check it, and prepend a 1-3-1 entry to watchlist.md
argument-hint: "[topic | url | empty for auto-discover]"
allowed-tools: Read, Edit, WebSearch, WebFetch, Bash
---

# /watchlist — Prepend a Watchlist Entry

Research a frontier-tech development, enforce topicality + dedup, compose a 1-3-1 entry, and prepend it to `projects/watchlist/watchlist.md`. One entry per run.

---

## Step 0 — Resolve today's date

Run:

```powershell
Get-Date -Format "MMM d"
Get-Date -Format "MMMM yyyy" | ForEach-Object { $_.ToUpper() }
```

Store:
- `DATE_SPAN` → e.g. `Jun 7` (used in `<span class="date">Jun 7</span>`)
- `MONTH_HEADER` → e.g. `JUNE 2026` (used in `## JUNE 2026`)

Do **not** trust session memory for dates — always read the system clock.

---

## Step 1 — Classify input

Inspect `$ARGUMENTS` (the text after `/watchlist`):

- Starts with `http://` or `https://` → **URL mode**: that article is the subject.
- Non-empty and not a URL → **topic mode**: research that keyword/phrase.
- Empty / blank → **discover mode**: auto-find the highest-signal frontier-tech shift in the last ~7 days.

---

## Step 2 — Research

### URL mode
1. `WebFetch` the given URL. Extract: headline, what's new, mechanism, implication, publication date.
2. One corroborating `WebSearch` (`"[headline keywords] 2026"`) to gather a second source or broader context.

### Topic mode
1. `WebSearch` the topic with a recency slant (e.g. append `"2026"` or `"latest"`). Pick the 1–2 strongest results.
2. `WebFetch` each result. Extract: what's new, mechanism, implication, primary source URL.

### Discover mode
1. Read `watchlist-topics.md`. Extract the search queries from its table (one or two per domain row).
2. Run 3–5 `WebSearch` calls spread across different domain buckets (not all the same domain).
3. From all results, pick **one** highest-signal development: the one with the clearest structural shift + a non-obvious second-order implication that has not yet been logged.
4. `WebFetch` its primary source for facts and the canonical URL.

In all modes, extract:
- The development (what happened)
- What's genuinely new (not incremental)
- The mechanism (why/how)
- The second-order implication (where leverage shifts)
- Primary source URL (canonical, normalized: strip UTM/tracking params, lowercase scheme+host)
- Optional secondary source URL
- Candidate date (article publication date; fall back to today)

---

## Step 3 — Topicality gate

**Hard filter — stop here if the development fails any criterion.**

Accept only if ALL of:
1. **Domain match:** sits in one of the watchlist theme areas (AI, semiconductors, tech-geopolitics, India deep-tech/policy/fintech, space, biotech/CRISPR, quantum, energy/nuclear/fusion, advanced manufacturing, cybersecurity, markets/capital).
2. **Structural shift:** describes something that changes *how* an industry, supply chain, or capability works — not a routine product launch, earnings beat, or generic market move.
3. **Non-obvious implication:** has a second-order effect (who gains leverage, what becomes economically fragile, what previously-blocked thing is now unblocked).
4. **Recent:** published within the last ~14 days (prefer last 7).

On failure → **STOP.** Print:

```
NOT TOPICAL — no entry written.
Reason: [one sentence]
```

---

## Step 4 — Read watchlist + build dedup sets

Read `projects/watchlist/watchlist.md` in full.

Build two sets:

**EXISTING_URLS** — every URL extracted from source lines matching `[...](url)`:
- Normalize: lowercase scheme + host, strip trailing slash, strip UTM/tracking params (`?utm_*`, `?ref=*`, `?guccounter=*`, etc.).

**EXISTING_TITLES** — every `### ` heading line, with date span + emoji stripped, lowercased.

---

## Step 5 — Dedup check

Reject and STOP if either condition holds:

1. **URL match:** candidate's primary source URL (normalized) ∈ `EXISTING_URLS`.
2. **Semantic match:** the candidate describes the same event as an existing title — same company/entity + same development, even if worded differently. Example: "Nvidia $26B open-source AI" already appears twice; don't add a third.

On rejection → **STOP.** Print:

```
ALREADY LOGGED — no entry written.
Matched: [the existing title or URL it duplicates]
```

---

## Step 6 — Compose the entry

### Emoji selection

Pick one emoji consistent with domain usage in the existing file:

| Domain | Emoji |
|--------|-------|
| AI / LLM / agents | 🤖 |
| Semiconductors / chips / photonics | 💡 |
| Quantum computing | ⚛️ |
| India (policy, startups, fintech) | 🇮🇳 |
| Space / launch / satellites | 🚀 |
| Biotech / CRISPR / gene editing | 🧬 |
| Nuclear / fusion / energy | ⚡ or ☢️ |
| Cybersecurity | 🛡️ |
| Markets / capital / funding | 💰 or 📈 |
| Manufacturing / hardware | 🏭 |
| Geopolitics / policy | 🌐 |

### Title

Short, punchy, noun-phrase or verb-led. Captures the shift, not the company's PR phrasing.
Max ~60 characters. Examples from file: "Silicon photonics escapes the lab", "AI crafts first zero-day exploit".

### Tags

Inline array, 2–5 lowercase freeform tags. No tags.yml lookup — these are free-form.
Examples: `[ai, semiconductors, photonics, datacenters]`, `[CRISPR, biotech, biosafety]`.
Use specific terms over generic ones (`silicon-photonics` over `tech`).

### Body — 1-3-1 rhythm (per `1-3-1.md`)

Structure each paragraph:
- **[1] Opening sentence** — the shift, stated plainly. Hook the skim reader.
- **[3] Expansion sentences** — clarify what's new / the mechanism / why it matters. Each adds distinct information.
- **[1] Closing sentence** — the second-order payoff: where leverage moves, what becomes fragile, what's now possible.

Sentence-length distribution:
- Ultra-short (1–3 words): ~10%
- Short (4–8 words): ~35%
- Medium (9–15 words): ~35%
- Long (16–30 words): ~20%
- After every long sentence: follow with a short or ultra-short.
- No 4+ medium sentences in a row.

Remove: filler, hedging, "it is important to note", corporate jargon, academic phrasing.
Prefer: verbs over nouns, examples over explanations, concrete over abstract.

Keep body to 3–6 sentences total (1-3-1 = 5 minimum). Aggressive chunking — no dense text walls.

### Source line

```
[source](url)
```

Add `[source2](url)` on a second line if a genuine second source adds material context. Otherwise one line only.

### Full block to assemble

```
### <span class="date">DATE_SPAN</span> EMOJI Title
tags: [tag1, tag2, tag3]

Body paragraph(s) in 1-3-1 rhythm.

[source](primary_url)

---
```

Blank line between `tags:` line and body. Blank line between body and source. Blank line before `---`.

---

## Step 7 — Prepend to watchlist

Read the top of `projects/watchlist/watchlist.md` (past frontmatter `---` block).

Find the first `## ` header line. Call it `TOP_HEADER` (e.g. `## MAY 2026`).

**Case A — same month:** `TOP_HEADER` matches `MONTH_HEADER`.
Insert the composed block immediately after the blank line following `TOP_HEADER`, before the first `### ` entry.

Edit target — find this pattern:
```
## MONTH YEAR


### <span class="date">...
```
Insert the new block + blank line between the `## ` line and the first `### `.

**Case B — new month:** `TOP_HEADER` does not match `MONTH_HEADER` (month rolled over).
Insert a new month header + the entry above `TOP_HEADER`:

```
## MONTH_HEADER


### <span class="date">DATE_SPAN</span> EMOJI Title
tags: [...]

Body.

[source](url)

---

## OLD_TOP_HEADER
```

Use `Edit` with the exact old_string matching a unique stretch at the top of the file.

Preserve existing blank-line spacing around `---` separators.

---

## Step 8 — Verify build

```bash
bundle exec jekyll build 2>&1
```

- **PASS:** exit 0, no `WARN` about invalid frontmatter or missing layouts → done.
- **FAIL:** report exact error lines. Roll back the edit (restore the previous content). Do **not** mark the task done.

---

## Step 9 — Report

Print a concise summary:

```
MODE:    [url | topic | discover]
ENTRY:   [EMOJI Title]
DATE:    [DATE_SPAN]
TAGS:    [tags]
SOURCE:  [url]
INSERT:  [new month header created | prepended under ## MONTH YEAR]
BUILD:   PASS / FAIL
```

If skipped: print the NOT TOPICAL or ALREADY LOGGED message instead.
