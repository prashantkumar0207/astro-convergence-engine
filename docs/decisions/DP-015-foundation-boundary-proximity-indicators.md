<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and recommends one. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-21 |
| Review cadence | TBD |

# DP-015. FOUNDATION "boundary-proximity indicators where sensitivity warrants"

## 1. The question

`docs/Q8_CLOSURE_MATRIX.md` s4 (FOUNDATION, `ACCEPTED`/`ADR-0048`, owner-ratified) lists "Boundary-
proximity indicators where sensitivity warrants" as a FOUNDATION implementation-scope item, alongside
rise/set, panchanga, Rahu Kalam/Yamaganda/Gulika, civil-date rendering, and H-01/H-02. Unlike every
other item in that list, it has **never been touched by any task, any ADR, or any decision paper in
this repository** - it has no governing text of its own anywhere. This paper investigates what the
ratified text actually requires, what governs it today (nothing, ratified), what legitimate treatment
options exist, and what the minimum decision paper needed to close it looks like. It decides nothing
and is not implementation-authorized.

## 2. What is already established, and what is not

**Established (direct citation, not re-derived):**

- `Q8_CLOSURE_MATRIX.md` s4's implementation-scope line names it verbatim: "Boundary-proximity
  indicators where sensitivity warrants." No further definition, cross-reference, or specification
  accompanies that clause anywhere in the ratified matrix.
- A repository-wide search (`docs/`, `engine/`, `reports/`) turns up **zero code** implementing any
  general-purpose "distance to a classification boundary" mechanism outside one place: `engine/kp/
  chain.py`/`engine/models/kp_chain.py`'s `nearest_boundary_arcsec` field (KP_CHAIN_V1, `ADR-0006`).
  That field is **certified but explicitly NOT a Constitution s12 Locked artifact** ("Ratification of a
  certification is not a lock; this layer is NOT a Constitution s12 Locked artifact," `ADR-0006`'s own
  status line) - distinct from the FORMALLY LOCKED Tier-0 scope (`ADR-0005`/`ADR-0034`), which covers
  only "the astronomical calculation kernel... and the certified D9/D10 divisional mathematics" and
  does not name KP_CHAIN_V1 at all.
