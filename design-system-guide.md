
# components

| #   | Section                   | What it captures                                |
| --- | ------------------------- | ----------------------------------------------- |
| 1   | Visual Theme & Atmosphere | Mood, density, design philosophy                |
| 2   | Color Palette & Roles     | Semantic name + hex + functional role           |
| 3   | Typography Rules          | Font families, full hierarchy table             |
| 4   | Component Stylings        | Buttons, cards, inputs, navigation with states  |
| 5   | Layout Principles         | Spacing scale, grid, whitespace philosophy      |
| 6   | Depth & Elevation         | Shadow system, surface hierarchy                |
| 7   | Do's and Don'ts           | Design guardrails and anti-patterns             |
| 8   | Responsive Behavior       | Breakpoints, touch targets, collapsing strategy |
| 9   | Agent Prompt Guide        | Quick color reference, ready-to-use prompts     |

# What is DESIGN.md?

A design system document that AI agents read to generate consistent UI across your project.


Every project has a visual identity: colors, fonts, spacing, component styles. Traditionally, this lives in a Figma file, a brand PDF, or a designer’s head. None of these are readable by an AI agent.

**`DESIGN.md` changes that.** It’s a plain-text design system document that both humans and agents can read, edit, and enforce. Think of it as the design counterpart to `AGENTS.md`:

|File|Who reads it|What it defines|
|---|---|---|
|`README.md`|Humans|What the project is|
|`AGENTS.md`|Coding agents|How to build the project|
|`DESIGN.md`|Design agents|How the project should look and feel|

## What it gives you

When a design agent like Stitch reads your `DESIGN.md`, every screen it generates follows the same visual rules: your color palette, your typography, your component patterns. Without it, each screen stands alone. With it, they look like they belong together.

`DESIGN.md` is a **living artifact**, not a static config file. It evolves as your design evolves. The agent generates it, you refine it, and it’s re-applied to screens as you iterate.

