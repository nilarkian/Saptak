# HTML Note Playbook

An HTML note is a standalone `.html` file that lives in `notes/`. It earns its format: use it when the content needs visual hierarchy, skimmable components, and interactive structure that markdown cannot produce. Its job is to be the best reference for its topic — not a blog post, not a summary dump, not a pretty wrapper around thin content.

This document is the operational reference for building one.

---

## 1. What It's For

**An HTML note is not:**
- A markdown note with extra steps
- A blog post or essay (use `_writing/` for that)
- A dump of information without visual structure
- A design exercise — the design serves the content, not the other way around

**An HTML note is:**
- A rich, skimmable reference for a topic dense enough to need components
- A system: hero → nav → sections → footer, every part intentional
- A document that respects the reader's time by making structure visible
- The only format when you need: scorecards, before/afters, drill grids, pull quotes, numbered habit stacks

**Where it lives:** `notes/slug.html` with Jekyll front matter — rendered via `layout: blank` — appears in the Notes section filtered by tags.

---

## 2. The Two Archetypes

All HTML notes fall into one of two shapes. Pick before you write a line of HTML.

| Archetype | Model file | When to use |
|---|---|---|
| **Deep Reference** | `notes/feyn.html` | Dense theory; needs essay sections + quick-ref drills + scorecard |
| **Quick Playbook** | `notes/signposts.html` | Actionable how-to; type/pattern cards, before/after blocks |

---

### Archetype A: Deep Reference

One subject, taken seriously across multiple registers: quick-ref components up front, essay depth in the back half. The reader can skim the drills or read the foundations — both are complete.

**Section order:**
```
Hero
TOC Bar
→ [00] Philosophy / Pillars (phil-grid — 3-col concept cards)
→ [01] Numbered Habit Stack (habit-cards)
→ [02] Drill Grid (drill-cards, 3-col)
→ [03] Scorecard (3-col level table)
Deep Divider
→ [04] Foundations Essay (essay-body + pull-quote)
→ [05] Case Study (case-grid + pull-quote)
→ [06] Expanded Drills (exp-drill stack)
→ [07] Integrity / Ethics (integrity-block)
→ [08] Psychology / Barriers (psych-grid)
→ [09] Protocol / Method (reading-protocol)
→ [10] Conclusion (conclusion-box)
Footer
```

**Key moves:**
- Phil-grid up front answers "what is the philosophy" before habits
- Deep Divider signals the shift from reference → essay depth
- Scorecard is diagnostic, not decorative — give it real levels with real criteria
- Conclusion box ends with the thesis re-arrived-at, not restated

---

### Archetype B: Quick Playbook

One actionable system, broken into types/patterns. The reader comes back to it. Every section is a reference unit, not a chapter.

**Section order:**
```
Hero
TOC Bar
→ [00] Why / Overview (fire-box + why-list)
→ [01] Core Types / Patterns (core-grid — card per type)
→ [02–N] Per-Type Deep Sections (before/after blocks, examples, pills)
→ [N+1] Cheat Sheet / At a Glance
→ Final Protocol Callout
Footer
```

**Key moves:**
- Core-grid is the spine — one card per type/pattern, each links to its section
- Before/after blocks are the value: show the transformation, not the rule
- Swipe tags mark the single most-used example per type
- Final Protocol Callout is the one rule that governs all the others

---

## 3. Front Matter Spec

```yaml
---
layout: blank
permalink: /notes/slug/
title: "Title"
date: YYYY-MM-DD
tags: [tag1, tag2]
is_note: true
---
```

**Field rules:**

| Field | Rule |
|---|---|
| `layout` | Always `blank` |
| `permalink` | `/notes/slug/` — slug is lowercase, hyphenated, no underscores |
| `title` | Plain title — no subtitle here, put it in the hero-sub |
| `date` | ISO format: `YYYY-MM-DD` |
| `tags` | Array. Use existing tags from `_data/tags.yml` where possible |
| `is_note` | Always `true` — required for Notes index to include the file |

---

## 4. Design System

### Palettes — pick one per note

**Never mix tokens across palettes in the same file.**

#### Scholar Palette (`feyn.html`)

Use for: academic, conceptual, theory-heavy topics. Chalkboard-dark hero.

