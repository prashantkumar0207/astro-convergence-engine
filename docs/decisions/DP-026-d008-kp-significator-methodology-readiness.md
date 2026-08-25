<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents readiness state and options. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-25 |
| Review cadence | TBD |

# DP-026. `D-008`/`ADR-0027` KP-significator methodology-specification decision-readiness

## 0. Authorization and scope

Authorized by "CEO direction — proceed with DP-023 resolution," item 4: "Prepare/authorize separate
decision-readiness papers for `D-008` KP significators and Parashari yoga methodology, but do not
implement either." This paper does not draft the KP significator methodology specification itself - it
establishes what already governs the question, what remains genuinely open, and what a future
specification-drafting task would need. It does not implement anything.

## A. What already exists and governs this question

**Root `DECISION_LOG.md` D-008** (verbatim): "The next tier is KP_SIGNIFICATOR_V1. Its methodology
specification must be frozen before implementation. Claude may be used as an implementation engineer, but
implementation is accepted only after independent spec audit and adversarial/holdout validation." Per
this file's own classification note (added by `ADR-0022`): D-008's methodology requirement "stands in
full and is generalised" - it is not merely a KP-specific rule, it is a project-wide principle (the same
one this session's own "methodology-first rule" instruction independently invokes). D-008's own
sequencing claim ("the next tier") is superseded by `ADR-0026`'s dependency-driven order - **KP
significators are not claimed to be mandatorily next**, only that, whenever pursued, methodology must be
frozen first.

**`ADR-0027`** (`Status: PROPOSED - pending owner ratification (Q1)`, 2026-08-11) - **a finding not
surfaced in `DP-021` or `DP-023`'s own earlier citations of this material, verified directly this task:**
the eleven-element checklist this project has repeatedly cited as "D-008's own requirements" in fact
lives inside `ADR-0027`, which is itself still `PROPOSED`, not ratified. Searched `docs/DECISION_LOG.md`
for any later ratification of `ADR-0027` specifically: none found; a separate entry (`ADR-0013`'s own
disposition table) confirms as of its own writing that "ADR-0013 is not closed, because every disposing
entry [including `ADR-0027`] is itself PROPOSED." No evidence was found that this has changed since.
**The eleven-element checklist is well-specified but not yet owner-ratified.**

`ADR-0027`'s own Decision 3-4 (quoted, for the checklist itself): "Four separately scoped items, never
one feature. KP significators; four-step; ruling planets; horary. Each requires its own specification,
its own ADR and its own certification. Combining them into one vague feature is prohibited. A
KP_SIGNIFICATOR specification MUST define, at minimum: exact methodology; source authority; houses
considered; star, sub and sub-sub logic; four-step interpretation if applicable; ruling planets if
included; cusp handling; retrograde treatment; node treatment; boundary behaviour; school and profile
requirements; independent validation protocol; protected holdout; negative controls; acceptance
criteria; and explicit non-claims."

## B. Dependency readiness (calculation infrastructure vs. methodology)

**Substantially ready, independent of D-008's own status:** `KP_CHAIN_V1` already certifies the full
SL/NL/SB/SS lordship chain on every planet, cusp, and the ascendant (`docs/KP_CHAIN_SPEC.md`) - the raw
"cuspal sub-lord" ingredient a significator methodology would consume already exists and is certified.
The one genuine remaining calculation dependency is the polar-Placidus gap (`DP-025`, kept explicitly
separate) - `ADR-0027`'s own checklist item "cusp handling" would need to state its own domain boundary
regardless of whether `DP-025` is resolved first, but a frozen specification could, in principle, state
"undefined outside the certified domain" without waiting for `DP-025`'s own resolution.

## C. What remains genuinely open (not resolvable from repository evidence)

Every one of `ADR-0027`'s own eleven checklist items is currently blank - no document in this repository
states a chosen source authority, a chosen four-step tradition, a chosen node/retrograde treatment, or
any of the rest. This is not resolvable by research alone; per `ADR-0027`'s own item 3, KP significators,
four-step, ruling planets, and horary are four separately-scoped items, each needing its own
specification - meaning even "KP significators" alone, the narrowest of the four, is a substantial
drafting task, not a research question with a single findable answer.

## D. Options

1. **Authorize a dedicated `KP_SIGNIFICATOR_V1` specification-drafting decision-readiness task now**,
   scoped to KP significators alone (not the other three named items), producing a draft specification
   addressing all eleven checklist items for owner review - the natural next step, per `ADR-0027`'s own
   framing.
2. **First ratify `ADR-0027` itself** (a separate, narrower act than drafting the specification), since
   its own checklist is currently unratified guidance rather than a binding requirement - clarifies the
   governing text before building on it.
3. **Defer** - KP significators remain the highest-architectural-leverage candidate in `DP-023`'s own
   scoring, but nothing in this repository requires acting on it now; D45 (or another varga) can proceed
   independently.

## E. Recommendation and confidence

**At medium confidence:** ratify `ADR-0027` first (Option 2), since its own checklist is the load-bearing
reference this paper and `DP-023` both already cite as though authoritative - formalizing it costs
nothing substantive (it changes no calculation, no certified value) and removes an inconsistency between
how confidently this project's own documents cite it and its actual unratified status. Drafting the
specification itself (Option 1) is a substantially larger undertaking, reasonably pursued next but not
simultaneously.

## F. Explicit non-claims

This paper does not draft the `KP_SIGNIFICATOR_V1` specification. It does not resolve any of the eleven
checklist items. It does not ratify `ADR-0027`. It does not implement anything. It does not resolve
`DP-025`'s own polar-Placidus question, though it notes cusp handling would eventually need to state a
position on it.

## G. Exact CEO decision required

1. Ratify `ADR-0027` as written, or address its own unratified status separately.
2. Authorize a dedicated `KP_SIGNIFICATOR_V1` specification-drafting decision-readiness task, scoped to
   KP significators alone, or defer.
3. Confirm the four-item separation (`ADR-0027` item 3) remains binding - four-step, ruling planets, and
   horary are not to be folded into a KP-significator specification.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-25 | Created. Establishes what already governs KP-significator methodology (root D-008, `ADR-0027`'s own eleven-element checklist), a finding not previously surfaced that `ADR-0027` itself remains `Status: PROPOSED`, unratified, and what a future specification-drafting task would need. Recommends ratifying `ADR-0027` first, at medium confidence. Decides nothing; drafts no specification; implements nothing. |
