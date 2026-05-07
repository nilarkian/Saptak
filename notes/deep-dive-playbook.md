---
project:
  - "[[notes]]"
next page➡️:
---
# Deep Dive Playbook

A deep dive is a curated, argued piece of writing — not a summary, not a link dump. It lives in the Inspo section alongside tools, tweets, and music. Its job is to tell the reader what something *is*, why it *matters*, and what's *uncomfortable* about it. It's written for a reader who is smart and time-poor. It respects their intelligence by having a point of view.

This document is the operational reference for writing one.

---

## 1. What It's For

**A deep dive is not:**
- A Wikipedia summary
- A review ("I liked this because...")
- A neutral explainer
- A list of facts without an argument

**A deep dive is:**
- A curatorial act — you chose this thing, you own the choice
- An argument dressed as curation — every piece has a thesis
- A guide to the uncomfortable part — surface what most readers would miss or soften
- A piece that earns the reader's time by having a position

**Where it lives:** `_writing/slug.md` → rendered via `layout: deep-dive` → appears in the Inspo "Deep Dives" tab.

---

## 2. The Two Archetypes

All deep dives fall into one of two shapes.

| Archetype | Example | When to use |
|---|---|---|
| **Subject Profile** | `aspi.md` | One org, tool, resource, or dataset worth unpacking |
| **Curated List** | `graphic.md` | Multiple sources unified by a single argument |

Pick the archetype before you write a word. It determines your structure.

---

### Archetype A: Subject Profile

One subject, taken seriously. Go deep on what it is, what makes it structurally interesting, and why it matters now.

**Section order:**
```
[Hook paragraph — no header]
---
## What Is [Subject]
## [Flagship feature or product]
## [The key mechanism, dataset, or framework]
## Why It Matters [Now]
## [Comparators / context — optional]
## Why It's In Here
---
[Kicker closer — 1–2 sentences]
---
Collected by Saptak
https://nilarkian.github.io/Saptak
```

**Key moves:**
- Lead with the institutional paradox or structural surprise, not the name
- Use `**At a glance**` bullets for data-dense items
- Surface comparable alternatives in a table — it contextualises without debating
- "Why It's In Here" = your opinion. Own it. Three lines max.

---

### Archetype B: Curated List

Multiple sources, one argument. The argument is the piece. The list is the evidence.

**Section order:**
```
[Hook paragraph — no header]
[Thesis paragraph — the thread running through all items]
---
## [Section title — "The Texts", "The Films", "The Projects"]
### [Item 1 Title] — [Author/Creator]
[Annotation: 3–4 sentences]
→ [Reader directive]
---
### [Item 2 Title] — [Author/Creator]
[Annotation: 3–4 sentences]
→ [Reader directive]
---
[... repeat]
---
## Why These [N]
[One paragraph explaining why this specific set, not any other]
---
[Kicker closer — 1–2 sentences, italicised]
---
Collected by Saptak
https://nilarkian.github.io/Saptak
```

**Key moves:**
- The `→` directive on each item tells the reader *when* to read it and *what to pair it with*
- The "Why These N" section is where the argument is made explicit — don't skip it
- Items should *disagree with each other productively* — a list where everything agrees is a listicle, not a deep dive

---

## 3. Front Matter Spec

```yaml
---
layout: deep-dive
title: "Title"
number: "003"
category: websites
date: YYYY-MM-DD
tags: [tag1, tag2]
blurb: "One sentence. Blunt. No hedging."
---
```

**Field rules:**

| Field | Rule |
|---|---|
| `layout` | Always `deep-dive` |
| `title` | Plain title. No subtitle here — put it in the body as `*subtitle*` |
| `number` | Zero-padded, 3 digits, sequential. Check `_writing/` for the highest existing |
| `category` | Must match an existing key in `_data/inspo_categories.yml` |
| `date` | ISO format: `YYYY-MM-DD` |
| `tags` | Array. Use existing tags from `_data/tags.yml` where possible |
| `blurb` | Max 2 clauses. Ends with a punch, not a summary. Write it last. |

**Blurb examples:**

❌ "A look at ASPI and how it tracks critical technologies across countries."  
✅ "Tracks which countries are winning the race for 64 critical technologies — with citations, not opinions."