```css
:root {
  --paper:     #f7f4ee;
  --paper-alt: #edeae0;
  --paper-dark:#e4e0d4;
  --ink:       #1c1a14;
  --ink-soft:  #3d3a2e;
  --muted:     #7a7460;
  --border:    #ccc9b8;
  --amber:     #c8860a;
  --amber-lt:  #fef3dc;
  --amber-mid: #fde8a8;
  --red:       #b83c2a;
  --red-lt:    #fdf0ee;
  --green:     #2a6639;
  --green-lt:  #eaf4ed;
  --blue:      #1e4478;
  --blue-lt:   #e8eef8;
  --chalk:     #ffffff;
  --board:     #1a1f1c;   /* hero background */
}
```

**Typography:** `Lora` (headings, pull-quotes, conclusion) + `DM Sans` (body) + `DM Mono` (labels, nav, badges)

**Google Fonts import:**
```html
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,700;1,500;1,700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
```

---

#### Editorial Palette (`signposts.html`)

Use for: practical, writing, process topics. High-contrast ink hero with accent circle.

```css
:root {
  --ink:         #1a1207;
  --paper:       #faf8f3;
  --paper-alt:   #f3f0e8;
  --accent:      #f5b800;
  --accent-dark: #c9920a;
  --red:         #e03c2f;
  --green:       #2a7a3b;
  --blue:        #1e4fa8;
  --blue-light:  #dce8ff;
  --yellow-light:#fff8d6;
  --muted:       #7a7060;
  --border:      #d6d0c0;
  --before-bg:   #fff0ee;
  --after-bg:    #edfaf1;
  --signpost-bg: #fff9e3;
  --effect-bg:   #e8eeff;
}
```

**Typography:** `Playfair Display` (headings) + `DM Sans` (body) + `DM Mono` (labels, nav)

**Google Fonts import:**
```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
```

---

### Layout

```css
.wrapper {
  max-width: 980px;   /* Scholar: 980px | Editorial: 1000px */
  margin: 0 auto;
  padding: 0 48px;
}
.section {
  padding: 64px 0 52px;
  border-bottom: 1px solid var(--border);
}
.section:last-child { border-bottom: none; }
```

Max content widths: `980px` (Scholar/feyn) · `1000px` (Editorial/signposts)

---

## 5. Component Library

Each component: name, class, description, when to use, copy-paste HTML scaffold.

---

### 1. Hero

**Class:** `.hero`  
Dark background, full-width entry. Sets tone for the entire note.  
**When:** Always — every HTML note starts here.

**Scholar scaffold:**
```html
<div class="hero">
  <a href="{{ site.baseurl }}/notes.html" class="back-btn">← Notes</a>
  <div class="hero-eyebrow">🧰 Playbook</div>
  <h1>Title With <em>Key Word</em><br>On Second Line</h1>
  <p class="hero-sub">One sentence. What this teaches and why it matters.</p>
  <div class="hero-pills">
    <span class="hero-pill gold">Section Name</span>
    <span class="hero-pill gold">Section Name</span>
    <span class="hero-pill">Section Name</span>
  </div>
</div>
```

**Rules:**
- `<em>` inside h1 = accent color on the key concept word
- `hero-pill gold` for primary sections, plain `hero-pill` for secondary
- `hero-eyebrow` = category label (e.g. "🧰 Playbook", "✍️ Writing", "📐 Design")
- `hero-sub` = one sentence only — what the note teaches

---

### 2. TOC Bar

**Class:** `.toc-bar`  
Sticky navigation. One link per major section.  
**When:** Every HTML note. Placed immediately after the hero.

```html
<nav class="toc-bar">
  <a href="#philosophy">Philosophy</a>
  <a href="#habits">Habits</a>
  <a href="#drills">Drills</a>
  <a href="#scorecard">Scorecard</a>
  <a href="#conclusion">Conclusion</a>
</nav>
```

**Rules:**
- Every `href="#id"` must match a `<section id="">` exactly
- Labels ≤ 2 words
- `position: sticky; top: 0; z-index: 100;` — always visible

---

### 3. Section Label

**Class:** `.section-label`  
Numbered orientation label above every h2. Extends right via `::after` line.  
**When:** Every section without exception.

```html
<div class="section-label">01 — Core Principles</div>
<h2>Section Title</h2>
```

**Rules:**
- Format: `NN — Description` (zero-padded 2-digit number)
- Starts at `00` for the first section
- Description = 2–3 words naming the section's category, not its title

---

### 4. Lead Text

**Class:** `.lead`  
Large intro sentence. Sets up the section before components appear.  
**When:** Immediately after h2 in any section that needs orientation before components.

