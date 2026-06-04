---
version: alpha
name: Saptak Notes
description: >
  Warm-paper editorial design system for Saptak's note pages.
  Ink-on-paper aesthetic with serif display type, amber accent, and a dark hero.
  Three sanctioned themes (light-paper, light-sidebar, dark) share identical token
  names so files deviate only in which tokens are remapped per theme.

colors:
  primary:         "#c8860a"   # amber — CTAs, accents, active states
  primary-lt:      "#fef3dc"   # amber tint — callout backgrounds
  primary-mid:     "#fde8a8"   # amber fill — hover shadows, card highlights
  secondary:       "#7a7460"   # muted — captions, metadata, section labels
  tertiary:        "#b83c2a"   # red — semantic error/danger
  tertiary-lt:     "#fdf0ee"   # red tint
  neutral:         "#ccc9b8"   # border — hairlines, dividers
  surface:         "#f7f4ee"   # paper — page background
  surface-alt:     "#edeae0"   # paper-alt — card headers, inner zones
  surface-dark:    "#e4e0d4"   # paper-dark — deep card surfaces
  surface-raised:  "#ffffff"   # chalk — cards, elevated white surfaces
  on-surface:      "#1c1a14"   # ink — primary text
  on-surface-soft: "#3d3a2e"   # ink-soft — body copy, captions
  board:           "#1a1f1c"   # dark hero bg / dark-theme base surface
  success:         "#2a6639"
  success-lt:      "#eaf4ed"
  info:            "#1e4478"
  info-lt:         "#e8eef8"
  error:           "#b83c2a"
  error-lt:        "#fdf0ee"

typography:
  headline-display:
    fontFamily: Lora
    fontSize: clamp(32px, 5.5vw, 64px)
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Lora
    fontSize: clamp(24px, 3.5vw, 36px)
    fontWeight: 700
    lineHeight: 1.2
  headline-md:
    fontFamily: DM Sans
    fontSize: 17px
    fontWeight: 700
    lineHeight: 1.4
  body-lg:
    fontFamily: DM Sans
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.7
  body-md:
    fontFamily: DM Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.75
  body-sm:
    fontFamily: DM Sans
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.65
  label-lg:
    fontFamily: DM Mono
    fontSize: 11px
    fontWeight: 600
    lineHeight: 1
    letterSpacing: 0.08em
  label-md:
    fontFamily: DM Mono
    fontSize: 10px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.15em
  label-sm:
    fontFamily: DM Mono
    fontSize: 9px
    fontWeight: 700
    lineHeight: 1
    letterSpacing: 0.2em

rounded:
  none: 0px
  sm:   2px
  md:   4px
  lg:   6px
  xl:   12px
  full: 999px

spacing:
  xs:          4px
  sm:          8px
  md:          16px
  lg:          24px
  xl:          32px
  2xl:         48px
  3xl:         64px
  section-v:   64px
  wrapper-h:   48px
  wrapper-max: 980px

components:
  card:
    backgroundColor: "{colors.surface-raised}"
    rounded: "{rounded.lg}"
    borderColor: "{colors.neutral}"
    borderWidth: 1.5px
    padding: 24px 28px
  card-hover:
    shadow: 4px 4px 0 {colors.primary-mid}
    borderColor: "{colors.primary}"
  hero:
    backgroundColor: "{colors.board}"
    textColor: "{colors.surface}"
    padding: 90px 48px 72px
  toc-bar:
    backgroundColor: "{colors.on-surface}"
    textColor: "{colors.surface}"
    padding: 0 48px
  sidebar-nav:
    backgroundColor: "{colors.surface-alt}"
    width: 220px
    padding: 32px 0
  sidebar-nav-dark:
    backgroundColor: "#232926"
    width: 240px
    padding: 32px 0
  section-label:
    fontFamily: DM Mono
    fontSize: 10px
    textColor: "{colors.secondary}"
    letterSpacing: 0.22em
  button-back:
    backgroundColor: transparent
    borderColor: rgba(255,255,255,0.3)
    textColor: "{colors.surface}"
    rounded: "{rounded.full}"
    padding: 6px 14px
  pill:
    backgroundColor: "{colors.surface-alt}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.sm}"
    padding: 4px 10px
  pill-dark:
    backgroundColor: "{colors.on-surface}"
    textColor: "{colors.surface}"
    rounded: "{rounded.sm}"
    padding: 4px 10px
  callout:
    backgroundColor: "{colors.primary-lt}"
    borderColor: "{colors.primary-mid}"
    rounded: "{rounded.lg}"
    padding: 24px 28px
  code-block:
    backgroundColor: "{colors.board}"
    textColor: "{colors.surface}"
    accentBorderColor: "{colors.primary}"
    rounded: "{rounded.lg}"
    padding: 20px 24px
  step-num:
    backgroundColor: "{colors.on-surface}"
    textColor: "{colors.surface-raised}"
    size: 22px
    rounded: "{rounded.sm}"