❌ "A collection of important essays about graphic design history."  
✅ "Seven canonical texts that shaped how designers think — and occasionally argue with each other across decades."

---

## 4. Tone Guide

**Voice:** Confident. Curatorial. Opinionated. Not academic — no hedging qualifiers, no passive-voice conclusions. Not hype — no superlatives without evidence.

**The test:** Could this sentence appear in something you'd want to read? If it sounds like a blog intro or a product description, rewrite it.

### Do

- State opinions as facts when earned by evidence
  > "That's a problem — not because it's gatekeeping, but because the same arguments keep getting reinvented."
- Name the uncomfortable thing directly
  > "The answer is often uncomfortable for Western audiences."
- Use short sentences for weight, long sentences for complexity
  > "**Most designers haven't read it.** That's a problem."
- Use "you" only when directing the reader to take an action
- Let the subject's own contradictions do the rhetorical work

### Don't

- **Throat-clearing:** "In this deep dive, I will explore..."
- **Hedging:** "arguably", "in a way", "sort of", "somewhat", "one could say", "it could be argued"
- **Superlatives without proof:** "the most important essay", "the best tracker"
- **Meta-commentary:** "this is a fascinating topic", "there's a lot to unpack here"
- **Passive voice for key claims:** "it has been argued that..." → "X argues that..."

---

## 5. Style Guide

### Document structure

- **Open** with 1–3 sentences. No header. No "Introduction." State the thesis or the surprising premise.
- **Separate major acts** with `---` horizontal rules, not headers.
- **H2** for major sections. **H3** for sub-items within a section.
- **Max width:** 880px rendered. Write for ~70-character line lengths.

### Markdown conventions

| Element | Use for |
|---|---|
| `**bold**` | Key claim, term being defined, the thing the reader must not miss |
| `*italic*` | Subtitle, qualifier, ironic distance |
| `→` | Reader directive only — "read this next" or "pair with X" |
| `> blockquote` | Direct quotes from the subject being discussed only |
| `- bullet list` | Factual enumerations only. Not for prose. |
| `\| table \|` | Comparators, at-a-glance data, structured specs |

### Inline annotation shortcodes (drafting scaffolding only — not in final output)

These are internal labels to use while drafting annotations for Curated List pieces. They name the rhetorical move you're making so you can check it consciously. Delete them before publishing.

| Code | Stands for | What it means |
|---|---|---|
| `D+A` | Design + Analysis | Describe the formal properties, then analyse what they do |
| `N+E` | Note + Elaboration | Name the key point, then unpack it |
| `A+N` | Argument + Note | State the rhetorical move, then tag its effect on the reader |
| `D+E` | Data + Effect | Cite the evidence, then state what it proves |

**Example in drafting:**
> *[D+A]* The essay is spare and declarative, the way manifestos are when they're written by people who genuinely believe them. *[D+A end]* The diagrams in the original don't argue — they demonstrate.

---

## 6. Rhetorical Devices

Six moves that recur across both existing deep dives. Use them consciously.

---

### a. The Provocation Opener

State the uncomfortable truth in sentence 1. Don't build to it — start there.

> "Design has a canon. **Most designers haven't read it.** That's a problem — not because it's gatekeeping, but because the same arguments keep getting reinvented by people who don't know they're reinventing them."

**How:** Subject + blunt verdict + brief justification. Three sentences max.

---

### b. The Institutional Paradox

Two things that shouldn't coexist — but do. State them in parallel. Let the tension carry the weight without explaining it.

> "Government-funded. Editorially independent."
> "Public funding — independent editorial line — open data."

**How:** Pair the contradiction in 2–4 words each. Don't resolve it immediately — let the reader sit with it.

---

### c. The Pivot-Against-Self

The subject contradicts or recants its own earlier position. Surface it. It proves intellectual seriousness, not inconsistency.

> "The irony is that Tschichold later rejected these principles himself, calling them too dogmatic. **But the dogma built a movement.**"

**How:** State the recantation first. Then state what it produced anyway. The reversal is the point.

---

### d. The Uncomfortable Conclusion

State the finding that cuts against the reader's priors. Don't soften it with qualifiers. Trust the reader.

