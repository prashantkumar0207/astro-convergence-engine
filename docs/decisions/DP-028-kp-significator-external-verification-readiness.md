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

# DP-028. KP-significator (`D-008`/`ADR-0027`) decision-readiness: external verification, priority confirmation, and the exact ratification question

## 0. Authorization and scope

Authorized by "CEO AUTHORIZATION — CONTINUE JATAKA ARCHITECTURE": continue autonomous decision-readiness
work from canonical `main` after the D45 merge (`c49336d`); independently determine the next unresolved
item, prioritizing KP significators / `D-008` **only if repository evidence confirms it remains the
highest-leverage unresolved item**; research the methodology question deeply enough to produce a genuine
decision paper covering fifteen named elements; perform and clearly distinguish external authoritative
research; draft/register the paper; do not implement KP significators; do not ratify `ADR-0027`.

This paper extends [[dp-026-d008-kp-significator-methodology-readiness]] (`DP-026`) section H, which
identified `ADR-0027`'s own sixteen-item checklist but found "no external KP-astrology authority,
classical text, or named methodology source... cited anywhere in `ADR-0027`," and recommended (section
H.4) that any future task "independently re-verify the sixteen-item checklist against a named KP source."
This paper performs that verification and answers the fifteen CEO-named elements. It does **not** rewrite
`DP-026` — it adds a new paper, per this project's own established discipline that decision papers add
sections/papers rather than silently rewrite prior ones.

It decides nothing, drafts no `KP_SIGNIFICATOR_V1` specification, implements nothing, and does not ratify
`ADR-0027` or any other ADR.

## A. Priority confirmation: is KP significators still the highest-leverage unresolved item?

The instruction is explicit: prioritize KP significators only **if evidence confirms it**, not merely
because it was previously recommended. This section makes that case honestly, including evidence that
complicates it.