---

# Saptak Notes Design System

## Overview

Saptak's note pages are **dense long-form reference documents** — physics pedagogy, router
architecture, communication playbooks. The aesthetic is *ink on warm paper*: a serif display
typeface (Lora), DM Sans body, DM Mono for everything data-like, and a single amber accent
that pulls focus to exactly one idea per visual zone.

**Mood:** Warm, editorial, unhurried. The page should feel like a well-marked hardcover — not
a startup landing page, not a docs site, not a notebook app. Density is honest; whitespace is
earned. The dark hero is a deliberate contrast threshold: you step *into* a document.

**Three themes** share the full token vocabulary and structural primitives. Only the palette
assignments change between them. See the **Themes** section.

**What makes it distinctive:**
- Lora italic `em` in headlines coloured amber — a single typographic gesture worth more than
  a dozen design flourishes.
- `box-shadow: 4px 4px 0` with zero blur — flat editorial offset, not drop shadows.
- `section-label::after` — a `flex: 1; height: 1px` growing rule line that spans to the edge.
  Encodes the document's structure without using borders or dividers on the container.
- DM Mono at 10–11px with `letter-spacing: 0.15–0.22em` as the sole label typeface — creates
  a clear editorial voice separation between "content" and "metadata."

---

## Colors

Palette is rooted in warm neutrals with a single amber accent. Semantic colors (red, green,
blue) appear only in data-rich zones like scorecards, before/after grids, and result strips.

- **Primary `#c8860a` amber** — action color, accent, active states, section labels, eyebrows.
  Use sparingly: one amber moment per visual zone.
- **Primary-lt `#fef3dc`** — amber tint for callout backgrounds. Always paired with
  primary-mid border.
- **Primary-mid `#fde8a8`** — amber fill for hover shadows and card accents.
- **Secondary `#7a7460` muted** — captions, metadata, section labels, the quiet voice.
- **Surface `#f7f4ee` paper** — canonical page background. Warm, not white.
- **Surface-raised `#ffffff` chalk** — card surfaces. Pure white only on top of paper, not as
  a page background.
- **Surface-alt `#edeae0` paper-alt** — card headers, inner zones, drill headers. One step
  darker than surface.
- **On-surface `#1c1a14` ink** — headlines, emphasis text.
- **On-surface-soft `#3d3a2e` ink-soft** — body prose, essay sections. Softer than ink.
- **Board `#1a1f1c`** — hero background, dark-theme base, `toc-bar` on light theme. Very dark
  warm green-black. Not `#000000`.
- **Neutral `#ccc9b8` border** — all dividers, card borders, hairlines.

**Semantic only — in data zones:**
- Success `#2a6639` / success-lt `#eaf4ed`
- Info `#1e4478` / info-lt `#e8eef8`
- Error/tertiary `#b83c2a` / error-lt `#fdf0ee`

---

## Typography

Three-font system. Each font owns a distinct register; mixing registers across fonts is the
anti-pattern.