```html
<p class="lead">One or two sentences. What this section does and why it matters for the reader.</p>
```

**Rules:**
- Max-width: 720px
- Not a summary — a frame. Tells the reader how to use what follows.

---

### 5. Phil Grid / Core Grid

**Classes:** `.phil-grid` / `.core-grid`  
3-column concept cards. Phil-grid = equal columns with border separator. Core-grid = auto-fill responsive.  
**When:** Introducing 3 foundational concepts, types, or principles.

**Phil Grid (Scholar):**
```html
<div class="phil-grid">
  <div class="phil-card">
    <span class="phil-card-icon">🎯</span>
    <div class="phil-card-label">Label</div>
    <p>Description. <strong>Key term</strong> in bold.</p>
  </div>
  <!-- repeat × 3 -->
</div>
```

**Core Grid (Editorial):**
```html
<div class="core-grid">
  <div class="core-card">
    <div class="core-card-num">01</div>
    <h3>Type Name</h3>
    <p class="tagline">One-line description in italic.</p>
    <p class="use-for">Use for: specific situation.</p>
    <div class="example-pills">
      <span class="pill">example phrase</span>
    </div>
    <span class="swipe-tag">★ Most-used</span>
  </div>
  <!-- repeat -->
</div>
```

---

### 6. Habit Card

**Class:** `.habit-card`  
Numbered stack card. Dark number column left, do/rule two-column right.  
**When:** Numbered behaviors, habits, or rules with both a "what" and a "why/constraint."

```html
<div class="habits-stack">
  <div class="habit-card">
    <div class="habit-num">1</div>
    <div class="habit-body">
      <h3>Habit Name</h3>
      <p class="habit-context">Trigger: when this habit fires.</p>
      <div class="habit-row">
        <div class="habit-tag do">
          <span class="tag-label">The Habit</span>
          What you do. <strong>Key action bolded.</strong>
        </div>
        <div class="habit-tag rule">
          <span class="tag-label">The Rule</span>
          The constraint or test that keeps it honest.
        </div>
      </div>
    </div>
  </div>
</div>
```

---

### 7. Drill Card

**Class:** `.drill-card`  
Badge header + ordered step list + result bar.  
**When:** High-intensity exercises with a defined outcome. Use in 3-column `drills-grid`.

```html
<div class="drills-grid">
  <div class="drill-card">
    <div class="drill-header">
      <div class="drill-badge">A</div>
      <div>
        <h3>Drill Name</h3>
        <span class="drill-sub">One-line framing.</span>
      </div>
    </div>
    <ol class="drill-steps">
      <li><span class="step-num">1</span><span>Step one.</span></li>
      <li><span class="step-num">2</span><span>Step two.</span></li>
      <li><span class="step-num">3</span><span>Step three.</span></li>
    </ol>
    <div class="drill-result">What this forces / produces</div>
  </div>
</div>
```

---

### 8. Scorecard

**Class:** `.scorecard`  
3-column diagnostic table: level / what-you-can-do / how-to-verify. Dark final row = mastery.  
**When:** Any topic with meaningful levels of understanding or competence.

```html
<div class="scorecard">
  <div class="scorecard-header">
    <span>Level</span>
    <span>What You Can Do</span>
    <span>How to Verify</span>
  </div>
  <div class="scorecard-row">
    <span class="level-badge">Level 1</span>
    <span class="scorecard-indicator">Indicator statement.</span>
    <span class="scorecard-verify">Verification method.</span>
  </div>
  <div class="scorecard-row mastery">
    <span class="level-badge">Level 4 ★</span>
    <span class="scorecard-indicator">Mastery statement.</span>
    <span class="scorecard-verify">How mastery is verified.</span>
  </div>
</div>
```

---

### 9. Pull Quote

**Class:** `.pull-quote`  
Amber left-border block quote. Lora italic. Optional `<cite>`.  
**When:** The single sentence that IS the section's thesis. Not for supporting evidence — for the claim itself.

```html
<div class="pull-quote">
  <p>"The quote that is the thesis of this section."</p>
  <cite>— Source Name</cite>
</div>
```

**Rules:**
- One per section maximum
- Must be a direct quote or a formulation precise enough to quote
- Do not use for general statements — use `essay-body` prose for those

---

### 10. Expanded Drill

**Class:** `.exp-drill`  
Full-width card: header with frequency badge + step list panel + outcome panel side-by-side.  
**When:** Deep practice drills with explicit outcomes. Stack vertically in `.expanded-drills`.

