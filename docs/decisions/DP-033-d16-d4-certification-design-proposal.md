<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents a certification-design PROPOSAL. DECIDES NOTHING. Requires owner approval before any certifier/validator code is written. No `scripts/certify_d16.py`, `scripts/certify_d4.py`, `validate_d16_holdout.py`, or `validate_d4_holdout.py` exists as of this entry. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-09-04 |
| Review cadence | TBD |

# DP-033. Certification-design proposal: D16 (Shodasamsa) and D4 (Chaturthamsa)

## 0. Authorization and scope

Authorized by the owner's "CEO RATIFICATION - ADR-0089 AND ADR-0090" instruction (2026-09-04), item 5:
"After recording the ratification, prepare the certification-design work for D16 and D4 as the next
stage. Stop at the certification-design authorization boundary" - clarified via an explicit choice
between two readings (a written design proposal, or actual certification-code execution): **the owner
selected the written-proposal-only reading.** This paper is that proposal. It writes no code, executes
nothing, and creates no certification artifact. Certification-code authorization (writing and running
`scripts/certify_d16.py`/`certify_d4.py` and their independent validators) remains a separate,
not-yet-given act, to be requested explicitly, exactly as `ADR-0089`/`ADR-0090`'s own "Consequences"
sections already anticipate.

**Governing methodology, ratified and unedited by this paper:** `ADR-0089` (D16, `Status: ACCEPTED`)
and `ADR-0090` (D4, `Status: ACCEPTED`), both ratified 2026-09-04. This paper does not reopen either
entry's own frozen rule, school, or explicit non-claims - it proposes only how each would be certified.

## 1. Template this proposal follows

Both proposals below follow `docs/NEW_VARGA_IMPLEMENTATION_TEMPLATE.md`'s own operational checklist and
`docs/VARGA_CERTIFICATION_ROADMAP.md` section 6's per-varga certification requirements, and mirror the
gate letter-scheme every registry-routed varga's own certifier already uses (A through I, established
across D2/D3/D7/D12/D24/D30/D40/D45's own certification-execution stages). Both proposals additionally
follow the **standalone/unregistered pattern** D24's `ADR-0083` and D40's own certification-execution
stage used: a frozen rule object instantiated *inside the certifier script itself*, classified via the
already-certified generic `engine.astrology.varga_classifier.classify`, never touching
`varga_registry.py` or creating a production module - exactly matching `ADR-0089`/`ADR-0090`'s own
"Consequences" sections, which authorize certification-design work but explicitly withhold production
implementation.

---

# PART A: D16 certification-design proposal

## A.1 Rule under certification (proposed, standalone)

A `CyclicVargaRule(divisions=16, start_sign=(0,4,8,0,4,8,0,4,8,0,4,8), direction=(1,)*12)` instantiated
inside `scripts/certify_d16.py` itself - not `engine/astrology/varga_d16.py`, which would not exist yet.
Content hash to be computed once, from this frozen object, and pinned as a literal
`CERTIFIED_D16_CONTENT_SHA256` constant, per `ADR-0049`'s B-02 remediation and every prior varga
certifier's own precedent - not computed at certification time from itself, which would trivially match.

## A.2 Proposed gates

