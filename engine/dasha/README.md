# Dasha layer

Purpose: Vimshottari maha, antar and pratyantar timelines in exact rational arithmetic.

Specification: `docs/VIMSHOTTARI_DASHA_SPEC.md`. Decision entry: `docs/DECISION_LOG.md` ADR-0007 (PROPOSED pending
owner ratification, Q1). Certification artifact: see `certification/` and the human-readable
report in `reports/certification/`.

Design notes: Year length is an EXPLICIT DashaProfile field with no hidden default; seeding is school-explicit and recorded in provenance; the Vimshottari tables are a deliberate separate copy from engine/kp so the layers stay isolated, with equality enforced by test rather than by cross-import (see ADR-0013 conflict 2).

Explicit non-claims: other dasha systems, depths beyond pratyantardasha, other year conventions. Each would require its own specification, decision entry and
certification before being built.