| Level | Token | Family | Size | Weight | Role |
|---|---|---|---|---|---|
| headline-display | h1 | **Lora** | clamp(32–64px) | 700 | Page titles, hero h1 |
| headline-lg | h2 | **Lora** | clamp(24–36px) | 700 | Section headers |
| headline-md | h3 | DM Sans | 17px | 700 | Sub-section headers |
| body-lg | lead | DM Sans | 18px | 400 | Opening paragraph |
| body-md | p | DM Sans | 16px | 400 | Body prose |
| body-sm | — | DM Sans | 14px | 400 | Dense data, card text |
| label-lg | nav, eyebrow | **DM Mono** | 11px | 600 | Toc-bar links, eyebrows |
| label-md | section-label | **DM Mono** | 10px | 500 | Section labels, card labels |
| label-sm | tag-label | **DM Mono** | 9px | 700 | Data tags, pill labels |

**Rules:**
- Lora owns *structural hierarchy* (h1, h2). Do not use it for body text.
- DM Mono owns *metadata and navigation* (labels, eyebrows, nav links, code). Do not use it
  for prose.
- DM Sans owns *content* (body, lead, h3). Default for anything not Lora or DM Mono.
- Lora `em` inside an h1 headline → colour to `var(--amber)`. One accent per heading maximum.
- All DM Mono instances: `text-transform: uppercase`. Always. It reads as label at any size.
- Letter-spacing on DM Mono: `0.06–0.22em` depending on size. Smaller sizes need more spacing.

**Google Fonts import (one link tag per file):**
```html
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,700;1,500;1,700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
```

---

## Layout

**Content model** for top-nav (light-paper) pages:
```
.hero              ← full-bleed dark intro
.toc-bar           ← sticky top nav strip, z-index 100
.wrapper           ← max-width 980px, padding 0 48px
  .section         ← padding 64px 0 52px, border-bottom 1px solid --border
    .section-label ← DM Mono eyebrow + growing rule line
    h2             ← Lora section header
    .lead          ← 18px opener paragraph, max-width 720px
    [components]   ← grids, cards, tables, etc.
.doc-footer        ← simple closing band
```

**Content model** for sidebar-nav pages (light-sidebar and dark themes):
```
.page              ← CSS grid: 220px [sidebar] minmax(0, 1fr) [main]
  .sidebar         ← sticky, full-height, overflow-y auto
    [nav links]
  .main            ← max-width 860px prose + components
```

**Spacing scale:**

| Token | Value | Where |
|---|---|---|
| xs | 4px | Chip/tag inner padding |
| sm | 8px | Inline gaps, icon+label |
| md | 16px | Paragraph gap, small card padding |
| lg | 24px | Gap between cards, section sub-padding |
| xl | 32px | Component top-margin |
| 2xl | 48px | Wrapper horizontal padding, hero horizontal padding |
| 3xl | 64px | Section vertical padding |
| section-v | 64px | Section `padding-top`, 52px `padding-bottom` |
| wrapper-h | 48px | Wrapper `padding: 0 48px` |
| wrapper-max | 980px | Wrapper `max-width` |

**Responsive breakpoints:**
- `≤ 900px` — toc-bar stays sticky but collapses to scrollable strip.
- `≤ 760px` — sidebar-nav pages: sidebar collapses to horizontal scroll strip above main.
- `≤ 680px` — 3-col grids → 1-col.
- `≤ 600px` — 2-col card sub-grids (habit-row etc.) → 1-col.

---

## Elevation & Depth

**Philosophy:** Depth through contrast, not blur. Shadows are editorial flat offsets.
Nothing in this system uses `blur` or `spread` in box-shadows.

| Level | Value | Usage |
|---|---|---|
| none | — | Default surfaces; rely on border + background contrast |
| card-default | `border: 1.5px solid var(--border)` | Cards at rest |
| card-hover | `box-shadow: 4px 4px 0 var(--amber-mid); border-color: var(--amber)` | Card `:hover` — the signature interaction |
| hero-overlay | `repeating-linear-gradient` chalk noise texture | `.hero::before` — subtle paper grain |
| deep-divider | `background: var(--ink)` full-bleed band | Separates major content parts |
| dark-nav | `background: var(--board)` | `.toc-bar` on light-paper theme |