Under the hood, every `DESIGN.md` has two layers: **YAML front matter** containing machine-readable design tokens (exact hex values, font properties, spacing scales) and a **markdown body** providing human-readable design rationale. Tokens give agents precise values. Prose tells them _why_ those values exist. See [the specification](https://app-companion-430619.appspot.com/docs/design-md/specification/) for the full format.

## The philosophy

The DESIGN.md spec is a **foundation, not a prescription**. It provides a common ground that agents, tools, and teams can rely on — a shared vocabulary for colors, typography, layout, and components — while preserving the freedom to extend the format for domain-specific needs. Unknown sections and custom tokens are accepted, not rejected.

## How they’re created

There are three paths to a `DESIGN.md`, from effortless to precise.

![Creating a design system from a prompt in Stitch](https://app-companion-430619.appspot.com/docs/design-systems-create.png)

### Let the agent generate it

Describe the vibe. The agent translates your aesthetic intent into tokens and guidelines.

PROMPT

A playful coffee shop ordering app with warm colors, rounded corners, and a friendly feel

Stitch generates a complete design system (colors, typography, spacing, component styles) and summarizes it as a `DESIGN.md`.

### Derive from branding

If you already have a brand, provide a URL or image. The agent extracts your palette, typography, and style patterns to build the `DESIGN.md` from what already exists.

![Importing a design system from a website URL in Stitch](https://app-companion-430619.appspot.com/docs/design-system-import-from-website.png)

### Write it by hand

Advanced users can author a `DESIGN.md` directly, encoding exact design preferences. Every section is just markdown with optional YAML front matter for design tokens. No special syntax beyond standard markdown and YAML.

## Example

Below is a minimal `DESIGN.md` for a dark-themed productivity app. The YAML front matter defines the exact token values; the markdown body explains the design intent.

```
---name: DevFocus Darkcolors:  primary: "#2665fd"  secondary: "#475569"  surface: "#0b1326"  on-surface: "#dae2fd"  error: "#ffb4ab"typography:  body-md:    fontFamily: Inter    fontSize: 16px    fontWeight: 400rounded:  md: 8px---
# Design System
## OverviewA focused, minimal dark interface for a developer productivity tool.Clean lines, low visual noise, high information density.
## Colors- **Primary** (#2665fd): CTAs, active states, key interactive elements- **Secondary** (#475569): Supporting UI, chips, secondary actions- **Surface** (#0b1326): Page backgrounds- **On-surface** (#dae2fd): Primary text on dark backgrounds- **Error** (#ffb4ab): Validation errors, destructive actions
## Typography- **Headlines**: Inter, semi-bold- **Body**: Inter, regular, 14–16px- **Labels**: Inter, medium, 12px, uppercase for section headers
## Components- **Buttons**: Rounded (8px), primary uses brand blue fill- **Inputs**: 1px border, subtle surface-variant background- **Cards**: No elevation, relies on border and background contrast
## Do's and Don'ts- Do use the primary color sparingly, only for the most important action- Don't mix rounded and sharp corners in the same view- Do maintain 4:1 contrast ratio for all text
```

This is what the agent reads when generating your next screen. For the complete format specification, see [The specification](https://app-companion-430619.appspot.com/docs/design-md/specification/). To validate your DESIGN.md against the spec, see [Validate with the CLI](https://app-companion-430619.appspot.com/docs/design-md/cli/).

# The DESIGN.md specification

The formal specification for the DESIGN.md format — token schema, section structure, and type system.

A DESIGN.md file has two layers. The **YAML front matter** contains machine-readable design tokens — the precise values agents use to enforce consistency. The **markdown body** provides human-readable design rationale organized into `##` sections. Prose may use descriptive color names (e.g., “Midnight Forest Green”) that correspond to systematic token names (e.g., `primary`). The tokens are the normative values; the prose provides context for how to apply them.

The spec is a **foundation, not a prescription**. It provides common ground that agents, tools, and teams can rely on, while preserving the freedom to extend the format for domain-specific needs.

## Design tokens

DESIGN.md embeds design tokens as YAML front matter at the beginning of the file. The front matter block must begin with a line containing exactly `---` and end with a line containing exactly `---`. The YAML content between these delimiters follows the schema defined below.

The token system is inspired by the [W3C Design Token Format](https://www.designtokens.org/). Tokens are easily converted to and from `tokens.json`, Figma variables, and Tailwind theme configs.

```
---version: alphaname: Daylight Prestigecolors:  primary: "#1A1C1E"  secondary: "#6C7278"  tertiary: "#B8422E"typography:  h1:    fontFamily: Public Sans    fontSize: 48px    fontWeight: 600    lineHeight: 1.1    letterSpacing: -0.02emrounded:  sm: 4px  md: 8pxspacing:  sm: 8px  md: 16pxcomponents:  button-primary:    backgroundColor: "{colors.primary-60}"    textColor: "{colors.primary-20}"    rounded: "{rounded.md}"    padding: 12px---
```

### Schema

```
version: <string>          # optional, current version: "alpha"name: <string>description: <string>      # optionalcolors:  <token-name>: <Color>typography:  <token-name>: <Typography>rounded:  <scale-level>: <Dimension>spacing:  <scale-level>: <Dimension | number>components:  <component-name>:    <token-name>: <string | token reference>
```

The `<scale-level>` placeholder represents a named level in a sizing or spacing scale. Common level names include `xs`, `sm`, `md`, `lg`, `xl`, and `full`. Any descriptive string key is valid.

## Token types

|Type|Format|Example|
|---|---|---|
|**Color**|`#` + hex code (sRGB)|`"#1A1C1E"`|
|**Dimension**|number + unit (`px`, `em`, `rem`)|`48px`, `-0.02em`|
|**Token Reference**|`{path.to.token}`|`{colors.primary}`|
|**Typography**|composite object|See properties below|

### Typography properties

|Property|Type|Description|
|---|---|---|
|`fontFamily`|string|The font family name|
|`fontSize`|Dimension|The font size|
|`fontWeight`|number|Numeric weight (e.g., `400`, `700`). In YAML, bare numbers and quoted strings are equivalent|
|`lineHeight`|Dimension \| number|A dimension (e.g., `24px`) or a unitless multiplier (e.g., `1.6`). Unitless is recommended|
|`letterSpacing`|Dimension|Letter spacing adjustment|
|`fontFeature`|string|Configures [`font-feature-settings`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-feature-settings)|
|`fontVariation`|string|Configures [`font-variation-settings`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variation-settings)|

### Token references

A token reference is wrapped in curly braces and contains an object path to another value in the YAML tree. For most token groups, the reference must point to a primitive value (e.g., `{colors.primary-60}`), not a group. Within the `components` section, references to composite values (e.g., `{typography.label-md}`) are permitted.

```
components:  button-primary:    backgroundColor: "{colors.primary-60}"    textColor: "{colors.primary-20}"    rounded: "{rounded.md}"
```

## Sections

Every DESIGN.md follows the same structure. Sections can be omitted if they are not relevant to the project, but those present should appear in the sequence listed below. All sections use `##` headings. An optional `#` heading may appear for document titling purposes but is not parsed as a section.

The section structure is intentionally open-ended. The canonical sections provide a shared vocabulary; design systems are free to add domain-specific sections beyond these.

### Section order

|#|Section|Aliases|
|---|---|---|
|1|Overview|Brand & Style|
|2|Colors||
|3|Typography||
|4|Layout|Layout & Spacing|
|5|Elevation & Depth|Elevation|
|6|Shapes||
|7|Components||
|8|Do’s and Don’ts||

### Overview

Also known as “Brand & Style.” A holistic description of the product’s look and feel. This section defines the brand personality, target audience, and the emotional response the UI should evoke. It serves as foundational context when a specific rule or token is not defined.

```
## OverviewA calm, professional interface for a healthcare scheduling platform.Accessibility-first design with high contrast and generous touch targets.
```

### Colors

Defines the color palettes for the design system. At least the `primary` palette should be defined. Additional palettes may be named freely; a common convention is `primary`, `secondary`, `tertiary`, and `neutral`.

```
## Colors
The palette is rooted in high-contrast neutrals and a single accent color.
- **Primary (#1A1C1E):** Deep ink for headlines and core text.- **Secondary (#6C7278):** Sophisticated slate for borders, captions, metadata.- **Tertiary (#B8422E):** The sole driver for interaction.- **Neutral (#F7F5F2):** Warm limestone foundation.
```

**Design tokens:** A `map<string, Color>` mapping the token name to its hex value.

```
colors:  primary: "#1A1C1E"  secondary: "#6C7278"  tertiary: "#B8422E"  neutral: "#F7F5F2"
```

### Typography

Defines typography levels. Most design systems have 9–15 levels, each with a semantic role (headline, body, label) and size variant (small, medium, large).

```
## Typography
- **Headlines:** Public Sans Semi-Bold for an institutional voice.- **Body:** Public Sans Regular at 16px for long-form readability.- **Labels:** Space Grotesk for technical data and metadata.
```

**Design tokens:** A `map<string, Typography>` mapping the token name to its typography properties.

```
typography:  h1:    fontFamily: Public Sans    fontSize: 48px    fontWeight: 600    lineHeight: 1.1    letterSpacing: -0.02em  body-md:    fontFamily: Public Sans    fontSize: 16px    fontWeight: 400    lineHeight: 1.6  label-caps:    fontFamily: Space Grotesk    fontSize: 12px    fontWeight: 500    lineHeight: 1    letterSpacing: 0.1em
```

### Layout

Also known as “Layout & Spacing.” Describes the layout and spacing strategy — grid models, spacing scales, and containment principles.

```
## Layout
The layout follows a Fluid Grid model for mobile and a Fixed-Max-WidthGrid for desktop (max 1200px). A strict 8px spacing scale is used.
```

**Design tokens:** A `map<string, Dimension | number>` mapping the spacing scale identifier to a dimension or unitless number (e.g., column counts or ratios).

```
spacing:  base: 16px  xs: 4px  sm: 8px  md: 16px  lg: 32px  xl: 64px  gutter: 24px  margin: 32px
```

### Elevation & Depth

Also known as “Elevation.” Describes how visual hierarchy is conveyed. For designs that use shadows, it defines the shadow properties. For flat designs, it explains the alternative methods (borders, tonal layers, color contrast).

```
## Elevation & Depth
Depth is achieved through tonal layers rather than heavy shadows.Background uses a soft off-white; primary content sits on pure white cards.
```

### Shapes

Describes how visual elements are shaped — corner radii, edge treatments, and the overall shape language.

```
## Shapes
All interactive elements use a minimal 4px corner radius.Modern enough to feel current, rigid enough to feel engineered.
```

**Design tokens:** A `map<string, Dimension>` mapping the scale level to the corner radius.

```
rounded:  sm: 4px  md: 8px  lg: 12px  full: 9999px
```

### Components

Style guidance for component atoms. The spec defines common component types — Buttons, Chips, Lists, Inputs, Checkboxes, Radio buttons, Tooltips — but design systems are encouraged to define additional components relevant to their domain.

```
## Components- **Buttons**: Rounded (8px), primary uses brand blue fill, secondary uses outline- **Inputs**: 1px border, surface-variant background, 12px padding- **Cards**: No elevation, 1px outline border, 12px corner radius
```

**Design tokens:** A `map<string, map<string, string>>` mapping a component identifier to a group of sub-token properties. Token values may be literal values or references to previously defined tokens.

**Variants.** A component may have variants for different UI states (hover, active, pressed). Variants are defined as separate component entries with a related key name.

```
components:  button-primary:    backgroundColor: "{colors.primary-60}"    textColor: "{colors.primary-20}"    rounded: "{rounded.md}"    padding: 12px  button-primary-hover:    backgroundColor: "{colors.primary-70}"
```

#### Component property tokens

|Property|Type|
|---|---|
|`backgroundColor`|Color|
|`textColor`|Color|
|`typography`|Typography|
|`rounded`|Dimension|
|`padding`|Dimension|
|`size`|Dimension|
|`height`|Dimension|
|`width`|Dimension|

### Do’s and Don’ts

Practical guidelines and common pitfalls. These act as guardrails during generation.

```
## Do's and Don'ts
- Do use the primary color only for the single most important action per screen- Don't mix rounded and sharp corners in the same view- Do maintain WCAG AA contrast ratios (4.5:1 for normal text)- Don't use more than two font weights on a single screen
```

## Consumer behavior for unknown content

The spec is designed to be extended. When a consumer encounters content not defined by this specification:

|Scenario|Behavior|Example|
|---|---|---|
|Unknown section heading|Preserve; do not error|`## Iconography`|
|Unknown color token name|Accept if value is valid|`surface-container-high: '#ede7dd'`|
|Unknown typography token name|Accept as valid typography|`telemetry-data`|
|Unknown spacing value|Accept; store as string if not a valid dimension|`grid-columns: '5'`|
|Unknown component property|Accept with warning|`borderColor`|
|Duplicate section heading|Error; reject the file|Two `## Colors` headings|

## Recommended token names

The following names are commonly used across design systems. They are not required but are provided as guidance for consistency.

**Colors:** `primary`, `secondary`, `tertiary`, `neutral`, `surface`, `on-surface`, `error`

**Typography:** `headline-display`, `headline-lg`, `headline-md`, `body-lg`, `body-md`, `body-sm`, `label-lg`, `label-md`, `label-sm`

**Rounded:** `none`, `sm`, `md`, `lg`, `xl`, `full`