- That same field has its own **known, unresolved defect**: `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`
  finding H-07, "`nearest_boundary_arcsec` is blind to the sign boundary while its docstring claims all
  levels." Verified directly against the live code this session: `engine/kp/chain.py:36-43`'s `nearest`
  computation minimises over nakshatra/sub/sub-sub edges only, with **no thirty-degree (sign) term** at
  all, while `engine/models/kp_chain.py:37-41`'s docstring states the field is "distance to the closest
  owning-interval boundary at any level." `docs/DECISION_LOG.md`'s only citation of H-07 is inside
  `ADR-0027`, which is itself `Status: PROPOSED - pending owner ratification (Q1)` - **H-07 has no
  ratified decision anywhere**, and this paper does not attempt to resolve it (out of scope; a separate,
  KP-specific finding, not itself named in FOUNDATION's exit criteria).
- `docs/DASHA_CERTIFICATION_ROADMAP.md` (`Status: PROPOSED - research and planning only... pending owner
  ratification`) is the only document that discusses extending the concept beyond KP: "The KP layer
  exposes a boundary-proximity indicator precisely so consumers can flag critical classifications. The
  dasha layer... exposes nothing equivalent. This is arguably the single most valuable addition for
  BTR." Its own recommended sequence lists "Add a boundary-proximity indicator to the timeline" as step
  6 of 8, for the **dasha layer specifically** - and `Q8_CLOSURE_MATRIX.md` s5 (JATAKA)'s entry criteria
  separately cites "the Dasha roadmap's steps 1 to 6" including this same step. Dasha computation itself
  is JATAKA-phase work (`ADR-0020` D6's domain order), not FOUNDATION scope, so the JATAKA-entry
  boundary-proximity item and the FOUNDATION-exit boundary-proximity item are **not the same
  requirement**, though they share a concept and, if FOUNDATION built a general mechanism first, JATAKA
  could plausibly reuse rather than reinvent it - this paper does not decide that either way.
- `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` finding M-02 independently observes: "The oracle gate
  contains zero near-boundary Moon cases, in the layer where boundary proximity has the largest
  downstream effect" (the dasha layer, where the audit elsewhere states amplification runs "hundreds of
  days per degree").
- `docs/H7_BTR_SPEC.md` (the specification for BTR, the phase the roadmap names as the primary
  downstream beneficiary) contains **zero mentions** of "boundary-proximity" or "boundary-critical"
  anywhere in its text, confirmed by direct search. BTR is explicitly "orthogonal to the phases... never
  a prerequisite for convergence" (`Q8_CLOSURE_MATRIX.md` s13) and becomes reachable only after EVIDENCE
  exits - a phase considerably later than FOUNDATION. Nothing currently blocks on this capability
  existing.
- No FOUNDATION-tier capability (rise/set, panchanga, `TRIKALAM_V1`) exposes anything resembling a
  boundary-distance field today - confirmed by direct search across `engine/astronomy/`, `engine/
  astrology/`. `engine/astrology/longitude_utils.py`'s `division_index()`/`BOUNDARY_TOLERANCE` (the
  engine-wide, FORMALLY LOCKED classification convention) only decides WHICH SIDE of a boundary a value
  falls on; it computes no distance.
- `TRANSIT_V1`'s H-02 fix (`ADR-0065`, this session, already closed - **not reopened by this paper**)
  is adjacent context worth noting: the original H-02 finding's own proposed solution language was
  "report the event with an explicit signed residual and an accompanying declared division" - `ADR-0065`
  implemented only the declared-division half; `TransitEvent.residual_arcsec` (pre-existing, unsigned)
  is the closest thing TRANSIT_V1 has to a distance-style field today, and it measures numerical solve
  precision at a searched-for target, not distance from an arbitrary instant to the nearest
  classification boundary - a different computation. This is cited only as evidentiary context for what
  "boundary-proximity" might concretely mean if implemented for TRANSIT_V1-adjacent output; it does not
  reopen H-02's own already-closed fix decision.

**Not established (explicitly not decided by this paper):** whether boundary-proximity indicators
should be implemented, for which FOUNDATION capabilities "sensitivity warrants" one, what such an
indicator would concretely compute for panchanga/rise-set/trikalam, whether H-07 should be fixed, and
whether the FOUNDATION-scope item and the JATAKA-entry dasha item should share one mechanism.

## 3. A critical textual finding: does "explicitly deferred" even apply here?

`Q8_CLOSURE_MATRIX.md` s4's exit criteria read, in full: "Every capability above at the level ADR-0017
defines as production certified. H-01 and H-02 resolved and certified, or explicitly deferred by
decision with the dependent domains blocked accordingly."

Read literally, the **second sentence's alternate path ("or explicitly deferred... blocked
accordingly") is textually scoped to H-01 and H-02 by name** - it is not the general rule the first
sentence states for "every capability above." Boundary-proximity indicators are named only in the first
sentence's implementation-scope list, not in the second sentence's carve-out. Two readings are both
textually defensible:

- **Narrow reading:** only H-01/H-02 may satisfy FOUNDATION exit via deferral-with-blocking; every other
  scope item, including boundary-proximity indicators AND the already-deferred civil-date rendering
  (`ADR-0063`), needs actual "production certified" status - meaning civil-date rendering's existing
  deferral may **not**, by this reading, actually satisfy FOUNDATION's exit bar either, an ambiguity
  this paper surfaces but does not resolve, since it predates and is broader than this paper's own
  boundary-proximity scope.
- **Broad reading:** the deferral-with-blocking pattern is a general FOUNDATION convention the drafters
  illustrated using H-01/H-02 (the two items requiring the most explanation) without meaning to exclude
  every other scope item from the same treatment - consistent with Phase G's own, structurally similar
  exit criteria ("The three BLOCKER findings B-01, B-02, B-03 either resolved or explicitly deferred by
  decision"), which used the softer form for its **entire** named list, not a two-item carve-out.

This paper takes no position on which reading governs. It matters directly here: under the narrow
reading, "explicitly defer boundary-proximity indicators" may not by itself close FOUNDATION's exit
criteria even if the owner chooses deferral - closing FOUNDATION might then require either implementing
something, or the owner separately confirming the broad reading applies. **This is a governance-text
interpretation question, not an engineering one, and belongs in the owner's hands together with the
substantive choice below.**

## A. Exactly what Q8 requires

Literally: "Boundary-proximity indicators where sensitivity warrants," as one implementation-scope
bullet among several, with the general exit bar "at the level ADR-0017 defines as production certified"
(subject to section 3's ambiguity about whether an explicit-deferral path is available for this item at
all). No count, no named capability list, and no definition of "sensitivity warrants" accompanies it -
those are left to be filled in by implementation-time judgment or a decision paper, per the matrix's own
stated pattern of leaving scope items intentionally general at ratification time (`Q8_CLOSURE_MATRIX.md`
s1: ratification "authorises no implementation... each [phase entry] says so individually").

## B. Why the capability exists in FOUNDATION scope

No ratified document states the rationale directly. The best-evidenced explanation, assembled from
adjacent material rather than invented: FOUNDATION's own implementation scope is dominated by
INSTANT-BASED CLASSIFICATIONS (which tithi, which nakshatra, which yoga/karana, which sign, which
Rahu-Kalam-style period a given moment falls in) - exactly the kind of output where a small time or
longitude uncertainty can flip the answer near a boundary. `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`
already identifies this failure mode twice in FOUNDATION-adjacent code: H-02 (ingress instants
misclassified because the search residual is wider than the classification tolerance) and, in the
KP layer, H-07 (the one existing "flag this as boundary-critical" field silently omitting the sign
level). `docs/DASHA_CERTIFICATION_ROADMAP.md` states the motivating downstream use directly: "so
consumers can flag critical classifications," particularly for BTR, where "boundary proximity is the
primary sensitivity" (`G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-07's own behavioural-impact line). In
short: FOUNDATION produces the boundary-sensitive classifications; a proximity indicator is the
mechanism by which a later consumer (BTR, chiefly) can tell a robust classification from a fragile one
without re-deriving it.

## C. Whether any prior ADR/specification already governs it

**No.** Confirmed by direct search of `docs/DECISION_LOG.md` (no ADR mentions "boundary-proximity" in
FOUNDATION or general terms), `docs/decisions/` (no other DP addresses it), and every FOUNDATION-tier
module (`engine/astronomy/rise_set.py`, `engine/astronomy/panchanga*.py` equivalents, `engine/astrology/
trikalam.py`) for any related field or function - none exists. The only related material in the
repository is: `ADR-0006`/`ADR-0037` (KP_CHAIN_V1's own certification, which includes but never names
"boundary-proximity" - it calls it `nearest_boundary_arcsec`, and is `PROPOSED`-adjacent only insofar as
its own defect, H-07, sits in an unratified ADR); `docs/DASHA_CERTIFICATION_ROADMAP.md` (`PROPOSED`,
dasha-specific, not FOUNDATION); and the bare `Q8_CLOSURE_MATRIX.md` scope citation itself. Nothing
ratified defines what a FOUNDATION-tier boundary-proximity indicator would compute, for which
capabilities, or to what certification standard.

## D. Existing certified/locked scope affected

None. No FOUNDATION-tier capability's certified value would need to change merely to add a NEW,
additive field reporting distance-to-boundary (the same additive pattern `ADR-0065` used for H-02's
`declared_division`) - **if** that is the option chosen; this paper does not choose it. KP_CHAIN_V1's
own `nearest_boundary_arcsec`/H-07 is a separate, non-FOUNDATION, non-Locked certification untouched by
anything this paper recommends.

## E. Existing evidence and tests

None specific to FOUNDATION-tier boundary-proximity - it has never been built. The only related test
coverage is KP_CHAIN_V1's own equivalence tests (`engine/tests/test_kp_legacy_equivalence.py`), which
verify `nearest_boundary_arcsec` matches the certified legacy value, not that it is complete (it isn't,
per H-07). `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` M-02 additionally found the Vimshottari dasha
oracle gate contains zero near-boundary Moon cases despite this being "the layer where boundary
proximity has the largest downstream effect" - evidence that even where boundary sensitivity is known
to matter most (dasha), the certification gates do not yet exercise it.

## F. What legitimate treatment options exist

### Option 1 - Implement now, scoped to named FOUNDATION capabilities

Design and build an additive "distance to the nearest classification boundary" field for one or more
FOUNDATION-tier outputs (candidates: panchanga tithi/nakshatra/yoga/karana, trikalam period boundaries;
rise/set's NO_RISE/NO_SET states are a structurally different kind of edge case and may not fit the same
mechanism). Requires the owner (or a follow-up paper) to name which capabilities "sensitivity warrants"
covers - this paper does not propose an answer, since that is exactly the judgment call `Q8_CLOSURE_
MATRIX.md`'s own wording defers to implementation time.

- **Advantages:** directly and unambiguously satisfies FOUNDATION's general "production certified" exit
  bar for this scope item, sidestepping section 3's textual ambiguity entirely. Serves BTR's eventual
  need proactively.
- **Disadvantages:** real, currently-undesigned scope - no existing spec states what the field computes
  per capability, unlike H-02's fix (which had the audit's own "signed residual and declared division"
  language ready to extract) or H-01's fix (which had two named solutions ready to extract). Building it
  well requires the same kind of per-capability design judgment `DASHA_CERTIFICATION_ROADMAP.md`
  acknowledges is still open even for the one layer (dasha) that already has a worked KP precedent to
  learn from - and that precedent (H-07) is a cautionary tale of an incomplete implementation shipping
  with a docstring overclaiming its own coverage.
- **Certification implications:** a new gate (or gate addendum) per capability touched, analogous to
  H-02's Gate E.
- **Blast radius:** confined to whichever FOUNDATION capabilities are named; additive fields only, if
  designed that way.

### Option 2 - Explicitly defer, subject to section 3's ambiguity being resolved first

Record a decision explicitly deferring boundary-proximity indicators until a consuming feature (BTR,
principally) actually needs one - mirroring `DP-012`/`ADR-0063`'s civil-date-rendering precedent
exactly. Because nothing today silently depends on a boundary-proximity indicator existing (unlike
H-01, where a reachable code path was silently wrong), there is no "dependent domain" that needs
code-level blocking the way `ADR-0066` blocked true-node transit search - deferral here would be a pure
documentation-level decision, with nothing to enforce mechanically.

- **Advantages:** zero implementation cost; matches the established, owner-accepted `DP-012` pattern;
  correct if "sensitivity warrants" is judged, today, to mean "nowhere yet" (a defensible reading, given
  BTR itself is phases away and its own spec never mentions the concept).
- **Disadvantages:** per section 3, a pure-deferral decision may not, by the exit criteria's narrower
  textual reading, actually satisfy "every capability above at the level ADR-0017 defines as production
  certified" - the same open question that already, quietly, applies to civil-date rendering's existing
  deferral. Choosing this option without the owner also addressing section 3 risks a FOUNDATION-exit
  acceptance later being challenged on textual grounds.
- **Certification implications:** none.
- **Blast radius:** none.

### Option 3 - Treat this as out of FOUNDATION's critical path pending a narrower, later decision

A variant of Option 2: explicitly note in the decision that FOUNDATION's other capabilities (rise/set,
panchanga, trikalam, H-01, H-02) are independently certified and checkpoint-accepted, and that boundary-
proximity indicators - being a cross-cutting enhancement rather than a capability with its own certified
correctness claim - should be decided separately from, and need not gate, the FOUNDATION-exit CEO
checkpoint itself. This is a scoping/sequencing choice about how the *exit checkpoint* is structured, not
a technical option; it still requires the owner to resolve section 3's textual question, since it turns
on whether "production certified" is read to require this item at all before FOUNDATION can be called
exited.