**No blur. No drop-shadow.** Any `box-shadow` with a non-zero blur radius is out of system.

---

## Shapes

Shape language: **deliberately tight, editorial, not rounded**.

| Token | Value | Used for |
|---|---|---|
| none | 0px | Tables, deep-dividers, toc-bar |
| sm | 2px | step-num badges, hero-pill labels |
| md | 4px | habit-tag, data chips inside cards |
| lg | 6px | All card containers: habit-card, drill-card, phil-grid, scorecard, code-block |
| xl | 12px | Large standalone callout containers |
| full | 999px | back-btn, hero-pill standalone tags |

**Rule:** Within a single component, use one radius. Never mix `lg` border-radius on a card
with `full` on a child badge — that creates radius dissonance. The exception is `back-btn`
(full) inside the hero (no radius): they are different layers.

---

## Components

### `.hero`
Full-bleed dark intro panel. `background: var(--board)`. Contains: `.back-btn`,
`.hero-eyebrow`, `h1`, `.hero-sub`, `.hero-pills`. Optional decorative elements:
`::before` chalk grain overlay, `::after` decorative circle (amber 20% opacity).

```css
.hero {
  background: var(--board);
  color: var(--chalk);
  padding: 90px 48px 72px;
  position: relative;
  overflow: hidden;
}
```

### `.back-btn`
Absolute-positioned pill link in the hero, top-left. DM Mono, full-radius, chalk border.

```css
.back-btn {
  position: absolute; top: 24px; left: 32px;
  font-family: 'DM Mono', monospace; font-size: 12px;
  font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--chalk); text-decoration: none;
  border: 1.5px solid rgba(255,255,255,0.3);
  padding: 6px 14px; border-radius: 999px;
  transition: background 0.2s;
}
.back-btn:hover { background: rgba(255,255,255,0.12); }
```

### `.hero-eyebrow`
DM Mono amber label above h1. Has a trailing `::after` amber rule line.

```css
.hero-eyebrow {
  font-family: 'DM Mono', monospace; font-size: 11px;
  letter-spacing: 0.2em; text-transform: uppercase; color: var(--amber);
  margin-bottom: 20px; display: flex; align-items: center; gap: 10px;
}
.hero-eyebrow::after {
  content: ''; display: inline-block;
  width: 40px; height: 1px; background: var(--amber);
}
```

### `.toc-bar`
Sticky top navigation strip. Dark (`--ink` background). DM Mono links, amber hover.
Scrolls horizontally on narrow viewports without scrollbar visible.

```css
.toc-bar {
  background: var(--ink); padding: 0 48px;
  display: flex; gap: 0; overflow-x: auto; scrollbar-width: none;
  position: sticky; top: 0; z-index: 100;
}
.toc-bar a {
  padding: 13px 18px; font-size: 11px; font-weight: 600;
  letter-spacing: 0.08em; text-transform: uppercase; color: rgba(247,244,238,0.55);
  text-decoration: none; white-space: nowrap;
  font-family: 'DM Mono', monospace; transition: color 0.15s;
}
.toc-bar a:hover { color: var(--amber); }
```

### `.sidebar` (sidebar-nav pages)
Left sticky sidebar, 220px, `--paper-alt` background on light-sidebar theme;
`#232926` on dark theme. Links use DM Mono label-md sizing.

```css
.page { display: grid; grid-template-columns: 220px minmax(0,1fr); min-height: 100vh; }
.sidebar {
  background: var(--paper-alt); border-right: 1px solid var(--border);
  padding: 32px 0; position: sticky; top: 0; height: 100vh; overflow-y: auto;
}
```