| Gate | Purpose | Mirrors |
|---|---|---|
| A - Table/constant integrity | The frozen `start_sign`/`direction` table matches `ADR-0089` section 3's construction cell by cell, content-hash pinned | D24/D40 Gate A |
| B - Dense mathematical sweep | ~51,429 points vs. an independently coded classical reference (re-derived from `ADR-0089`'s own text, not imported from the rule under test) | D24/D40 Gate B |
| C - Corroboration disclosure | PyJHora's own `shodasamsa_chart()` read directly from source (already done, `ADR-0089` section 3); genuine oracle execution deferred to CI, exactly as D40's own certification-execution stage disclosed - **not executed locally**, this host's PyJHora environment remains degraded | D40 Gate C (disclosure form) |
| D - Isolation | Confirms the certifier touches no existing `engine/` file and the standalone rule is never registered - mirrors D24's original `ADR-0083`-stage Gate D and D40's own pre-production Gate D exactly | D24/D40 Gate D (isolation form) |
| E - Independent validator | `validate_d16_holdout.py`, a from-scratch reimplementation importing nothing from `engine.astrology` | D24/D40 Gate E |
| F - Boundary cases | Sign-transition edges over all 12 signs x 16 divisions (192 boundaries); `DP-032` section B.F already computed this sweep clean (zero mismatches) - the certifier would reproduce that computation independently, not cite the paper's own numbers as proof | D24/D40 Gate F |
| G - Protected holdout | Prime-step deterministic sampling, independent of gates B/F, never used to tune the frozen rule | D24/D40 Gate G |
| H - Negative controls | A real planted violation (e.g. `start_sign[0]` mutated), confirmed detected, confirmed the frozen object itself remains unmutated | D24/D40 Gate H |
| I - Static reference regression | LIVE certifier output compared against STATIC values frozen from the independent validator's own output, never regenerated by the certifier's own rule at certification time (the `ADR-0079` lesson, applied from the outset) | D24/D40 Gate I |

**No composition/plumbing mutation gate is proposed** for D16 at this standalone stage - matching D24's
and D40's own precedent exactly (that gate only becomes meaningful once a production module exists and
routes through `build_varga_chart()`; per `ADR-0088`'s own MEDIUM-1 finding, D16 would rely on
`VARGA_D45_V1`'s own Gate I for that shared-path coverage once production-registered, not duplicate it).

## A.3 Independent validator strategy

`validate_d16_holdout.py`, mirroring `validate_d24_holdout.py`/`validate_d40_holdout.py` exactly: a
from-scratch `reference_d16()` re-deriving the movable/fixed/dual -> Aries/Leo/Sagittarius rule from
`ADR-0089` section 3's own text (not imported from PyJHora or the certifier's own rule object), a static
holdout of ~10 hand-picked longitude cases with pre-computed expected `(d_sign, division_index)` pairs,
and a `generate_static_expected()` helper to produce those pairs once, offline, for gate I's own use.

## A.4 Oracle/PyJHora plan

Disclosure-only at this stage, identical to D40's own certification-execution stage: PyJHora's own
published source already read and cited (`ADR-0089` section 3); genuine execution deferred to this
project's own CI hash-pinned oracle environment, **not performed locally** (degraded environment,
unchanged, already disclosed). CI-oracle wiring itself remains explicitly out of scope for this proposal
and for the certification-design stage generally, per `ADR-0089`'s own "Consequences" section.

## A.5 Boundary/holdout test plan

Full absolute-longitude sweep across all 12 signs x 16 divisions (192 boundaries): at-exact-boundary,
3-ULP-above, and a coarse-step-below, mirroring the D24/D40/D45 gate-F convention exactly. `DP-032`
section B.F already performed this computation and found zero mismatches - the actual certifier would
recompute it fresh, not cite that paper's numbers as certification evidence (papers are not proof; a
reproducible run is).

---

# PART B: D4 certification-design proposal

## B.1 Rule under certification (proposed, standalone)

A `SegmentVargaRule(segments=(...), division=4)` instantiated inside `scripts/certify_d4.py` itself,
per `ADR-0090` section 3's full 12x4 table - not `engine/astrology/varga_d4.py`. This mirrors
`scripts/certify_d3.py`'s own precedent structurally (the one existing certifier for a
`SegmentVargaRule`-based, multi-sign-jump varga), not `certify_d24.py`/`certify_d40.py`'s
`CyclicVargaRule`-based structure. Content hash pinned as a literal constant, same discipline as D16.

## B.2 Proposed gates

| Gate | Purpose | Mirrors |
|---|---|---|
| A - Table/constant integrity | The frozen 12x4 segment table matches `ADR-0090` section 3's table cell by cell, content-hash pinned | D3 Gate A |
| B - Dense mathematical sweep | ~51,429 points vs. an independently coded classical reference (re-derived from the kendra-step-3 rule, not imported) | D3 Gate B |
| C - Corroboration disclosure | PyJHora's own `chaturthamsa_chart()` (already read, `ADR-0090` section 3); not executed locally | D40 Gate C (disclosure form) |
| D - Isolation | Confirms the certifier touches no existing `engine/` file, never registers the standalone rule, and - per the owner's explicit item-2 instruction - never imports or modifies `CyclicVargaRule`/`varga_classifier.py`'s cyclic path | D3/D24/D40 Gate D, extended per the owner's explicit isolation instruction |
| E - Independent validator | `validate_d4_holdout.py`, from-scratch, importing nothing from `engine.astrology` | D3 Gate E |
| F - Boundary cases | All 12 signs x 4 divisions (48 boundaries); `DP-032` section A.F already computed this sweep clean | D3/D24/D40 Gate F |
| G - Protected holdout | Prime-step sampling, independent of B/F | D24/D40 Gate G |
| H - Negative controls | A real planted violation in the segment table, confirmed detected | D3/D24/D40 Gate H |
| I - Static reference regression | LIVE vs. frozen STATIC values from the independent validator | D24/D40 Gate I |

