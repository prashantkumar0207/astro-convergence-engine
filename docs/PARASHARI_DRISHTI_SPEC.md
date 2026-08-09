<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | IMPLEMENTED AND CERTIFIED - decision entry ADR-0012 PROPOSED pending owner ratification (Q1) |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-09 |
| Review cadence | TBD (see docs/OPEN_QUESTIONS.md Q1) |

# Parashari graha drishti specification

> **Provenance and normative status.** This specification was authored as a plan,
> approved by the owner conversationally, and implemented before being lifted into
> `docs/`. `docs/PROJECT_CONSTITUTION.md` s7 states that anything not in the repository
> is input material and not truth, so the out-of-repository original carried no
> authority; this file is the resident specification. The governing decision is recorded
> in `docs/DECISION_LOG.md` at ADR-0012, whose status is PROPOSED pending owner
> ratification (Q1). The text below is DESCRIPTIVE of the certified implementation and
> of the decisions actually taken; the ADR is the normative record. Sections retain the
> numbering of the original plan, including its implementation and publication records,
> which are preserved as dated evidence.

Date: 2026-08-09
Status: PROPOSED. Implementation starts only after explicit approval.
Base: origin/main 3633db2 (varga batch certified and published).

## 1. Objective and school separation

Begin the aspect-systems layer, which the architecture mandates as SEPARATE MODULES PER SCHOOL, never one conflated engine. This first phase builds the Parashari graha drishti (planetary aspects) as PARASHARI_DRISHTI_V1, opening the engine/parashari/ package, the first school layer above the shared primitives. Jaimini rashi drishti, Western angular aspects, and KP aspect usage are explicitly OUT of this phase and will be their own modules under their own ADRs.

## 2. Classical rule (source identification)

Brihat Parashara Hora Shastra, drishti adhyaya, the full (purna) aspects: every graha aspects the seventh sign from its own; Mars additionally aspects the fourth and eighth; Jupiter additionally the fifth and ninth; Saturn additionally the third and tenth. Counting is inclusive sign-counting from the sign occupied by the aspecting planet (whole-sign, the same house-counting convention the certified D1 uses). The rule is a small frozen table: planet class to aspected-house offsets.

## 3. Decisions that need your explicit sign-off

Decision AS-A, scope: full aspects only. The fractional sputa drishti system (BPHS virupa strengths, quarter and half aspects by angular distance) is a genuinely different calculation with its own verification needs; it is deferred to its own ADR, recorded as a non-claim. V1 answers exactly: which planets fully aspect which signs, houses, and planets in a chart.

Decision AS-B, node aspects: EXCLUDED in V1. Traditions genuinely disagree on whether Rahu/Ketu cast aspects (some give them Jupiter-like 5/9 aspects, some none); BPHS manuscripts differ. Following the project's convention discipline (Rahu/Ketu dignity variants are already recorded-but-not-selected in the knowledge layer), V1 computes no node aspects, records the variant question explicitly, and a future profile-style selection can add them without touching certified behavior.

Decision AS-C, counting basis: whole-sign counting from the aspecting planet's sign, consistent with the certified D1 house decision. Aspects are reported at three granularities from one computation: aspected signs, aspected houses (via the chart's whole-sign houses), and aspected planets (planets occupying aspected signs).

## 4. Architecture

engine/parashari/__init__.py (school package, isolated); engine/parashari/drishti.py (frozen aspect-offset table plus the computation over a certified D1 chart or snapshot); engine/models/drishti.py (typed results carrying provenance). Consumes only certified facts (sidereal sign positions, whole-sign houses). Nothing imports KP, dasha internals, or varga modules; nothing is imported BY them.

## 5. Certification gates

Gate 1, table integrity: the offset table (all grahas 7; Mars 4, 7, 8; Jupiter 5, 7, 9; Saturn 3, 7, 10) verified against a second independent transcription and a re-derivation from the classical statement. Gate 2, combinatorial verification: for all 12 x 12 (aspecting sign, target sign) pairs and every planet class, aspected-sign sets match an independently coded rule; symmetry and inclusiveness properties (a planet never aspects its own sign under full drishti; the 7th aspect is mutual at the sign level) proven exhaustively. Gate 3, external oracle: PyJHora's graha drishti function over full charts for the 11-case holdout matrix, zero categorical tolerance on the aspected-sign sets (pure combinatorics on sign positions; astronomy enters only through the already-certified positions). Gate 4, chart-level integration: aspects computed on certified D1 charts for the holdout cases, with planet-to-planet aspect lists cross-checked against hand-derived expectations for at least two cases. Gate 5, independent validator (validate_parashari_drishti_holdout.py, in-file lookup reference). Gate 6, certification artifact (certification/PARASHARI_DRISHTI_V1_certification.json), collected pinning test, additive README. Full existing battery (345 tests, ten validators, nine certifiers) must pass untouched.

## 6. Risks

The main risk is scope creep toward interpretation; the module stops at aspect FACTS (who aspects what), with strengths, yogas, and judgments out of scope. The node-aspect variant is the one classical controversy; Decision AS-B keeps it out of certified behavior and on the record.

## 7. What I need from you

Approve or amend: AS-A (full aspects only, sputa drishti deferred), AS-B (no node aspects in V1, variant recorded), AS-C (whole-sign counting, three reporting granularities). One word, approved, covers all.

## Implementation record (2026-08-09) - BUILT AND VERIFIED, PENDING PUBLICATION

Built on branch parashari-drishti-v1 (one commit on top of published main 3633db2; tip 7d170f829f51a112d358af179fde2abd1b3a5979). Fully additive except the README. Opens engine/parashari/, the first school layer, with methodology isolation enforced in code (parashari_lahiri snapshots only).

Approved decisions executed: AS-A full aspects only; AS-B no node-cast aspects (the oracle's 7th-aspect-for-nodes convention recorded as the divergent variant, oracle gate compares the seven classical grahas); AS-C whole-sign inclusive counting with signs/houses/planets reporting.

Gates: dual-transcribed offset table with special-aspect re-derivation; exhaustive 84-pair combinatorics (mutual 7th, never own sign); hand-derived Case C integration; PyJHora oracle fed our certified D1 placements across the 11-case holdout, 154 comparisons, zero mismatches; independent name-counting validator; regenerated artifact with pinning test. Full battery: 356 tests, eleven independent validators, legacy gate 5/5, ten certification runners regenerate PASS.

## Publication record (2026-08-09)

Published via owner bundle relay: origin/parashari-drishti-v1 pushed, main fast-forwarded 3633db2 -> 7d170f829f51a112d358af179fde2abd1b3a5979. Fresh-clone post-publication verification (EXECUTED): 356 tests, eleven independent validators PASS, legacy gate 5/5, ten certification runners regenerate PASS, tree clean. PARASHARI_DRISHTI_V1 is CERTIFIED and PUBLISHED; engine/parashari/ is the first school layer in certified production use.
## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-09 | Lifted into docs/ from the out-of-repository plan document(s): ASPECT_PARASHARI_PLAN.md. Content preserved; header, provenance note and change history added per docs/DOCUMENTATION_STANDARD.md s2. |
