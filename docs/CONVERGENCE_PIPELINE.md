# Astro Convergence Pipeline

## Objective

Transform deterministic astronomical calculations into explainable astrological predictions using independent rule engines and evidence aggregation.

---

# Layer 1 — Astronomy

Produces:

- Planet Positions
- Houses
- Ayanamsa
- Sidereal Positions
- Aspects

Output:

AstronomySnapshot

---

# Layer 2 — Knowledge

Provides canonical astrology data.

Examples:

- Planets
- Signs
- Houses
- Dignities
- Relationships
- Nakshatras

---

# Layer 3 — Calculation

Pure calculations only.

Examples:

- Planet Strength
- House Strength
- Dignities
- Relationships
- Ownership
- Dispositors
- Yogas
- Vargas
- Dasha

No predictions are made here.

---

# Layer 4 — Rule Engines

Independent implementations.

Modules:

- Parashari
- KP
- Jaimini
- Nadi
- BNN
- Tajik

Each produces evidence only.

---

# Layer 5 — Evidence Engine

Collects evidence from all rule engines.

Example:

Marriage Delay

Evidence

- Saturn influences 7th
- Weak Venus
- KP confirms
- Nadi confirms

No conclusions yet.

---

# Layer 6 — Reasoning Engine

Combines evidence.

Produces:

- Confidence
- Supporting Factors
- Conflicting Factors
- Missing Evidence

---

# Layer 7 — Prediction Engine

Produces structured predictions.

Examples:

- Marriage
- Career
- Health
- Wealth
- Children

---

# Layer 8 — Explanation Engine

Explains every prediction.

Output includes:

- Why
- Which rules fired
- Which systems agreed
- Confidence

---

# Guiding Principles

1. Astronomy never predicts.
2. Knowledge never calculates.
3. Calculations never interpret.
4. Rule engines never overwrite each other.
5. Evidence is immutable.
6. Every prediction must be explainable.
7. Every confidence score must be reproducible.