**Explicit isolation gate, per the owner's item-2 instruction** ("Do NOT modify the shared
CyclicVargaRule/Cyclic classifier architecture merely to support D4... Keep the implementation isolated
to D4 wherever technically possible"): Gate D would additionally assert, by direct source inspection
(mirroring `certify_d24.py`'s own AST-walk isolation check), that `certify_d4.py` imports
`SegmentVargaRule` only, never `CyclicVargaRule`'s `direction`/`step`-adjacent internals, and that
`engine/astrology/varga_rules.py`'s own file content hash is unchanged from the currently-committed
version - a direct, mechanically-checkable proof of the isolation commitment `ADR-0090` section 5 already
states as a design commitment, "to be verified again by direct diff at the production-implementation
stage."

**No composition/plumbing mutation gate proposed**, matching D16's own Part A.2 reasoning exactly.

## B.3 Independent validator strategy

`validate_d4_holdout.py`, mirroring `validate_d3_holdout.py` (the one existing `SegmentVargaRule`-based
validator) more closely than `validate_d24_holdout.py`: a from-scratch `reference_d4()` re-deriving the
kendra-step-3 rule from `ADR-0090` section 3's own text, independent of PyJHora and of the certifier's
own segment table, plus a static holdout.

## B.4 Oracle/PyJHora plan

Identical structure to D16's Part A.4 - disclosure only, not executed locally, CI-oracle wiring out of
scope for this stage.

## B.5 Boundary/holdout test plan

Full absolute-longitude sweep across all 12 signs x 4 divisions (48 boundaries), mirroring D16's Part
A.5. `DP-032` section A.F already computed this sweep clean; the certifier would recompute it fresh.

---

# PART C: What this proposal does not do

Does not create `engine/astrology/varga_d16.py`, `engine/astrology/varga_d4.py`, `scripts/certify_d16.py`,
`scripts/certify_d4.py`, `validate_d16_holdout.py`, or `validate_d4_holdout.py`. Does not compute or pin
any content hash (the numbers in `ADR-0089`/`ADR-0090` describe the frozen rule's *construction*, not a
computed artifact hash - hash pinning is the certification-EXECUTION stage's own act, per `ADR-0082`/
`ADR-0087`'s own precedent, explicitly deferred here). Does not execute any gate. Does not produce
`certification/VARGA_D16_V1_certification.json` or `certification/VARGA_D4_V1_certification.json`. Does
not modify `.github/workflows/ci.yml`, `certification_support.py`'s `CERTIFIER_SOURCES`/
`VALIDATOR_SOURCES` tuples, or any existing certification artifact. Does not authorize production
implementation or CI wiring for either capability - those remain separate, later, not-yet-given
authorizations, exactly as `ADR-0089`/`ADR-0090` already state.

## Exact CEO decision required

1. Authorize certification-code execution for D16 (writing and running `scripts/certify_d16.py` and
   `validate_d16_holdout.py` per Part A above), for D4 (Part B above), or both together.
2. Confirm or amend the proposed gate structure (Parts A.2/B.2) before code is written, if the owner
   wants a different gate set than the one proposed here.
3. Confirm the standalone/unregistered pattern (mirroring D24's `ADR-0083`/D40's own certification-
   execution stage) is the intended form, as opposed to some other sequencing.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-09-04 | Created. Certification-design proposal for D16 (`ADR-0089`) and D4 (`ADR-0090`), per the owner's explicit written-proposal-only clarification. Proposes gate structures, independent-validator strategies, oracle/PyJHora corroboration plans, and boundary/holdout test plans for both, mirroring the established D24/D40/D3 certifier precedents. Writes no code; executes nothing; produces no certification artifact; does not authorize certification-code execution. |
