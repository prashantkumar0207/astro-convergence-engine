<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | IMPLEMENTED AND CERTIFIED - decision entry ADR-0006 PROPOSED pending owner ratification (Q1) |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-09 |
| Review cadence | TBD (see docs/OPEN_QUESTIONS.md Q1) |

# KP lordship chain layer specification

> **Provenance and normative status.** This specification was authored as a plan,
> approved by the owner conversationally, and implemented before being lifted into
> `docs/`. `docs/PROJECT_CONSTITUTION.md` s7 states that anything not in the repository
> is input material and not truth, so the out-of-repository original carried no
> authority; this file is the resident specification. The governing decision is recorded
> in `docs/DECISION_LOG.md` at ADR-0006, whose status is PROPOSED pending owner
> ratification (Q1). The text below is DESCRIPTIVE of the certified implementation and
> of the decisions actually taken; the ADR is the normative record. Sections retain the
> numbering of the original plan, including its implementation and publication records,
> which are preserved as dated evidence.

Date: 2026-08-09
Status: PROPOSED. Implementation starts only after explicit approval.
Base: origin/main 45ea7bf (audited, certified, published).

## 1. Objective

Migrate the KP (Krishnamurti Paddhati) lordship-chain capability from the certified legacy kernel (legacy/kp.py, legacy/engine.py) into an isolated, production-grade engine/kp/ package running on the current engine's certified astronomy under the ratified KP_KRISHNAMURTI profile, with the legacy implementation as the equivalence oracle. Scope name: KP_CHAIN_V1.

## 2. What the legacy reference actually provides (CODE-INSPECTED)

legacy/kp.py computes, for any longitude, the exact-rational KP hierarchy: sign lord (SL), nakshatra lord (NL), sub lord (SB), sub-sub lord (SS), using the Vimshottari lord order Ke Ve Su Mo Ma Ra Ju Sa Me with years 7 20 6 10 7 18 16 19 17, nakshatra span exactly 40/3 degrees, interval ownership exact rational [start, end), and float inputs converted through Decimal(str(x)) to preserve the decimal spelling of ephemeris output rather than the raw IEEE-754 expansion. Its own tests prove interval completeness (sub widths sum exactly to the nakshatra span, recursively), start-inclusive boundary ownership at all 2,187+ generated boundaries, classical anchors, and determinism. legacy/engine.py applies that chain to all bodies and Placidus cusps under KRISHNAMURTI ayanamsa with mean node. Certification evidence: LOCK_MANIFEST.json (zero SL/NL/SB/SS mismatches on the legacy holdout) and v1_1_engineering_decision.json (200/200 exact fields on the 50-item transcribed KP fixture).

## 3. Proposed architecture (additive only, no certified file modified)

New package engine/kp/, isolated per the school-separation rule:

