<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents readiness state and options. DECIDES NOTHING. Requires owner approval. |
| Version | 1.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-25 (section H added: independent provenance audit of `ADR-0027`'s own checklist, per explicit CEO instruction - `ADR-0027` is NOT ratified by this update) |
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
the checklist this project has repeatedly cited as "D-008's own requirements" in fact lives inside
`ADR-0027`, which is itself still `PROPOSED`, not ratified. Searched `docs/DECISION_LOG.md` for any later
ratification of `ADR-0027` specifically: none found; a separate entry (`ADR-0013`'s own disposition
table) confirms as of its own writing that "ADR-0013 is not closed, because every disposing entry
[including `ADR-0027`] is itself PROPOSED." No evidence was found that this has changed since. **The
checklist is well-specified but not yet owner-ratified** - see section H for a further independent audit
of its own provenance, including a correction to this paper's own earlier miscount of its size.

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

Every one of `ADR-0027`'s own checklist items (section H corrects the count to sixteen, not eleven) is
currently blank - no document in this repository
states a chosen source authority, a chosen four-step tradition, a chosen node/retrograde treatment, or
any of the rest. This is not resolvable by research alone; per `ADR-0027`'s own item 3, KP significators,
four-step, ruling planets, and horary are four separately-scoped items, each needing its own
specification - meaning even "KP significators" alone, the narrowest of the four, is a substantial
drafting task, not a research question with a single findable answer.

## D. Options

1. **Authorize a dedicated `KP_SIGNIFICATOR_V1` specification-drafting decision-readiness task now**,
   scoped to KP significators alone (not the other three named items), producing a draft specification
   addressing all sixteen checklist items (section H) for owner review - the natural next step, per
   `ADR-0027`'s own framing.
2. **First ratify `ADR-0027` itself** (a separate, narrower act than drafting the specification), since
   its own checklist is currently unratified guidance rather than a binding requirement - clarifies the
   governing text before building on it.
3. **Defer** - KP significators remain the highest-architectural-leverage candidate in `DP-023`'s own
   scoring, but nothing in this repository requires acting on it now; D45 (or another varga) can proceed
   independently.

## E. Recommendation and confidence (v1.0.0 - superseded on the ratification question by section H; preserved as originally drafted)

**At medium confidence:** ratify `ADR-0027` first (Option 2), since its own checklist is the load-bearing
reference this paper and `DP-023` both already cite as though authoritative - formalizing it costs
nothing substantive (it changes no calculation, no certified value) and removes an inconsistency between
how confidently this project's own documents cite it and its actual unratified status. Drafting the
specification itself (Option 1) is a substantially larger undertaking, reasonably pursued next but not
simultaneously.

**Superseded, 2026-08-25:** the owner's own explicit instruction was "DO NOT ratify ADR-0027 yet. First
perform the necessary independent audit of ADR-0027's provenance/source basis." Section H performs that
audit; section H.4 restates the operative recommendation.

## F. Explicit non-claims

This paper does not draft the `KP_SIGNIFICATOR_V1` specification. It does not resolve any of the sixteen
checklist items (section H). It does not ratify `ADR-0027`. It does not implement anything. It does not
resolve `DP-025`'s own polar-Placidus question, though it notes cusp handling would eventually need to
state a position on it.

## H. Independent audit of `ADR-0027`'s own provenance/source basis (2026-08-25)

Authorized by the owner's explicit "First perform the necessary independent audit of `ADR-0027`'s
provenance/source basis and determine whether it should become the governing KP-significator methodology
authority" instruction. This section does not ratify `ADR-0027`; it reports what was found.

### H.1 A counting error in this project's own prior citations, corrected here

**`ADR-0027`'s own checklist has sixteen items, not eleven**, as `DP-021`, `DP-023`, and this paper's own
v1.0.0 text all repeated without independently counting. Enumerated directly from `ADR-0027`'s own
Decision 4 text: (1) exact methodology, (2) source authority, (3) houses considered, (4) star/sub/
sub-sub logic, (5) four-step interpretation if applicable, (6) ruling planets if included, (7) cusp
handling, (8) retrograde treatment, (9) node treatment, (10) boundary behaviour, (11) school and profile
requirements, (12) independent validation protocol, (13) protected holdout, (14) negative controls, (15)
acceptance criteria, (16) explicit non-claims. **This is disclosed as a self-correction, not attributed to
any other source** - the miscount originated in this session's own earlier paraphrasing and was carried
forward uncorrected across three prior documents until this audit counted the list directly.

### H.2 Where the checklist actually comes from

`ADR-0027`'s own Evidence line cites only: root `DECISION_LOG.md` D-008; `LOCK_MANIFEST.json`'s tier
table; `docs/KP_CHAIN_SPEC.md`'s own non-claims; `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-07.
**No external KP-astrology authority, classical text, or named methodology source is cited anywhere in
`ADR-0027` for the sixteen-item checklist itself.** The checklist's own structure - a numbered list of
"what a frozen methodology must define, at minimum," ending in independent validation/holdout/negative-
controls/acceptance-criteria/non-claims - is **not unique to KP significators in this repository**: the
same structural pattern appears independently in `ADR-0021` D1 (Mundane validation pre-registration:
event classes, hypotheses, training/holdout sets, hypothesis/event counts, multiple-comparison
methodology, effect-size measures, negative controls, replication) and in `docs/VARGA_CERTIFICATION_
ROADMAP.md` section 6 (varga certification requirements: source, school, frozen table, boundary policy,
independent reference, dense sweep, ULP battery, external oracle, protected holdout, regeneration runner,
artifact gate, provenance, ADR, certification artifact). **Conclusion: the checklist's own process-
structure is this project's own repeatedly-applied "methodology completeness" pattern, independently
re-derived at least three times (Mundane validation, varga certification, KP significators) - not a
KP-specific authority citation.** The KP-domain-specific *nouns* it names (houses considered, star/sub/
sub-sub logic, four-step interpretation, ruling planets, cusp handling, retrograde/node treatment, school
and profile) are genuine, recognizable KP terminology - real domain vocabulary was used in selecting which
sub-items to name - but this project has never checked the resulting list against an actual KP source text
for completeness (whether it omits something real KP practice requires) or correctness (whether the terms
are used as a KP practitioner would use them).

### H.3 Determination: should `ADR-0027` become the governing authority?

**Not yet, and not simply by ratification.** `ADR-0027`'s checklist is a credible, internally-consistent
*process* requirement (this repository's own established pattern, applied a third time) - ratifying it as
"the list of things a KP significator spec must define" carries little risk, since it changes no
calculation and commits to no specific methodology. But `ADR-0027` was never itself checked against any
named KP authority, and this audit does not perform that check either - it only establishes that no such
check has ever happened. **Recommendation, at medium confidence:** ratifying the *process* checklist
(that a spec must address these sixteen items) is low-risk and could proceed independently of the harder
question - but the owner's own instruction was not to ratify yet, so no ratification is proposed here;
instead, the recommendation is that any future `KP_SIGNIFICATOR_V1` specification task independently
verify the checklist's own completeness against a named KP source (e.g., K.S. Krishnamurti's own
foundational KP writings, or a widely-recognized modern compilation, analogous to how PyJHora's own yoga
module cites B.V. Raman by name and item number - see `DP-027` section H) rather than treating `ADR-0027`'s
own list as beyond question merely because it is procedurally sound.

### H.4 Operative recommendation (supersedes section E)

Do not ratify `ADR-0027` yet, per explicit instruction. If a future `KP_SIGNIFICATOR_V1` specification-
drafting task is authorized, it should independently re-verify the sixteen-item checklist against a named
KP source as part of its own work, rather than inheriting `ADR-0027`'s list unquestioned - and `ADR-0027`
itself could then be ratified alongside that work, once its own list has been checked rather than merely
inherited.

## I. Exact CEO decision required

1. Whether to authorize the independent KP-source cross-check of `ADR-0027`'s own checklist described in
   section H.3/H.4, as its own narrow task or folded into a future `KP_SIGNIFICATOR_V1` specification
   task.
2. Whether to ratify `ADR-0027`'s own sixteen-item checklist now as a process requirement only (not yet
   recommended, since the owner's own instruction was to audit first, which this section does, without
   itself proposing ratification).