```html
<div class="expanded-drills">
  <div class="exp-drill">
    <div class="exp-drill-header">
      <div class="exp-drill-num">1</div>
      <h3>Drill Name</h3>
      <span class="exp-drill-freq">Daily</span>
    </div>
    <div class="exp-drill-body">
      <div class="exp-drill-steps">
        <ul>
          <li>Step one — specific action.</li>
          <li>Step two — specific action.</li>
          <li>Step three — specific action.</li>
        </ul>
      </div>
      <div class="exp-drill-outcome">
        <span class="outcome-label">Outcome</span>
        <p>What this produces over time.</p>
      </div>
    </div>
  </div>
</div>
```

**Frequency badge values:** `Daily` / `Weekly` / `Monthly` / `As Needed`

---

### 11. Integrity Block

**Class:** `.integrity-block`  
Dark background block with 2-column amber-bordered list.  
**When:** Rules, ethics, non-negotiables, or "do this or the whole system fails" items.

```html
<div class="integrity-block">
  <h3>Block Title</h3>
  <p class="ib-sub">One sentence framing what these rules govern.</p>
  <ul class="integrity-list">
    <li><strong>Rule Name</strong> Explanation of the rule in 1–2 sentences.</li>
    <li><strong>Rule Name</strong> Explanation of the rule in 1–2 sentences.</li>
    <li><strong>Rule Name</strong> Explanation of the rule in 1–2 sentences.</li>
    <li><strong>Rule Name</strong> Explanation of the rule in 1–2 sentences.</li>
  </ul>
</div>
```

---

### 12. Psych / Case Grid

**Classes:** `.psych-grid` / `.case-grid`  
3-column colored cards. Psych = red-lt (barriers). Case = neutral white (comparisons).  
**When:** Psych-grid for failure modes, cognitive barriers. Case-grid for side-by-side comparisons or case study facets.

**Psych Grid:**
```html
<div class="psych-grid">
  <div class="psych-card">
    <span class="pc-label">Barrier 1</span>
    <strong>Barrier Name</strong>
    Description of the barrier and why it exists.
  </div>
</div>
```

**Case Grid:**
```html
<div class="case-grid">
  <div class="case-card">
    <span class="cc-label">Facet Label</span>
    <strong>Finding or verdict.</strong>
    Explanation in 2–3 sentences.
  </div>
</div>
```

---

### 13. Reading Protocol

**Class:** `.reading-protocol`  
Numbered step stack. Dark number column left, body right. Alternating row background.  
**When:** Any sequential process with distinct named steps and optional sub-notes.

```html
<div class="reading-protocol">
  <div class="rp-step">
    <div class="rp-num">1</div>
    <div class="rp-body">
      <strong>Step Name</strong>
      <span>Sub-note or clarification. Smaller text, muted color.</span>
    </div>
  </div>
  <!-- repeat -->
</div>
```

---

### 14. Conclusion Box

**Class:** `.conclusion-box`  
Paper-alt background with large decorative quote mark. Lora italic body.  
**When:** Final section. The thesis re-arrived-at, not restated.

```html
<div class="conclusion-box">
  <p>The central insight, restated with new weight now that the reader has the context.</p>
  <p>A second sentence that opens outward — what this means beyond the topic.</p>
  <p class="c-final">The plainest version. <strong>The word that matters most.</strong></p>
</div>
```

---

### 15. Final Protocol Callout

**Class:** `.final-protocol`  
Amber-tinted callout with amber left border and DM Mono label.  
**When:** The one rule that governs all the others. The "if you remember nothing else" item.

```html
<div class="final-protocol">
  <span class="fp-label">⚑ Protocol Name</span>
  The governing rule stated plainly. <strong>The critical phrase bolded.</strong> Why it matters.
</div>
```

---

### 16. Deep Divider

**Class:** `.deep-divider`  
Full-width dark separator. Lines on both sides of centered italic text + icon.  
**When:** Signals a major register shift — e.g., quick-reference → essay depth in Deep Reference notes.

```html
<div class="deep-divider">
  <div class="deep-divider-line"></div>
  <span class="deep-divider-icon">🔬</span>
  <span class="deep-divider-text">Section Title — A Deep Dive</span>
  <div class="deep-divider-line"></div>
</div>
```

---

### 17. Fire Box