> "The answer is often uncomfortable for Western audiences. That's exactly why it's worth keeping close."

**How:** Name the discomfort directly. Then give the counterintuitive reason to engage with it anyway.

---

### e. The Productive Disagreement Frame

Show that the sources you're collecting *argue with each other*. The conflict is the value, not a flaw in the curation.

> "There are hundreds of design essays. These seven earn their place because they *disagree with each other productively.* Warde and Keedy would not get along. Tschichold renounced himself. Rand and Kalman had real public disagreements. **That tension is the education.**"

**How:** Name the disagreement explicitly. Then reframe it as the reason to read the whole set together.

---

### f. The Kicker Closer

One or two sentences. Reframes everything above. Not a summary — a reorientation. The reader should feel a gear-shift.

> *"The canon doesn't require agreement. It requires engagement."*

**Test:** Could it stand alone as a tweet? If yes, it's a kicker. If it summarises what came before, it's a conclusion — rewrite it.

---

### g. Phrase Pairing

Two parallel noun phrases that contrast or complete each other. Creates rhythm and memorability.

> "with citations, not opinions"  
> "with citations, not vibes"

**How:** Pick the core noun. Then find its foil. The second phrase should be shorter or punchier than the first.

---

## 7. How to Use Your Material

Turn raw notes, links, and highlights into a publishable deep dive.

---

**Step 1 — Collect**

Dump everything into a scratch file: links, quotes, notes, reactions. No structure. Don't try to write yet.

---

**Step 2 — Find the argument**

Ask: what is the one thing this material proves that isn't obvious?

That's the thesis. Everything else either supports it or complicates it usefully. If you can't state the thesis in one sentence, you're not ready to write. Keep reading.

---

**Step 3 — Pick your archetype**

- One subject (org, tool, dataset, person) → **Subject Profile**
- Multiple sources with a shared thread → **Curated List** (the thread is the piece, not the list)

---

**Step 4 — Write the hook first**

The opening 1–3 sentences must state the uncomfortable truth or the surprising premise. If you can't write this yet, you don't know the argument yet. Stop and find it.

Do not write Section 1 and hope the hook emerges. The hook *is* the argument. It comes first in thinking, even if it comes first on the page.

---

**Step 5 — Draft the body**

Follow the archetype template from Section 2. For Curated List pieces, use the D+A / N+E shortcodes internally to name the rhetorical move in each annotation. Delete them before publishing.

Use `→` directives to guide reading order between items. Every directive should tell the reader *why* now, not just *what* next.

---

**Step 6 — Write the kicker**

One or two sentences. Gear-shift, not summary. Test it against: could this stand alone?

If it summarises, cut it and try again. The kicker should feel like the argument finally arriving — not repeating it.

---

**Step 7 — Write the blurb last**

The `blurb` front matter field is the hardest sentence to write. It goes last because you don't know what the piece *proves* until it's done.

It should be what the piece *proves*, not what it *covers*.

> Covers: "A look at ASPI and its Critical Technology Tracker"  
> Proves: "Tracks which countries are winning the race for 64 critical technologies — with citations, not opinions."

---

## 8. Pre-Publish Checklist

- [ ] **Front matter:** all fields present — `layout`, `title`, `number`, `category`, `date`, `tags`, `blurb`
- [ ] **`number`** is next in sequence — check `_writing/` for highest existing entry
- [ ] **`category`** matches a key in `_data/inspo_categories.yml`
- [ ] **`blurb`** is ≤ 2 clauses and ends with a punch, not a qualifier
- [ ] **Hook** paragraph: no header above it, states the uncomfortable truth
- [ ] **No hedging phrases** anywhere in the body: "arguably", "in a way", "sort of", "somewhat", "one could say"
- [ ] **Bold** used only for key claims — not decoration, not emphasis for excitement
- [ ] **Every `→` directive** points to something real (a URL, a named item in the piece, or a pairing instruction)
- [ ] **Kicker closer** is a reorientation, not a summary
- [ ] **Closing line:** `Collected by Saptak` followed by `https://nilarkian.github.io/Saptak`
- [ ] **File location:** `_writing/slug.md` (slug is lowercase, hyphenated)
- [ ] **Shortcodes** (D+A, N+E, etc.) removed from final output