3. Confirm the four-item separation (`ADR-0027` item 3) remains binding - four-step, ruling planets, and
   horary are not to be folded into a KP-significator specification.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-08-25 | Section H added: independent audit of `ADR-0027`'s own provenance/source basis, per explicit CEO instruction not to ratify `ADR-0027` yet. Corrects a self-propagated counting error (the checklist has sixteen items, not eleven, as `DP-021`/`DP-023`/this paper's own v1.0.0 all repeated). Traces the checklist to no external KP-authority citation - `ADR-0027`'s own Evidence line names none - and identifies its process-structure as this project's own repeatedly-applied "methodology completeness" pattern (independently matched in `ADR-0021` D1 and `docs/VARGA_CERTIFICATION_ROADMAP.md` section 6), while its KP-specific domain vocabulary is genuine but never checked against a named KP source. Recommends any future specification task independently verify the checklist against a named KP authority (as `DP-027`'s own PyJHora/B.V. Raman finding models) rather than inherit it unquestioned. Does not ratify `ADR-0027`. Section E's original recommendation preserved, marked superseded on the ratification question. |
| 1.0.0 | 2026-08-25 | Created. Establishes what already governs KP-significator methodology (root D-008, `ADR-0027`'s own checklist), a finding not previously surfaced that `ADR-0027` itself remains `Status: PROPOSED`, unratified, and what a future specification-drafting task would need. Recommends ratifying `ADR-0027` first, at medium confidence. Decides nothing; drafts no specification; implements nothing. |