**Class:** `.fire-box`  
Dark background highlight block. Single strong statement with amber bold.  
**When:** (Editorial palette only) The "this is the thing" statement — the uncomfortable truth or the core rule the whole note rests on.

```html
<div class="fire-box">
  Opening sentence framing the problem. <strong>The key claim that changes how the reader sees everything after.</strong> The consequence.
</div>
```

---

### 18. Why List

**Class:** `.why-list`  
Arrow-prefixed list. Border-top separators between items.  
**When:** (Editorial palette only) Reasons, evidence, or benefits — ordered by importance.

```html
<ul class="why-list">
  <li>
    <span class="why-arrow">→</span>
    <span>Reason or evidence. Specific and falsifiable.</span>
  </li>
  <!-- repeat -->
</ul>
<div class="bottom-line">The one-sentence takeaway from everything above.</div>
```

---

### 19. Before / After Block

**Classes:** `.before-block` / `.after-block` (or inline via `--before-bg` / `--after-bg`)  
Red-tinted "before" + green-tinted "after" side-by-side or stacked.  
**When:** (Editorial palette only) Showing a transformation: bad → good, weak → strong, unclear → precise.

```html
<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin:24px 0;">
  <div style="background:var(--before-bg); border-left:4px solid var(--red); padding:18px 20px; border-radius:0 6px 6px 0;">
    <div style="font-family:'DM Mono',monospace; font-size:10px; letter-spacing:0.15em; text-transform:uppercase; color:var(--red); font-weight:700; margin-bottom:8px;">Before</div>
    <p style="font-size:15px;">The weak version.</p>
  </div>
  <div style="background:var(--after-bg); border-left:4px solid var(--green); padding:18px 20px; border-radius:0 6px 6px 0;">
    <div style="font-family:'DM Mono',monospace; font-size:10px; letter-spacing:0.15em; text-transform:uppercase; color:var(--green); font-weight:700; margin-bottom:8px;">After</div>
    <p style="font-size:15px;">The strong version — what specifically changed.</p>
  </div>
</div>
```

---

### 20. Pill Tags

**Classes:** `.pill` / `.swipe-tag`  
Small tag labels. Pills for neutral categorization; swipe-tags for "most-used" call-outs.  
**When:** Inside core-cards or hero-pills to tag examples or highlight the canonical case.

```html
<div class="example-pills">
  <span class="pill">example phrase</span>
  <span class="pill">another example</span>
</div>
<span class="swipe-tag">★ Most-used</span>
```

---

### 21. Footer

**Class:** `.doc-footer`  
Dark mono. Note title left, summary pills right.  
**When:** Always — every HTML note ends here.

```html
<footer class="doc-footer">
  <span><strong>🧰 Note Title</strong></span>
  <span>Section Name · Section Name · Section Name</span>
</footer>
```

---

## 6. Tone & Design Voice

**The test:** Does every visual element earn its place by serving the reader's comprehension? If it's decorative, remove it.

### Do

- **Dark hero, paper body** — high contrast entry, warm reading field. Never reverse this.
- **Amber/gold as single accent** — labels, numbers, hover states, key claims. It signals importance, not decoration.
- **Section labels in DM Mono uppercase** — they orient before h2 explains. Never skip them.
- **Pull quotes only for the thesis** — one per section, only when the sentence earns it.
- **Hover states on every card** — `box-shadow` offset + `border-color` shift. Subtle. No animation.
- **Responsive at 640px and 700px** — grids collapse to single-column. Always add the `@media` rule.

### Don't

- **Mix palettes** — Scholar tokens in an Editorial file or vice versa. One palette per file.
- **More than 2 font families + DM Mono** — the fonts are load-bearing, not decorative.
- **Color for decoration** — every token must carry semantic load (red = before/wrong/barrier, green = after/outcome, amber = important/accent, blue = informational).
- **Skip `section-label`** — it orients the reader's sense of position before h2 does.
- **`position: absolute` backgrounds beyond the hero** — stay flat in content zones.
- **Inline `style=""` except for one-off h3 subtitle overrides** — all other styles in `:root` + class selectors.
- **Long lead text** — `.lead` is orientation, not a second introduction. Two sentences max.

---

## 7. How to Use Your Material

Turn raw notes, outlines, or research into a finished HTML note.

---

**Step 1 — Pick archetype.**

Dense theory with definitions, levels, drills, foundations → **Deep Reference**.  
Actionable system with types, patterns, before/afters → **Quick Playbook**.