---

## 9. Claude Prompts

Copy-paste ready. Fill in the `[BRACKETED]` fields.

---

### Prompt A — Find the Argument

Use when: you have raw notes but no thesis yet.

```
Here are my raw notes on [SUBJECT]:

[PASTE NOTES]

What is the single most surprising or uncomfortable claim this material supports? State it in one sentence. Don't soften it.
```

---

### Prompt B — Write the Hook

Use when: you have the thesis but can't open the piece.

```
Write a 2–3 sentence opening for a deep dive about [SUBJECT].

Rules:
- No header. No "In this piece."
- State the uncomfortable truth in sentence 1.
- Bold the key claim using **markdown bold**.
- Don't summarise the whole piece — set up the argument.

Argument: [YOUR THESIS IN ONE SENTENCE]
```

---

### Prompt C — Write the Blurb

Use when: the piece is done and you need the front matter `blurb`.

```
Write a single-sentence blurb for a deep dive titled "[TITLE]".

Rules:
- Max 2 clauses.
- State what the piece proves, not what it covers.
- End with a punch, not a qualifier.
- No hedging. No "explores" or "examines."

Piece summary: [2–3 sentences describing what the piece argues]
```

---

### Prompt D — Write Entry Annotations (Curated List)

Use when: writing individual item annotations for a Curated List deep dive.

```
Write a 3–4 sentence annotation for this source:

Title: [TITLE]
Author: [AUTHOR]
Core argument: [1 sentence]
What makes it uncomfortable or surprising: [1 sentence]

Rules:
- Sentence 1: state the author's core move or premise. Be specific.
- Sentence 2: name the uncomfortable implication. Lead with "**The uncomfortable part:**"
- Final sentence: end with a → directive telling the reader when or why to read it.
- Tone: confident, curatorial, no hedging.
- No "I think", "arguably", "in a way", "sort of."
```

---

### Prompt E — Write the Kicker Closer

Use when: the body is done but the ending falls flat.

```
Write a 1–2 sentence closing for a deep dive about [SUBJECT].

The piece argues: [THESIS]

Rules:
- Not a summary. A reorientation — the argument finally arriving, not being repeated.
- Should feel like a gear-shift at the end.
- Test: could it stand alone as a tweet? It should.
- Italicise if it's a single punchy line.
```

---

### Prompt F — Full Draft from Outline

Use when: you have thesis + material and want a full draft to edit from.

```
Write a deep dive in the style of the examples below.

ARCHETYPE: [Subject Profile | Curated List]
SUBJECT: [what it is]
THESIS: [the uncomfortable claim in one sentence]
MATERIAL: [paste your notes, links, and key quotes]

STYLE RULES:
- State opinions as facts when earned by evidence.
- Short sentences for weight. Long sentences for complexity. Never long sentences for padding.
- **bold** = key claim or term. *italic* = subtitle, qualifier, or ironic distance.
- → for reader directives only (not bullets, not asides).
- No hedging: "arguably", "in a way", "somewhat", "one could say."
- Open with the uncomfortable truth. No header above the opening.
- End with a kicker closer — reorientation, not summary.
- Final two lines: "Collected by Saptak" then "https://nilarkian.github.io/Saptak"

REFERENCE EXAMPLES FOR STYLE (do not copy content — only match voice and structure):
[paste graphic.md and/or aspi.md]
```

---

### Prompt G — Cold Review

Use when: draft is written and you want a style check before publishing.

```
Review this deep dive draft against the following checklist. For each item, say PASS or FAIL with one sentence of explanation if FAIL.

CHECKLIST:
1. Hook paragraph has no header above it and states an uncomfortable truth
2. No hedging phrases (arguably, in a way, sort of, somewhat, one could say)
3. Bold used only for key claims — not decoration
4. Every → directive points to something real
5. Kicker closer is a reorientation, not a summary
6. Blurb is ≤ 2 clauses and ends with a punch
7. No throat-clearing ("In this piece, I will...")
8. No passive voice for key claims

DRAFT:
[PASTE DRAFT]
```

---

*This playbook reflects the voice and structure of the existing deep dives as of May 2026. Update it when a new pattern emerges across three or more new entries.*
