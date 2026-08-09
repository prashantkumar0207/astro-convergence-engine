# Parashari school layer

Purpose: Full (purna) graha drishti facts: aspected signs, whole-sign houses, and aspected grahas.

Specification: `docs/PARASHARI_DRISHTI_SPEC.md`. Decision entry: `docs/DECISION_LOG.md` ADR-0012 (PROPOSED pending
owner ratification, Q1). Certification artifact: see `certification/` and the human-readable
report in `reports/certification/`.

Design notes: First school layer above the shared primitives, isolated per the school-separation rule; requires a parashari_lahiri snapshot and rejects others. Node-cast aspects are excluded from certified behaviour because traditions disagree, and the variant is recorded rather than chosen.

Explicit non-claims: sputa drishti, node-cast aspects, Jaimini rashi drishti, Western aspects, yogas, strengths, interpretation. Each would require its own specification, decision entry and
certification before being built.
