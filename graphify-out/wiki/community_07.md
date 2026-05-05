# Inspiration Curation System

**Cohesion:** 0.23 · **Nodes:** 12

## Nodes

- **Inspo Categories Data File** `document` — `_data/inspo_categories.yml`
- **Inspo Deep Dives Card Template Include** `code` — `_includes/inspo/deep-dives.html`
- **Inspo Music Card Template Include** `code` — `_includes/inspo/mu.html`
- **Inspo Tools Card Template Include** `code` — `_includes/inspo/tools.html`
- **Inspo Tweet Card Template Include** `code` — `_includes/inspo/tweet.html`
- **Inspo Category: Deep Dives** `document` — `_data/inspo_categories.yml`
- **Inspo Category: Music** `document` — `_data/inspo_categories.yml`
- **Inspo Category: Tools** `document` — `_data/inspo_categories.yml`
- **Inspo Category: Tweets** `document` — `_data/inspo_categories.yml`
- **Inspo Category: Websites** `document` — `_data/inspo_categories.yml`
- **Inspo Category: Writing** `document` — `_data/inspo_categories.yml`
- **Inspo Category: YouTube** `document` — `_data/inspo_categories.yml`

## Internal Edges

- **Inspo Categories Data File** → `references` → **Inspo Music Card Template Include** [EXTRACTED 1.0]
- **Inspo Categories Data File** → `references` → **Inspo Tweet Card Template Include** [EXTRACTED 1.0]
- **Inspo Categories Data File** → `references` → **Inspo Tools Card Template Include** [EXTRACTED 1.0]
- **Inspo Categories Data File** → `references` → **Inspo Deep Dives Card Template Include** [EXTRACTED 1.0]
- **Inspo Categories Data File** → `references` → **Inspo Category: YouTube** [EXTRACTED 1.0]
- **Inspo Categories Data File** → `references` → **Inspo Category: Music** [EXTRACTED 1.0]
- **Inspo Categories Data File** → `references` → **Inspo Category: Tweets** [EXTRACTED 1.0]
- **Inspo Categories Data File** → `references` → **Inspo Category: Tools** [EXTRACTED 1.0]
- **Inspo Categories Data File** → `references` → **Inspo Category: Writing** [EXTRACTED 1.0]
- **Inspo Categories Data File** → `references` → **Inspo Category: Websites** [EXTRACTED 1.0]
- **Inspo Categories Data File** → `references` → **Inspo Category: Deep Dives** [EXTRACTED 1.0]
- **Inspo Category: Music** → `references` → **Inspo Music Card Template Include** [EXTRACTED 1.0]
- **Inspo Category: Tweets** → `references` → **Inspo Tweet Card Template Include** [EXTRACTED 1.0]
- **Inspo Category: Tools** → `references` → **Inspo Tools Card Template Include** [EXTRACTED 1.0]
- **Inspo Category: Deep Dives** → `references` → **Inspo Deep Dives Card Template Include** [EXTRACTED 1.0]

## Cross-Community Connections

- **Inspo Categories Data File** → `shares_data_with` → **Jekyll Static Site (Saptak's Website)** (in *Site Navigation & Tag System*)
- **Tags Sidebar Include (filterable tag navigation)** (from *Site Navigation & Tag System*) → `references` → **Inspo Deep Dives Card Template Include**

---
_[← Back to index](index.md)_