### `.section-label`
DM Mono eyebrow with a `flex: 1` growing rule line to the right edge. **The signature
structural element.** The line is not a border — it is a CSS `::after` flex child.

```css
.section-label {
  font-family: 'DM Mono', monospace; font-size: 10px;
  letter-spacing: 0.22em; text-transform: uppercase; color: var(--muted);
  margin-bottom: 12px; display: flex; align-items: center; gap: 10px;
}
.section-label::after {
  content: ''; flex: 1; height: 1px; background: var(--border);
}
```

### Cards
All cards: `border: 1.5px solid var(--border); border-radius: 6px; overflow: hidden;
background: var(--chalk); transition: box-shadow 0.2s`.

Hover state: `box-shadow: 4px 4px 0 var(--amber-mid); border-color: var(--amber)`.
This is the system's signature interaction — do not change shadow blur or spread.

### `.callout` (was `.final-protocol`)
Callout box with amber accent. **Full border only — no side-stripe.** Use full
`border: 1.5px solid var(--amber-mid); background: var(--amber-lt)` pattern.

```css
.callout {
  margin-top: 36px;
  background: var(--amber-lt);
  border: 1.5px solid var(--amber-mid);
  border-radius: 6px;
  padding: 24px 28px;
  font-size: 16px; line-height: 1.7;
  max-width: 780px;
}
.callout-label {
  font-family: 'DM Mono', monospace; font-size: 10px;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--amber); font-weight: 700;
  margin-bottom: 10px; display: block;
}
```

### `.pull-quote`
Editorial blockquote in essay sections. **Full border — no side-stripe.**

```css
.pull-quote {
  margin: 32px 0; padding: 20px 28px;
  background: var(--amber-lt);
  border: 1.5px solid var(--amber-mid);
  border-radius: 6px;
}
.pull-quote p {
  font-family: 'Lora', serif; font-size: 19px;
  font-style: italic; line-height: 1.6; color: var(--ink);
}
.pull-quote cite {
  display: block; margin-top: 10px;
  font-family: 'DM Mono', monospace; font-size: 11px;
  letter-spacing: 0.1em; color: var(--amber);
  font-style: normal; text-transform: uppercase;
}
```

### `.code-block`
Dark code panel on `--board`. Left amber border accent is permitted here
(code panels are not "cards, list items, callouts, or alerts" — they are
code display surfaces where the border functions as a language gutter).

```css
.code-block {
  background: var(--board); border-radius: 6px;
  overflow: hidden; margin-top: 20px;
  border: 1px solid rgba(255,255,255,0.1);
  border-left: 3px solid var(--amber);
}
```

### `.step-num`
Numbered list badges. Ink background, chalk text, DM Mono, `border-radius: 2px`.

```css
.step-num {
  background: var(--ink); color: var(--chalk);
  font-family: 'DM Mono', monospace; font-size: 10px; font-weight: 500;
  min-width: 22px; height: 22px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 2px; flex-shrink: 0;
}
```

### `.pill` / `.pill-dark`
Label chips. Two variants: light (paper-alt bg, ink text) and dark (ink bg, chalk text).
Both use `border-radius: 2px` (rounded.sm). DM Mono label-sm sizing.

### `.doc-footer`
Closing band. Dark (`--board`) or muted, full-bleed. DM Mono label text.

---

## Themes

All themes share identical `:root` variable **names**. Themes remap values by overriding
`:root` in a `<style>` block at the top of each file's CSS — or by adding a theme class.

### Theme: `light-paper` (default — feyn, triple-stack, signposts)
No overrides needed. Use the canonical token values above exactly.
Nav: `.toc-bar` on dark (`--ink`). Hero: `--board`.

### Theme: `light-sidebar` (21-playground-explainer)
Same surface palette; no hero. Nav replaces `.toc-bar` with a left `.sidebar`.

```css
/* light-sidebar: sidebar bg is paper-alt, no hero */
.page { display: grid; grid-template-columns: 220px minmax(0,1fr); }
.sidebar { background: var(--paper-alt); border-right: 1px solid var(--border); }
```