If you're unsure: can the reader use it as a reference they return to without reading linearly? If yes → Quick Playbook. If they need to read through to build understanding → Deep Reference.

---

**Step 2 — Pick palette.**

| Topic type | Palette |
|---|---|
| Academic, conceptual, theory, science, philosophy | Scholar |
| Writing, process, communication, practical craft | Editorial |

---

**Step 3 — Write front matter.**

Copy the template from §3. Fill `permalink` with your slug. Set `date` to today. Choose 2–4 tags from `_data/tags.yml`.

---

**Step 4 — Build the Hero.**

Write these four elements in order:
1. `hero-eyebrow` — topic category with emoji (e.g. `✍️ Writing`, `🧰 Playbook`, `📐 Design`)
2. `h1` — title with `<em>` on the key concept word (accent color)
3. `hero-sub` — one sentence: what this note teaches and why it's useful
4. `hero-pills` — 3–6 pill tags named after your major sections. Use `hero-pill gold` for the 2–3 most important, plain `hero-pill` for secondary.

Write the hero last if you don't know your sections yet — or write it as a draft and revise after the sections are done.

---

**Step 5 — Write TOC links.**

List every major section as one `<a href="#id">` link. IDs must exactly match `<section id="">` values. Labels ≤ 2 words. Aim for 5–10 links — more than 10 means sections should be merged.

---

**Step 6 — Map content to components.**

For each piece of content you have, choose the right component:

| Content type | Component |
|---|---|
| 3 foundational concepts or principles | Phil Grid / Core Grid |
| Numbered behaviors with triggers and rules | Habit Card Stack |
| High-intensity exercises with outcomes | Drill Grid or Expanded Drills |
| Levels of competence | Scorecard |
| The one sentence that IS the thesis | Pull Quote |
| Rules that are non-negotiable | Integrity Block |
| Failure modes or cognitive barriers | Psych Grid |
| Sequential process with named steps | Reading Protocol |
| Transformation (bad → good) | Before/After Block |
| The one governing rule | Final Protocol Callout |
| Topic types with examples | Core Grid |
| Evidence or ranked reasons | Why List |

---

**Step 7 — Write section labels and lead text first.**

Before filling components, write the `section-label` and `h2` and `.lead` for every section. This forces you to know what each section is *for* before filling it with content.

If you can't write the lead text for a section, you don't know what that section argues yet. Find it before building the component.

---

**Step 8 — Run design audit prompts (§9).**

Run Prompt E ("Why Does This Look Cheap?") first — it gives the headline problem fast. Then run Prompts A–D for each layer. Paste the rendered HTML, not the source — the audit needs to see what the reader sees.

---

**Step 9 — Run pre-publish checklist (§8).**

---

## 8. Pre-Publish Checklist

- [ ] **Front matter:** all 6 fields present — `layout`, `permalink`, `title`, `date`, `tags`, `is_note`
- [ ] **`permalink`** slug is lowercase and hyphenated
- [ ] **Hero:** eyebrow, h1 with `<em>`, hero-sub (one sentence), ≥ 3 hero-pills
- [ ] **TOC links** all have matching `<section id="">` values
- [ ] **Palette is single** — no cross-token mixing (Scholar or Editorial, not both)
- [ ] **Every section has a `section-label`** in format `NN — Description`
- [ ] **Pull quotes** used only for thesis-level claims (max one per section)
- [ ] **Hover states** present on all card components (habit-card, drill-card, core-card)
- [ ] **No inline `style=""`** except one-off h3 subtitle color overrides
- [ ] **Footer present** with note title + section summary
- [ ] **Back button** in hero links to `{{ site.baseurl }}/notes.html`
- [ ] **Responsive** — tested at 640px and 700px breakpoints (3-col grids collapse)
- [ ] **Design audit prompts run** — at minimum Prompt E ("Why Does This Look Cheap?")
- [ ] **Section IDs unique** — no duplicate `id=""` values in the document
- [ ] **File location:** `notes/slug.html` (not `_writing/`, not `notes/slug.md`)

---

## 9. Claude Prompts

Copy-paste ready. Use on the **rendered HTML** (what the browser displays), not the source code.

---

### Prompt A — The Visual Hierarchy Surgeon

**Use when:** You have a draft and need to know if the eye lands in the right order.

**How to use:**
1. Open the rendered note in the browser
2. Take a screenshot or paste the full HTML
3. Run the prompt, get the verdict
4. Fix the ranked items in order — don't skip to item 3 before item 1 is solved

