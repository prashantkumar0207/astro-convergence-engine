<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-25 |
| Review cadence | TBD |

# DP-025. Polar-Placidus certification gap and M-04 provenance mislabeling: Tier-0/FOUNDATION-tier
maintenance decision-readiness

## 0. Authorization and scope

Authorized by "CEO direction — proceed with DP-023 resolution," item 3: "Keep polar-Placidus/M-04
completely separate as Tier-0 maintenance; prepare its own decision-readiness only." This paper
consolidates evidence already gathered in `docs/decisions/DP-021-jataka-first-capability-decision-
readiness.md` sections D and N.1, organized as its own standalone decision-readiness paper per explicit
instruction, rather than folded into any JATAKA-capability paper. It does not implement anything and does
not modify `engine/astronomy/house_positions.py`, `engine/parashari/drishti.py`, or any certified
artifact.

**Explicit architectural framing, per instruction:** this is Tier-0/FOUNDATION-tier certification-
completion work, not a JATAKA capability. The polar-Placidus gap lives inside `current_engine_
certification.json`, the already-locked Tier-0 kernel artifact (`ADR-0005`/`ADR-0034`), not a
`Q8_CLOSURE_MATRIX.md` s5 JATAKA-scope artifact. It is kept out of `DP-023`'s own candidate scoring for
exactly this reason.

## A. The two items, restated precisely