### Theme: `dark` (workflows-guide)
Remap surface and on-surface tokens to dark values. Accent stays amber.

```css
:root {
  /* dark theme overrides */
  --paper:    #1a1f1c;   /* board becomes the page surface */
  --paper-alt:#1f2521;
  --paper-dark:#232926;
  --ink:       #f0ece2;   /* paper becomes the text color */
  --ink-soft:  #c8c3b3;
  --muted:     #8a8c7a;
  --border:    #2f3630;
  --chalk:     #e8e3d8;
  --board:     #141a16;   /* deeper dark for hero/nav bg */
  /* amber, red, green, blue: unchanged */
}
```

Nav: left `.sidebar` on `--paper-dark`. No `.hero` panel.

---

## Nav Patterns

### Top `toc-bar` (light-paper pages)
Structure: `.hero` → `.toc-bar` → `.wrapper`. The toc-bar is `position: sticky; top: 0`.
Links are horizontal, `overflow-x: auto`, scrollbar hidden. Do not add an additional
back-button outside the hero in this pattern.

### Left sidebar (light-sidebar and dark pages)
Structure: `.page` grid with 220px sidebar column. Sidebar is `position: sticky; top: 0;
height: 100vh; overflow-y: auto`. Active link tracking via `IntersectionObserver` (for
sections) or click-based `.active` class toggle. No `.hero` band in this pattern.

---

## CSS Custom Properties Reference

Every note file must declare this exact `:root` block (token names canonical — values may
be remapped per theme):

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
  --board:     #1a1f1c;
}
```

Dark theme files include the override block immediately after (see Themes section).
**All colour values in CSS use these vars. Never hardcode a hex in a rule.**

---

## Do's and Don'ts

**Do:**
- Use `var(--amber)` for exactly one active/focal element per visual zone.
- Use `box-shadow: 4px 4px 0 var(--amber-mid)` (zero blur) for all card hovers.
- Use `section-label::after` flex rule line — never `<hr>` or `border-bottom` on the section
  container to create structural dividers.
- Keep DM Mono uppercase at all times. `text-transform: uppercase` is non-negotiable.
- Use Lora only for h1 and h2. Italic Lora `em` in headlines → amber. That's the system's
  typographic signature.
- Apply `overflow: hidden; border-radius: 6px` together on any card that has a
  visually-distinct header region (like `.drill-header` or `.scorecard-header`).
- On sidebar-nav pages: use `IntersectionObserver` for active link highlighting. No JS
  `scroll` listener polling.
- Every internal link: `href="{{ '/notes/slug/' | relative_url }}"`. Never bare `/path`.

**Don't:**
- **No side-stripe borders** on callouts, list items, or alert boxes. Use full borders
  (`border: 1.5px solid`) + background tints instead. The only permitted `border-left`
  accent > 1px is on `.code-block` (code gutter, not a callout pattern).
- **No gradient text.** `background-clip: text` with a gradient is banned. Use a solid amber
  for emphasis.
- **No blur shadows.** `box-shadow: 0 4px 12px rgba(0,0,0,0.15)` is out of system. Zero blur.
- **No `opacity` on parent containers with interactive children.** Use `color: var(--muted)`
  to dim text; never `opacity: 0.6` on a parent that contains hover states.
- **No hardcoded hex values in CSS rules.** All values through `:root` vars.
- **No Playfair Display, system-ui, or Inter.** Lora + DM Sans + DM Mono only.
- **No yellow toc-bar.** The toc-bar is always `background: var(--ink)` on light-paper theme.
  Yellow nav was a signposts.html divergence — it is not sanctioned.
- **No amber toc-bar background.** Amber is a text/accent colour, not a surface colour.
- **No `height: 100%` on `.hero`**. It is intrinsic-height (padding-based).
- **No SCSS, no `assets/css/`, no shared stylesheet.** CSS lives inline in each file.
- **No `layout:` other than `blank` for note files.**