```
I'm going to share a design with you. Your job is to act as a visual hierarchy surgeon, not a compliment machine.

Do this in order:
1. Tell me where the eye lands first, second, and third — based purely on size, contrast, color weight, and position.
2. Tell me where the eye SHOULD land first, second, and third — based on the business or communication goal.
3. Identify every element that is competing for attention it hasn't earned. For each problem, give me one specific fix: exact font size change, contrast adjustment, spacing tweak, or removal.

Rules:
- No vague feedback like 'improve the hierarchy.' Name the element, name the fix.
- If something needs to be removed entirely, say so.
- Rank your fixes by impact. What one change would do the most work?
```

---

### Prompt B — The Typography Interrogation

**Use when:** Something feels off about the text but you can't name it.

**How to use:**
1. Paste the rendered HTML or screenshot
2. Get verdicts for all 5 checkpoints
3. Fix FAIL items — start with SCALE, then SPACING (highest visual impact)

```
Audit the typography in this design like a senior type director. Go through each of these checkpoints and give me a verdict + fix for each:

1. PAIRING
   - Do the fonts create tension or harmony? Is that the right call for this context?
   - Are the fonts doing distinct jobs or are they stepping on each other?
2. SCALE
   - Is there enough size contrast between heading levels?
   - Does the smallest text stay readable at actual viewing distance?
3. SPACING
   - Is line-height set for readability or left at default?
   - Is letter-spacing on headlines tightened? On all-caps labels, loosened?
   - Are paragraph widths within the 60-75 character ideal?
4. WEIGHT
   - Is font weight doing contrast work, or just decorative?
   - Are there bold elements replaceable by size contrast instead?
5. HIERARCHY SIGNAL
   - Can someone tell the difference between primary, secondary, and tertiary text at a glance?
```

---

### Prompt C — The Whitespace Pressure Test

**Use when:** The layout feels cramped or breathless — or over-spaced and disconnected.

**How to use:**
1. Paste rendered HTML or screenshot
2. Get macro then micro verdicts
3. Apply pixel recommendations directly to the CSS — these token changes are usually 1-line fixes

```
Pressure-test the whitespace and spacing in this design.

MACRO SPACING (sections, containers)
- Are section gaps large enough to signal a new zone, or do sections bleed together?
- Is there a consistent spatial rhythm (e.g., 8pt grid) or does spacing feel ad hoc?

MICRO SPACING (components, text, icons)
- Inside cards and components, is padding equal on all sides or does it look squeezed?
- Do icons have enough clearance from adjacent text?
- Are button labels getting enough horizontal padding?

BREATHING ROOM
- Which elements need more isolation to feel important?
- Where is whitespace being filled out of fear instead of intention?

PERCEIVED VALUE
- Would increasing padding in any area make the design feel more premium?
- Are there dense areas that could be split across two sections instead of one?

Give me specific pixel recommendations. If the design uses a component library, tell me which spacing tokens or utility classes to change.
```

---

### Prompt D — The Color & Contrast Stress Test

**Use when:** The palette feels wrong, muddy, or off-brand — or you need to check accessibility.

**How to use:**
1. Paste rendered HTML or screenshot
2. Fix any WCAG AA failures first — they're not optional
3. Then address sophistication issues (overused accent, unconsidered neutrals)

```
Run a full color and contrast audit on this design.

PALETTE LOGIC
- How many colors are actively in use? List them.
- Is there a clear dominant, secondary, and accent structure, or are colors roughly equal weight?
- Do any colors feel like they were added 'just because'?

EMOTIONAL SIGNAL
- What does this palette communicate emotionally? (e.g., clinical, warm, energetic, trustworthy, playful)
- Is that the right signal for the product and audience?
- Is there tension between what the colors say and what the product promises?

ACCESSIBILITY
- Flag any text/background combinations below WCAG AA (4.5:1 for body, 3:1 for large text).
- Are interactive elements distinguishable from non-interactive ones?

SOPHISTICATION
- Is the accent color being overused?
- Are there neutrals in the palette? Do they feel considered or left at defaults?
- Would swapping any color for a muted version increase perceived quality?

Give me hex values for any suggested replacements.
```

---

### Prompt E — The "Why Does This Look Cheap?" Diagnosis

**Use when:** First prompt to run on any draft. Gets the headline problem fast.

