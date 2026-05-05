# Hook-Body-Payoff Framework

**Cohesion:** 0.36 · **Nodes:** 8

## Nodes

- **Body** `image` — `assets/img/signposting-example-arrowgraphic.png`
- **Hook** `image` — `assets/img/signposting-example-arrowgraphic.png`
- **Open Loop (For Body)** `image` — `assets/img/signposting-example-arrowgraphic.png`
- **Open Loops** `image` — `assets/img/signposting-example-arrowgraphic.png`
- **Outro + CTA** `image` — `assets/img/signposting-example-arrowgraphic.png`
- **Payoff #1 Open Loop** `image` — `assets/img/signposting-example-arrowgraphic.png`
- **Payoff Unit (Why / What / How)** `image` — `assets/img/signposting-example-arrowgraphic.png`
- **Why-What-How Framework** `image` — `assets/img/signposting-example-arrowgraphic.png`

## Internal Edges

- **Why-What-How Framework** → `has_section` → **Hook** [INFERRED 0.75]
- **Why-What-How Framework** → `has_section` → **Body** [INFERRED 0.75]
- **Why-What-How Framework** → `has_section` → **Outro + CTA** [INFERRED 0.75]
- **Hook** → `contains` → **Open Loop (For Body)** [INFERRED 0.75]
- **Hook** → `uses_mechanism` → **Open Loops** [INFERRED 0.75]
- **Open Loop (For Body)** → `transitions_to` → **Body** [INFERRED 0.75]
- **Open Loops** → `is_instance_of` → **Payoff #1 Open Loop** [INFERRED 0.75]
- **Body** → `contains_repeating_unit` → **Payoff Unit (Why / What / How)** [INFERRED 0.75]
- **Body** → `contains` → **Payoff #1 Open Loop** [INFERRED 0.75]
- **Body** → `leads_to` → **Outro + CTA** [INFERRED 0.75]

## Cross-Community Connections

_No cross-community edges_

---
_[← Back to index](index.md)_