engine/kp/tables.py: frozen data tables (lord order, Vimshottari years, KP sign lords) with classical citations. Constructor-style validation at import: years sum to 120, table lengths exact.
engine/kp/intervals.py: the exact-rational interval walk and boundary generator, migrated with identical mathematics from legacy/kp.py, including the Decimal(str(x)) float conversion rule, documented as the KP layer's numeric contract.
engine/kp/chain.py: kp_chain(longitude) returning a typed KpChain model (sign, SL, nakshatra index and name, NL, SB, SS, nearest_boundary_arcsec).
engine/kp/chart.py: kp_chart(birth_data) which requests an AstronomySnapshot EXPLICITLY under KP_KRISHNAMURTI (never the default profile, per the lock's methodology-isolation rule), asserts node_policy is mean, attaches the chain to every planet, cusp, and the ascendant, and carries the snapshot Provenance through to the output.
engine/models/kp_chain.py and engine/models/kp_chart.py: typed models. KP output uses KP terminology only; nothing is written into Parashari models.

Nothing registers into the Generic Varga registry (KP chains are not vargas). The dispatcher, D1/D9/D10, and all Tier-0 modules are untouched.

## 4. Convention decisions that need your explicit sign-off

Decision KP-A, boundary policy: the engine-wide float convention promotes values within 1e-10 degrees below a division boundary up to it. The legacy KP layer instead classifies the exact rational value with [start, end) ownership and no promotion. These agree everywhere except floats lying within 1e-10 below an exact KP boundary. I recommend preserving the legacy exact-rational behavior verbatim in engine/kp/ (Option A), because it is the certified reference behavior, D-003 requires zero categorical mismatch against it, and KP's exact arithmetic is mathematically self-sufficient without a float tolerance. The difference from the engine float convention will be documented in the module header and in the certification artifact as an explicit, deliberate, school-specific policy (not a hidden second convention), and every chain output carries nearest_boundary_arcsec so downstream consumers can flag boundary-critical results. The alternative (Option B, apply 1e-10 promotion before conversion) breaks exact legacy equivalence and reopens the certified baseline; I advise against it.

Decision KP-B, node policy: KP charts always use the mean node (matches legacy certification and the profile identification evidence in regression_report.json). kp_chart will assert this and raise if handed a true-node profile.

Decision KP-C, open item O-1: commit the executable bit on swetest once (mode-only change, content hash f53943bb... unchanged), so certification runs stop dirtying the tree. This is a one-line, zero-byte-content change to a locked artifact's file mode; I will document it in the commit message and verify the hash before and after.

## 5. Equivalence and certification strategy (the gates)

Gate 1, pure-math equivalence (unit level): engine/kp/ chain versus legacy/kp.py chain, exact tuple equality of (SL, NL, SB, SS) over a 51,429-point dense sweep, plus every boundary from legacy all_boundaries() tested at, just above, and just below with the same exact-rational epsilon the legacy tests use, plus float ULP neighbors of every boundary. Zero mismatch tolerance (D-003).

Gate 2, invariant reproduction: port the legacy invariant tests (interval completeness, recursive width sums, start-inclusive ownership, classical anchors, determinism) into engine/tests/test_kp_intervals.py so the default gate owns them forever.

Gate 3, chart-level equivalence (astronomy included): the frozen 11-case holdout matrix run through engine/kp/chart.py under KP_KRISHNAMURTI, compared against legacy engine.compute() under the identical profile (KRISHNAMURTI, mean node, Placidus, strict SWIEPH, same bundled ephemeris). Longitudes must agree within the already-certified sub-milliarcsecond bound; every SL/NL/SB/SS assignment for every body and cusp must match exactly. Zero categorical tolerance.

Gate 4, fixture regression: the transcribed KP fixture set used in v1_1_engineering_decision.json (200/200 exact) recomputed through the new path via brihat_fixtures.py longitudes as pure-math structural checks.

Gate 5, independent holdout validator: a new root-level validate_kp_holdout.py, same pattern as the D9/D10 validators, importing NOTHING from engine/kp/ for its reference values (independent re-derivation of the chain from the classical rule inside the validator).

Gate 6, certification artifact: certification/KP_CHAIN_V1_certification.json regenerated from scratch by a runner script, plus a status section added to the certification docs additively. Full default gate, both existing holdout validators, legacy gate, and the Tier-0 certifier must still pass untouched (proving no regression outside KP).

Explicit non-claims of KP_CHAIN_V1: no significators (that is Tier-1 KP_SIGNIFICATOR_V1 and per DECISION_LOG D-008 its methodology spec must be frozen first), no four-step, no ruling planets, no horary, no dasha. These will raise or simply not exist.

## 6. Implementation order (each step commits only after its battery passes)

Step 1: O-1 mode-only commit (Decision KP-C). Step 2: tables.py + intervals.py + chain.py + models with Gates 1 and 2 green. Step 3: chart.py with Gates 3 and 4 green. Step 4: validator and certification runner, Gates 5 and 6 green, docs updated additively. Step 5: publication (bundle relay to you, or direct push if you have provided a PAT by then), followed by my fresh-clone post-publication verification, same discipline as the cleanup phase.

## 7. Risks and mitigations

The Decimal(str(x)) conversion is semantically load-bearing at boundaries; it will be ported verbatim, unit-tested against adversarial spellings, and cross-checked by Gate 1. Lord and sign tables could drift from engine Parashari tables; a consistency test asserts KP sign lords agree with engine/astrology/sign_lord.py names while remaining separate data (isolation preserved, agreement verified). The engine float nakshatra index and the KP rational nakshatra index could disagree at ULP boundary points; a documented test pins down exactly where and why, so the difference is a recorded convention, never a surprise. Legacy modules are imported by tests only as an oracle, never by production code.

## 8. What I need from you

Approve or amend: the overall plan, Decision KP-A (recommend Option A, preserve exact legacy boundary behavior in the KP layer), Decision KP-B (mean node asserted), Decision KP-C (one-time swetest mode commit). On approval I begin Step 1 and stop next at publication time.

## Implementation record (2026-08-09) - BUILT AND VERIFIED, PENDING PUBLICATION

All four steps implemented as approved, on branch kp-chain-v1 (four commits on top of published main 45ea7bf; tip d0d79fe505f6973921ae9a8e1ea8360365e49745). The branch is provably additive: 15 new files, README updated additively, swetest mode-only commit (Decision KP-C executed with corrected rationale: the certifier was NOT the chmod culprit, my manual audit executions were; the certifier copies to a temp path by design).

All six gates executed and green: Gate 1 oracle equivalence (51,429 dense + full boundary battery + ULP neighbors + adversarial spellings, zero mismatches); Gate 2 invariants ported into the default gate; Gate 3 11-case chart holdout vs the legacy kernel (275 chain comparisons, zero mismatches, max longitude delta 0.0 arcsec); Gate 4 fixture structural check 200/200; Gate 5 independent validator with an in-file flat-table reference (58k cases, zero failures; two of my own hand-derived anchor drafts were wrong and corrected after a third derivation, recorded in the commit message); Gate 6 certification artifact regenerated from scratch (certification/KP_CHAIN_V1_certification.json). Final battery: 267 tests, all three holdout validators, legacy gate 5/5, Tier-0 matrix PASS. Certified surfaces diff vs main: empty.

## Publication record (2026-08-09)

Published via owner bundle relay: origin/kp-chain-v1 pushed, main fast-forwarded 45ea7bf -> d0d79fe505f6973921ae9a8e1ea8360365e49745. Fresh-clone post-publication verification (EXECUTED): 267 tests, D9/D10/KP independent validators all PASS, legacy gate 5/5, Tier-0 and KP certification runners both regenerate PASS, working tree clean after certifier runs (O-1 resolved as intended). KP_CHAIN_V1 is CERTIFIED and PUBLISHED.
## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-09 | Lifted into docs/ from the out-of-repository plan document(s): KP_MIGRATION_PLAN.md. Content preserved; header, provenance note and change history added per docs/DOCUMENTATION_STANDARD.md s2. |