**How to use:**
1. Paste rendered HTML or screenshot
2. Read THE ROOT CAUSE item first — this is the one fix that unlocks everything else
3. Apply THE 10X TREATMENT items in impact order
4. Then run Prompts A–D to fix each layer systematically

```
Forget the positives for now. I need a brutally honest diagnosis.

THE DIAGNOSIS
- Name the 3 specific reasons this looks underdeveloped, low-budget, or unfinished.
- For each reason, tell me: what visual signal is creating that impression?

THE ROOT CAUSE
- Is the core problem typography, spacing, color, layout, component quality, or consistency?
- If you had to fix only ONE thing that would immediately shift the perceived quality, what is it?

THE 10X TREATMENT
- Give me the 3 changes that would make this design look like it cost 10x more.
- Order them by impact.
- For each: what specifically changes, and why does that change signal premium quality to a viewer?

WHAT TO KEEP
- Name one thing in this design that is already working and should not be changed.

Be direct. I want a design doctor, not a design cheerleader.
```

---

### Prompt F — Generate Section HTML

**Use when:** You have content for a section but need the component scaffold.

**How to use:**
1. Know your archetype (Deep Reference / Quick Playbook) and palette (Scholar / Editorial)
2. Know which component fits your content (use §6 content-to-component table)
3. Fill `[BRACKETED]` fields, run the prompt, paste the output into your file
4. Verify class names match the palette's CSS — don't add new classes

```
Generate the HTML for a [COMPONENT NAME] section for an HTML note.

Content:
- Section topic: [TOPIC]
- Items to include: [LIST EACH ITEM ON ITS OWN LINE]
- Palette: [Scholar | Editorial]
- Archetype: [Deep Reference | Quick Playbook]

Rules:
- Use only CSS classes from this component library: hero, toc-bar, section-label, lead, phil-grid/core-grid, habit-card, drill-card, scorecard, pull-quote, exp-drill, integrity-block, psych-grid/case-grid, reading-protocol, conclusion-box, final-protocol, deep-divider, fire-box, why-list, pill, doc-footer.
- No inline styles except one-off h3 subtitle color overrides (style="color:var(--muted); font-weight:400; font-size:15px;").
- Include section-label, h2, and lead text before the component.
- Wrap in <section class="section" id="[ID]"><div class="wrapper"> structure.
- Do not invent new CSS classes.
```

---

### Prompt G — Cold Design Review

**Use when:** Draft is complete and you want a full pre-publish check.

**How to use:**
1. Paste full HTML source (not rendered — this prompt checks structure)
2. Get PASS/FAIL for all 8 items
3. Fix every FAIL before publishing
4. Re-run Prompt E on the fixed version

```
Review this HTML note draft. For each item, say PASS or FAIL with one specific fix if FAIL.

CHECKLIST:
1. Hero has eyebrow label, h1 with <em>, hero-sub (one sentence), at least 3 hero-pills
2. TOC bar links all have matching <section id=""> values in the document
3. Palette is single — Scholar or Editorial tokens only, no mixing
4. Every section has a section-label in format "NN — Description"
5. Pull quotes used only for thesis-level claims (max one per section)
6. Hover states present on all card components (habit-card, drill-card, core-card)
7. Back button in hero links to /notes.html
8. Footer present with note title and section summary

DRAFT HTML:
[PASTE FULL HTML SOURCE]
```

---

## 10. Assets

**`notes/5 claude prompts  for better design.md`**  
Source document for Prompts A–E (Visual Hierarchy Surgeon, Typography Interrogation, Whitespace Pressure Test, Color & Contrast Stress Test, "Why Does This Look Cheap?" Diagnosis). The prompts in §9 are embedded verbatim from this file — if the source is updated, update §9 to match.

**`notes/feyn.html`**  
Reference implementation for the Deep Reference archetype. Scholar palette. Components present: hero (Scholar), TOC bar, section-label, lead, phil-grid, habit-card, drill-card, scorecard, final-protocol, deep-divider, essay-body, pull-quote, case-grid, expanded-drills, integrity-block, psych-grid, reading-protocol, conclusion-box, doc-footer.

**`notes/signposts.html`**  
Reference implementation for the Quick Playbook archetype. Editorial palette. Components present: hero (Editorial), TOC bar, section-label, lead, fire-box, why-list, bottom-line, core-grid, core-card, example-pills, swipe-tag, before/after blocks, doc-footer.

---

*This playbook reflects the design system and component patterns of `feyn.html` and `signposts.html` as of May 2026. Update when a new component pattern appears across two or more new notes.*