**A1. Polar-Placidus certification gap.** `certification/ENGINE_CAPABILITY_INVENTORY.json`: Placidus
house cusps are `"PARTIALLY_CERTIFIED"`, "exercised to 64.1N only; polar behaviour NOT VERIFIED and
undefined." Consistently documented across `README.md`, `docs/ENGINE_STATUS.md`, `docs/PROJECT_
ROADMAP.md`, `ARCHITECTURE_STATUS.md`, `CURRENT_ENGINE_CERTIFICATION_STATUS.md`, `docs/DECISION_LOG.md`'s
own Tier-0 lock scope note.

**A2. M-04 (`DrishtiChart` provenance mislabeling).** Re-confirmed live this session (`DP-021` section
N.1): `engine/parashari/drishti.py::graha_drishti_from_snapshot()` computes `aspected_houses` via pure
whole-sign counting (`((sign - ascendant_sign) % 12) + 1`, line 84, no Placidus reference), while reusing
`snapshot.provenance` unmodified (line 63); the certified `PARASHARI_LAHIRI` profile hardcodes
`house_system=b"P"`. The resulting `DrishtiChart.provenance.house_system` field reads `"P"` on every
certified Parashari drishti chart despite carrying whole-sign houses.

## B. Why these two are grouped, and why they are architecturally separate from any JATAKA capability

Both concern the *labelling and domain-completeness* of the already-certified Tier-0 house-cusp/drishti
machinery, not new analytical capability. Neither adds a new production analytical input in the sense
`Q8_CLOSURE_MATRIX.md` s5's own exit criteria use the term. A2 is a pure labelling defect (the computed
whole-sign houses are correct; only the provenance field describing them is wrong). A1 is a domain-
completeness gap in an already-certified Tier-0 artifact. Grouping them reflects that both are cheap,
narrow, and share a `RISE_SET_V1`-style precedent for how to close this class of gap - not that they are
the same defect.

## C. Evidence and precedent

**RISE_SET_V1's own directly-applicable precedent** (`ADR-0054`): a structured `RiseSetStatus` enum
(`OK`/`NO_RISE`/`NO_SET`), never an exception, never a silently-wrong value;
`certification/RISE_SET_V1_certification.json` records `"circumpolar_cases_checked": 2`. No equivalent
structured status exists yet for undefined house cusps - `house_positions()` today has no polar guard at
all and passes through whatever Swiss Ephemeris itself does.

**What is NOT yet known, disclosed honestly:** the exact mathematical latitude threshold at which
Placidus becomes undefined is not derived or cited anywhere in this repository - "64.1N" is the edge of
the certified holdout's own highest-latitude case (`H5_reykjavik_1992`), not a proven theoretical
boundary; the true astrological/astronomical polar circle (~66.5633°N/S) is the commonly-cited threshold,
leaving the 64.1°-to-66.5° band and the true polar zone both unverified. `scripts/profile.py`/
`regression_report.json` assert, without in-repo verification, that Swiss Ephemeris falls back to
Porphyry above the polar circle - untested against `swetest` in this repository.

**Oracle availability:** PyJHora has never been used as a house-cusp/bhava oracle anywhere in this
repository (confirmed by exhaustive search of every `scripts/certify_*.py` PyJHora import site, `DP-021`
section D.12) - only for panchanga, dasha, varga charts, and aspects. The bundled `swetest` 2.10.03
binary, already the Tier-0 oracle for non-polar Placidus (verified to ~0.0002 arcsec), is the natural
first oracle to test against at high latitude, since its own polar behaviour can be observed directly.

## D. Options

**For A1 (polar-Placidus):**
- Option 1: extend the existing Tier-0 kernel certification's own holdout matrix with polar/near-polar
  cases (64.1°-66.5°N/S and beyond), define a structured refusal/undefined-status return
  (mirroring `RiseSetStatus`) for the domain Swiss Ephemeris itself cannot resolve meaningfully.
- Option 2: a small, dedicated `HOUSES_POLAR_V1`-style artifact, separate from the Tier-0 kernel
  artifact, recording exactly what was tested and what remains genuinely unverifiable - matching this
  project's own one-artifact-per-capability convention.
- Option 3: defer indefinitely, since no current certified consumer reaches the polar domain in practice
  (KP significators, the only named prerequisite consumer, is itself not methodology-ready per `DP-026`).

**For A2 (M-04):**
- Option 1: add a `houses_convention: str` (or similarly named) field to `DrishtiChart`'s own provenance
  usage, explicitly recording "whole-sign" rather than inheriting the snapshot's own Placidus-labelled
  `house_system` field unmodified - additive, mirrors `ADR-0065`'s `declared_division`/`ADR-0071`'s
  `seed_boundary_convention` precedent of a small, explicit disclosure field.
- Option 2: leave `DrishtiChart` consuming a separate, purpose-built provenance object rather than the
  snapshot's own shared one - larger change, more invasive.
- Option 3: fix via documentation/non-claim only (state clearly in `PARASHARI_DRISHTI_V1`'s own
  certification artifact that `provenance.house_system` does not describe `aspected_houses`) - cheapest,
  but leaves the field itself still capable of misleading a future consumer who reads it out of context.

## E. Recommendation and confidence

**At medium-high confidence:** A2 Option 1 (an additive disclosure field, mirroring the already-twice-used
`declared_division`/`seed_boundary_convention` pattern) - cheap, precedented, closes a genuine mislabeling
with zero certified-value impact. **At medium confidence:** A1 Option 1 or 2 (extend the holdout, define a
structured undefined-status return) - narrow, `RISE_SET_V1`-precedented, but genuinely needs new empirical
work (testing `swetest`'s own polar behaviour, which has never been done here) before a specific option can
be chosen with full confidence.

## F. Certification plan (if authorized)

For A1: extend `current_engine_certification.json`'s own holdout with cases bracketing 64.1°N/S, the true
polar circle (~66.5633°N/S), and at least one case strictly inside the Arctic/Antarctic circle; an
independent Placidus re-derivation at high latitude; a genuine negative control. For A2: a pinning test
confirming the new disclosure field's value on every certified Parashari drishti chart; a negative control
proving the field is not vacuous.

## G. Explicit non-claims

This paper does not implement A1 or A2. It does not modify `house_positions.py`, `engine/parashari/
drishti.py`, or any certified artifact. It does not derive the exact mathematical polar-failure threshold.
It does not choose an option for either item. It does not claim this work is a JATAKA capability - it is
explicitly scoped as Tier-0/FOUNDATION-tier maintenance, per instruction.

## H. Exact CEO decision required

1. Authorize A1 and/or A2 as Tier-0/FOUNDATION-tier maintenance now, or defer either/both.
2. If authorized: select an option for each (sections D, E).
3. Confirm whether this work needs its own JATAKA-adjacent ADR label at all, or proceeds under ordinary
   Tier-0 maintenance discipline (no JATAKA phase-entry ceremony implied either way).

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-25 | Created, consolidating `DP-021` sections D/N.1 into a standalone Tier-0/FOUNDATION-tier maintenance decision-readiness paper, kept explicitly separate from any JATAKA-capability decision per instruction. Presents options for both the polar-Placidus certification gap and the M-04 provenance mislabeling, a certification plan, and three exact owner decisions required. Decides nothing; no code touched; no capability implementation authorized. |