**Evidence for KP significators:**
1. `Q8_CLOSURE_MATRIX.md` s5's JATAKA implementation-scope row does not name KP significators, Parashari
   yoga, or karakas at all (all three proceed via `ADR-0075`'s ILLUSTRATIVE interpretation, per `DP-022`)
   — so Q8 itself does not differentiate between them.
2. Root `DECISION_LOG.md` **D-008 exists specifically for KP significators** and nothing structurally
   equivalent exists for Parashari yoga or karakas — no root-level entry mandates a frozen methodology
   specification for those before implementation. This is a genuine, repository-evidenced asymmetry.
3. `ADR-0027` already provides a scaffolded sixteen-item checklist (unratified, but present) — `DP-027`
   had to construct an analogous checklist for Parashari yoga "by analogy," from nothing. Less
   from-scratch governance work remains for KP significators.
4. `specs/PROJECT_CHARTER.md`'s own analytical-systems language names "KP with Four-Step refinement"
   specifically; it does not similarly single out Parashari yoga by name (Parashari as a *school* is
   named throughout, but "Parashari yoga" as a distinct analytical capability is not called out the way
   KP's four-step refinement is).

**Evidence complicating the case (found this task, not previously surfaced):**
5. `DP-027` section H found PyJHora already implements **233 individually-named, B.V.-Raman-attributed
   yoga-detection functions** — a materially strong oracle-availability position. This task's own
   equivalent audit (section D below) found PyJHora has **no dedicated KP significator, ruling-planets, or
   four-step function at all** — only a generic lordship-chain calculator. On pure
   oracle-availability/certification-difficulty grounds, Parashari yoga is now **better** positioned than
   KP significators, not worse.

**Determination.** These are two different questions and this paper does not conflate them. "Which item
needs its *governance/methodology decision-readiness* investigated next" (this task's actual mandate) is
answered by items 1-4: KP significators has a root decision (`D-008`), a scaffolded checklist
(`ADR-0027`), and no repository evidence has emerged that displaces it as the correct **investigation**
target. "Which capability should be **implemented** first, if a choice must be made between the two" is a
separate question this paper does not resolve, and on which item 5 is genuinely new, relevant evidence
that a future capability-sequencing decision must weigh. **Confidence: high** that KP significators was
the correct target for this investigation; **the paper explicitly flags, rather than resolves,** the
oracle-availability asymmetry as a live consideration for whichever paper next addresses implementation
sequencing.

## B. Required KP methodology elements (`ADR-0027` Decision 4, re-verified)

`ADR-0027`'s own Decision 4 checklist has **sixteen items**, confirmed by direct re-count of the entry's
text (matching `DP-026` section H.1's own correction of this project's prior repeated undercount):
(1) exact methodology; (2) source authority; (3) houses considered; (4) star/sub/sub-sub logic; (5)
four-step interpretation if applicable; (6) ruling planets if included; (7) cusp handling; (8) retrograde
treatment; (9) node treatment; (10) boundary behaviour; (11) school and profile requirements; (12)
independent validation protocol; (13) protected holdout; (14) negative controls; (15) acceptance criteria;
(16) explicit non-claims.

Sections C-G below verify, against external authority, whether this checklist is complete and correctly
scoped — the specific gap `DP-026` section H left open.

## C. External source verification (WebSearch — explicitly external evidence, not repository evidence)

**Provenance note:** everything in this section comes from secondary web sources (search-engine results
describing K.S. Krishnamurti's work), not from the primary Reader texts themselves, which were not
directly available to fetch and read in full. This is disclosed explicitly per the CEO's instruction to
distinguish external evidence from repository evidence, and per this project's own `D-001`-style discipline
of naming the actual authority rather than a description of it. **A future `KP_SIGNIFICATOR_V1`
specification task should verify these claims against the primary Reader texts (or a citable secondary
compilation) directly before treating them as frozen source authority** — this paper raises confidence, it
does not itself constitute the "source authority" checklist item 2 requires.

1. **Foundational source.** K.S. Krishnamurti's own foundational works are commonly cited as the **"Six KP
   Readers"** (published from ~1968-1971), reorganised from an originally larger planned set. Reader II is
   commonly described as covering Fundamental Principles; Reader III as covering Predictive Stellar
   Astrology, which includes significator determination. Multiple independent web sources converge on this
   structure and attribution.

2. **Cuspal sub-lord theory** (developed by Krishnamurti, commonly dated to the 1960s) is described across
   sources as the system's central mechanism: a house matter is judged to manifest if that house's cuspal
   sub-lord signifies houses supporting the matter, and judged denied if the sub-lord signifies negating
   houses. The planetary lordship hierarchy this rests on — sign lord, star (nakshatra) lord, sub lord (and
   a further sub-sub-lord level) — matches this project's own already-certified `KP_CHAIN_V1` (SL/NL/SB/SS)
   structure directly, which is a point of genuine internal corroboration: the calculation substrate
   `KP_SIGNIFICATOR_V1` would consume already exists and is already certified.

3. **A significator-selection priority rule** is described across sources as part of core Krishnamurti
   methodology (a tiered rule for selecting the *strongest* significator among several candidate planets
   for a house): common with ruling planets ranks highest, followed by planets posited in the stars of the
   cuspal sub-lords of the required houses, followed by the cuspal sub-lords themselves, followed by a
   sub-lord to a house with no planets of its own in its stars. This is presented as core-system material,
   distinct from the "Four Step Theory" discussed next.

4. **Critical disambiguation — "Four Step Theory" is not part of Krishnamurti's original system.**
   Multiple independent sources agree: Four Step Theory was developed by a **different, later author,
   Sunil Gondhalekar** (commonly dated to ~1990, after study of "Sub Lord Speaks"-era KP material), and
   published under his own name (*Advance Theory Of KP — Four Step Theory*). It defines a four-step
   procedure for determining which houses a single planet signifies (via the planet's own occupation and
   ownership, its star lord, and sub-lord/cusp-level analysis), governed by its own named "9 rules." Most
   significantly for this project's own scoping question: sources explicitly describe Four Step Theory's
   **stated purpose as removing reliance on Ruling Planets** — i.e. it is presented in the literature as an
   **alternative** to Ruling Planets for significator work, not a component that depends on or extends it.

5. **Ruling Planets** (also Krishnamurti's own development) is a seven-factor construct (day lord; ascendant
   sign/star/sub lord; Moon sign/star/sub lord) described as intended to **verify or confirm a judgment at
   the moment of judgment** — i.e. it requires the ascendant and Moon position *at the time the question is
   judged*, not merely the natal chart. Sources consistently frame it as most native to **horary** practice
   (KP's own signature use case — "Krishnamurti Padhdhati" is widely associated with horary/Prashna
   prediction), rather than as a natal-chart-only technique.

## D. Repository-side oracle/reference-availability audit (repository/local-installation evidence, not external)

Searched the local PyJHora installation (scratchpad `oracle_probe_venv`, the same installation `DP-027`
searched for Parashari yoga functions) for any dedicated KP significator, ruling-planets, or four-step
function, in parallel to `DP-027`'s own methodology. **Finding: none exists.** The only KP-adjacent function
found is `utils.py::kp_lords_for_longitude(planet_label, lon_deg, include_sign_lord=False,
include_kp_index=True, levels=5)`, a **generic lordship-chain calculator** (up to 6 levels: sign, star, sub,
pratyantar, sookshma, prana/deha) — more granular than this project's own certified 4-level `KP_CHAIN_V1`,
but **not** a significator-determination function: it returns which planet rules a longitude at each
hierarchy level, not which houses a planet signifies, and implements no house-manifestation, ruling-planets,
or four-step logic whatsoever.

This is a materially important negative finding, reported honestly rather than glossed over: **KP
significators has a strictly worse oracle-availability position than Parashari yoga** (233 named,
attributed functions vs. zero dedicated functions). Any independent-validator design for
`KP_SIGNIFICATOR_V1` (checklist item 12) cannot lean on a pre-built external reference implementation the
way a future Parashari-yoga validator plausibly could — it would need to be built from a from-scratch
re-derivation of the frozen specification, the same pattern already used successfully for `D45`'s own
independent validator (`validate_d45_holdout.py`), which is feasible but is genuinely more work and carries
genuinely more re-derivation risk than validating against an existing, independently-authored oracle.

## E. Cusp handling and the polar-Placidus/M-04 dependency

`ADR-0027` checklist item 7 requires "cusp handling" to be defined. Cuspal sub-lord theory (section C.2) is
structurally cusp-dependent: every house's significator judgment begins from that house's cusp longitude and
its lordship chain. This project's cusps come from the FOUNDATION-tier house-cusp calculation, which
[[dp-025-polar-placidus-m04-tier0-maintenance]] (`DP-025`) already found has two open items: (A1) an
undefined-behaviour gap at high/polar latitude (`current_engine_certification.json`'s own holdout does not
bracket the true polar circle, ~66.5633°N/S), and (A2) an M-04 provenance-mislabeling gap (house-system
declaration not disclosed on the chart the way `declared_division`/`seed_boundary_convention` already are
elsewhere). Both remain **DEFERRED by owner instruction** as of `DP-024`/`DP-025`'s own entries in
`docs/decisions/README.md` — not resolved, not authorized, untouched since.

**This dependency is real but narrow, not blocking.** KP significator work for ordinary (non-polar)
natal charts does not require A1's resolution — the polar gap only matters for charts inside or near the
Arctic/Antarctic circle, an edge case, not the general case. A2 (provenance disclosure) is lower-stakes
still: it affects labelling, not calculated values. **Determination: a future `KP_SIGNIFICATOR_V1`
specification can proceed without A1/A2 resolution, provided it explicitly states, as one of its own
required non-claims (checklist item 16), that its cusp-derived judgments are unverified/out of scope for
charts inside the undefined polar-latitude band** — mirroring the same disclosure discipline already used
for `RISE_SET_V1`'s own polar non-claim. This paper does not reopen `DP-024`/`DP-025`; both remain
deferred exactly as the owner instructed.

## F. Four-step significator variants, ruling planets, and system-boundary scoping

`ADR-0027` Decision 3 already requires "four separately scoped items, never one feature: KP significators;
four-step; ruling planets; horary. Each requires its own specification, its own ADR and its own
certification." Section C's external research now gives this project **independent, external justification
for exactly that separation**, stronger than the process-only justification `ADR-0027` cited on its own:

- **Four-Step Theory is a distinct, separately-authored (Gondhalekar, ~1990) system**, not part of core
  Krishnamurti methodology, and is explicitly positioned in the literature as an *alternative* to Ruling
  Planets. A `KP_SIGNIFICATOR_V1` methodology specification that silently blended "core Krishnamurti
  significators" with "Four Step Theory" as if they were one settled system would misrepresent two
  different authors' work as one — `ADR-0027`'s own separation is now not just prudent scoping but
  factually necessary. **Recommendation: a V1 specification should implement core Krishnamurti significator
  theory (sections C.2-C.3) only, and treat Four-Step Theory as an explicitly out-of-scope future variant**,
  named as such in the non-claims (checklist item 16), not silently folded in.
- **Ruling Planets is structurally horary-adjacent** (requires judgment-time ascendant/Moon position, not
  only the natal chart) — a genuine system-boundary question for a JATAKA (natal) capability. Since this
  project's phase structure (`Q8_CLOSURE_MATRIX.md`) treats JATAKA and any future horary/Prashna phase as
  architecturally distinct, **Ruling Planets plausibly belongs to a future PRASHNA-phase capability, not to
  a JATAKA-phase `KP_SIGNIFICATOR_V1`.** This paper does not decide this — it flags it as a concrete
  scoping question the eventual ADR must answer explicitly, rather than assume.

## G. System isolation, provenance, and validation feasibility (repository-pattern evidence)

These three checklist items (11 school/profile requirements informing isolation; 15/12 validation feasibility) are primarily governed by patterns already established and certified in this repository, not by external KP sources:

- **System isolation:** the existing `CyclicVargaRule`/registry pattern (`varga_registry.py`, extended six
  times now through `D45`) and `KP_CHAIN_V1`'s own school-scoped design (`docs/KP_CHAIN_SPEC.md`) both
  demonstrate a workable isolation pattern: a new capability registers under its own identifier, is
  independently content-hashed, and cannot silently alter any existing certified capability. A
  `KP_SIGNIFICATOR_V1` implementation should follow the same pattern: a new, separately identified module
  consuming `KP_CHAIN_V1`'s already-certified output as a read-only input, never modifying it.
- **Provenance:** the `declared_division`/`seed_boundary_convention` disclosure-field pattern (used for
  `D45` and proposed for `DP-025` A2) is the established mechanism; a significator result should disclose
  which house-cusp system, which significator-priority rule variant, and which non-claims apply, on the
  chart itself, not only in documentation.
- **Independent-validator feasibility:** feasible but harder than `D45`'s own precedent, per section D — no
  pre-built oracle exists, so the validator must be an independent from-scratch re-derivation of the frozen
  specification (the same category of work as `validate_d45_holdout.py`, at a higher combinatorial
  complexity given 16 checklist items vs. a single cyclic mapping rule).
- **Protected holdout / negative controls:** both are mechanically identical in kind to the pattern already
  used for `D45` (gates F/G/H in `certify_d45.py`) — prime-step deterministic sampling for the holdout, and
  planted-mutation detection (tampering with a lordship value, a house-priority rule, or a content hash) for
  negative controls. No new mechanism needs to be invented; the existing certification-gate vocabulary
  transfers directly.

## H. Unresolved variants and required non-claims for a future specification

A future `KP_SIGNIFICATOR_V1` specification, if authorized, must explicitly state (checklist item 16) at
minimum:
1. Scope is core Krishnamurti cuspal-sub-lord significator theory only (section C.2-C.3); Four-Step Theory
   (Gondhalekar) is out of scope for V1, a distinct future variant (section F).
2. Ruling Planets is out of scope for a JATAKA-phase V1; it is a horary/judgment-time construct more
   naturally scoped to a future PRASHNA-phase capability (section F).
3. Horary/Prashna significator judgment generally is out of scope (already required by `ADR-0027` Decision
   3, reaffirmed here).
4. Judgments for charts with cusps inside the undefined polar-latitude band (per `DP-025` A1, still
   deferred) are unverified/out of scope, mirroring `RISE_SET_V1`'s own polar non-claim (section E).
5. The specification's own source citations must name the actual primary or citable secondary KP authority
   consulted, not merely restate this paper's own secondary-source summary (section C's own provenance
   caveat) — this paper is a readiness input, not itself the frozen source-authority citation checklist
   item 2 requires.

## I. Whether `ADR-0027` should be ratified now

`DP-026` section H.4 declined to recommend ratification, pending exactly the external verification this
paper performs. Having performed it: **`ADR-0027`'s sixteen-item checklist survives external scrutiny
essentially intact** — every item it names (methodology, source authority, houses, star/sub/sub-sub logic,
four-step-if-applicable, ruling-planets-if-included, cusp handling, retrograde, node, boundary, school/
profile, validation protocol, holdout, negative controls, acceptance criteria, non-claims) maps cleanly onto
a real requirement this task's own research surfaced, and Decision 3's four-way separation (significators;
four-step; ruling planets; horary) is now independently corroborated by external evidence (section F) rather
than resting on process-only reasoning alone.

**Recommendation: ratify `ADR-0027` as written, at medium-high confidence** (raised from `DP-026`'s prior
"not yet"). This paper does not ratify it — only the owner may. The one open point worth the owner's
attention before ratifying: `ADR-0027`'s own Evidence line still cites no external KP authority (as `DP-026`
H.2 found) — ratifying the checklist itself carries low risk since it commits to no calculation, but the
owner may prefer this paper's section C findings be folded into `ADR-0027` (or cited alongside it) rather
than ratifying `ADR-0027` in isolation, so the ratified record itself shows the external verification, not
only this paper.

## J. Explicit non-claims

This paper does not implement KP significators, `KP_SIGNIFICATOR_V1`, four-step logic, or ruling planets. It
does not ratify `ADR-0027` or any ADR. It does not reopen or resolve `DP-024` or `DP-025` (both remain
DEFERRED exactly as instructed). It does not touch FOUNDATION, closed Dasha items, H-03, or H10/H11. It does
not treat its own section C external-research summary as a substitute for primary-source verification by a
future specification-drafting task. It does not decide the Parashari-yoga-vs-KP-significators implementation
sequencing question — it only surfaces the oracle-availability asymmetry (section A, D) as evidence relevant
to that future decision.

## K. Exact CEO decision(s) required

1. Whether to ratify `ADR-0027` now, given this paper's external verification (section I) — and if so,
   whether to require `ADR-0027`'s own Evidence line be amended first to cite this paper's section C
   findings, or to ratify as-is with this paper cited alongside it.
2. Whether to authorize a `KP_SIGNIFICATOR_V1` methodology-specification-drafting task next (still not
   implementation), scoped per section H's non-claims (core Krishnamurti significators only; Four-Step and
   Ruling Planets explicitly deferred as separate future items).
3. Given the newly-confirmed oracle-availability asymmetry (section A, D): whether to proceed with KP
   significators next regardless, or to reconsider Parashari yoga as the better near-term implementation
   candidate on certification-difficulty grounds, while keeping KP significators' own governance/methodology
   track (items 1-2 above) moving in parallel.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-25 | Created. Extends `DP-026` section H with external verification (K.S. Krishnamurti's own Six Readers; cuspal sub-lord theory; ruling planets; the Gondhalekar/Four-Step-Theory disambiguation) and a repository-side PyJHora oracle-availability audit finding no dedicated KP significator/ruling-planets/four-step function exists (contrast `DP-027`'s 233-function Parashari-yoga finding). Confirms KP significators as the correct decision-readiness investigation target (section A) while flagging, not resolving, an implementation-sequencing tension the oracle-availability asymmetry raises. Recommends ratifying `ADR-0027` at medium-high confidence. Decides nothing; drafts no specification; implements nothing; does not ratify `ADR-0027`. |