## G/H/I - Advantages/disadvantages, certification implications, blast radius

Stated inline under each option in section F, following this session's established pattern; no
speculative detail added beyond what section 2's evidence supports.

## J. Whether existing certified values would change

No, under any option. Nothing in FOUNDATION's already-certified capabilities (rise/set, panchanga,
trikalam) or in TRANSIT_V1/KP_CHAIN_V1 would need a value change - Option 1's field, if built, is
additive by the same pattern already twice used this session (`ADR-0065`, `ADR-0066`).

## K. The minimum decision paper required

This paper (`DP-015`) itself is judged to be the minimum: a narrow scoping paper establishing (a) that
nothing governs this item today, (b) the section 3 textual ambiguity, and (c) the three treatment
options above. It deliberately does **not** attempt to pre-design Option 1's field-by-field mechanism -
doing so before the owner picks a direction would risk exactly the "invent a convention" failure mode
this session has been instructed to avoid throughout. If the owner selects Option 1, a **second,
follow-up paper** (or an ADR directly, if the design is simple enough to state in one) would then be
needed to name which capabilities are covered and what each field computes - that second paper is
explicitly NOT drafted here.

## L. Recommendation

No option is clearly compelled by the evidence. Weak lean, low confidence: **Option 2 (explicit
deferral), contingent on the owner also resolving section 3's textual question** - because (i) nothing
today is silently wrong in the way H-01 was (there is no live defect to stop), (ii) the one FOUNDATION-
adjacent precedent that exists (KP's `nearest_boundary_arcsec`) is itself unfinished and a caution
against building this quickly, and (iii) BTR, the stated primary beneficiary, is phases away and its own
spec does not yet reference the concept. This lean is explicitly **not** a strong recommendation -
Option 1 is equally legitimate if the owner judges FOUNDATION's exit bar requires it regardless of
section 3, and Option 3 is a legitimate sequencing choice if the owner wants to decouple this item from
the FOUNDATION-exit checkpoint entirely.

**Confidence: low.** This is a weaker basis for a recommendation than any other decision paper this
session has produced - there is no audit-authored "proposed solution" to extract (unlike H-01/H-02),
and the governing text itself carries a live interpretive ambiguity (section 3) that sits upstream of
the substantive choice.

## M. What is NOT being decided by this paper

Whether boundary-proximity indicators are built; which FOUNDATION capabilities they would cover; what
they would compute; whether H-07 is fixed; whether the FOUNDATION and JATAKA (dasha) boundary-proximity
needs share one mechanism; and, most importantly, which textual reading of section 3 governs FOUNDATION's
exit criteria generally - a question this paper surfaces but does not resolve, and which also bears on
civil-date rendering's already-recorded deferral (`ADR-0063`), not only on this item.

## N. Exact CEO/owner decision required

Two, genuinely separate, decisions:

1. **The interpretive question (section 3):** does FOUNDATION's exit criteria require an item to be
   "production certified," full stop, unless it is H-01 or H-02 by name (narrow reading) - or does the
   "explicitly deferred by decision with the dependent domain blocked accordingly" pattern generally
   apply to any FOUNDATION scope item, matching Phase G's own precedent (broad reading)? This governs
   not only boundary-proximity indicators but also whether civil-date rendering's existing deferral
   (`ADR-0063`) already satisfies FOUNDATION exit.
2. **The substantive question:** given that interpretive answer, select Option 1 (implement, naming
   which capabilities), Option 2 (defer explicitly), or Option 3 (decouple from the exit checkpoint) for
   boundary-proximity indicators specifically.

Recorded as a new, numbered decision-log entry citing this paper - this paper alone authorizes nothing.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-21 | Created. Investigates the FOUNDATION-scope "boundary-proximity indicators where sensitivity warrants" gap: confirms nothing ratified governs it, traces the only related code (KP_CHAIN_V1's `nearest_boundary_arcsec` and its own unresolved H-07 defect) and the only related planning document (`DASHA_CERTIFICATION_ROADMAP.md`, PROPOSED), and surfaces a textual ambiguity in `Q8_CLOSURE_MATRIX.md` s4's exit criteria about whether the explicit-deferral path is scoped to H-01/H-02 only. Presents three treatment options with a low-confidence lean toward deferral. Options only; decides nothing; not implementation-authorized. |
