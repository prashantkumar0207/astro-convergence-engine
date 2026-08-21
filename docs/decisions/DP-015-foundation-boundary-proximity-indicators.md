<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and recommends one. DECIDES NOTHING. Requires owner approval. |
| Version | 2.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-21 |
| Review cadence | TBD |

# DP-015. FOUNDATION "boundary-proximity indicators where sensitivity warrants"

## 0. CEO decision package (read this first)

Three genuinely separate questions, kept explicitly apart per the owner's own instruction not to
collapse them into one:

**Question 1 - the H-01/`ADR-0066` finding (confirmation only, not reopened).** The Q8 explicit-
deferral/dependent-domain-blocked carve-out is **textually valid for H-01** (`ADR-0066` is a decision,
and the dependent domain - true-node transit-event search - is blocked at the code level). Its use
there is **novel: no prior case in this repository's history has the owner accepting a "deferred, with
the gap blocked rather than fixed" treatment as satisfying an exit criterion.** `ADR-0049` (Phase G's
B-01/B-02/B-03) had an equivalent, even less restrictive clause available and used it for none of the
three - all three were fully remediated instead. **This finding is not represented as precedent for
anything else in this paper**, including boundary-proximity indicators' own treatment. Nothing about
H-01 is reopened, questioned, or reconsidered here - see section 4 for the full restatement.

**Question 2 - does the Q8 deferral carve-out reach beyond H-01/H-02? (owner interpretation required).**
The exact governing sentence is: "H-01 and H-02 resolved and certified, or explicitly deferred by
decision with the dependent domains blocked accordingly." Section 3 lays out, side by side: the exact
language and its immediate surrounding context; a structural comparison against Phase G's own,
differently-scoped exit criteria; and three possible characterizations - (a) explicitly limited to
H-01/H-02 by name, (b) generally applicable to any FOUNDATION scope item, or (c) genuinely ambiguous,
requiring owner interpretation - with the textual evidence and consequences of each stated plainly. This
paper adopts none of the three; **the carve-out is not silently extended to boundary-proximity
indicators anywhere in this document.**

**Question 3 - boundary-proximity indicators (option selection required, once Question 2 is answered).**
Section F presents three legitimate treatment options (implement now for named capabilities; defer
explicitly; decouple from the FOUNDATION-exit checkpoint), each restated in section 5 with its
consequences under each of Question 2's three possible answers. **`DP-012`/`ADR-0063`'s civil-date-
rendering deferral is not treated as precedent that deferral satisfies FOUNDATION's exit bar** - per
Question 2's own narrow-reading branch, that deferral's own textual sufficiency is exactly as open as
this item's would be, so it cannot be used to settle the question for either. No option is implemented
or chosen by this paper.

**What the owner must decide, precisely (restated from section N):** (1) confirm or correct the
Question 1 framing above; (2) choose one of Question 2's three characterizations, or supply a fourth if
none fit; (3) given that answer, select a Question-3 treatment option for boundary-proximity indicators.
All three are recorded together as a new, numbered decision-log entry citing this paper - nothing below
this section pre-selects any of them.

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

## 3. Does the Q8 deferral carve-out reach beyond H-01/H-02? Exact language, context, and three characterizations

**The exact governing sentence** (`Q8_CLOSURE_MATRIX.md` s4, "Exit criteria" row, `ACCEPTED`/`ADR-0048`,
quoted in full, nothing omitted): "Every capability above at the level ADR-0017 defines as production
certified. H-01 and H-02 resolved and certified, or explicitly deferred by decision with the dependent
domains blocked accordingly."

**Immediate surrounding context, also quoted exactly, for the same row's neighbours:**

- Implementation scope (same section): "Rise and set with declared conventions. Panchanga: tithi, vara,
  nakshatra as a panchanga element, yoga, karana. Rahu Kalam, Yamaganda, Gulika with variant tables
  recorded. Civil-date rendering for dasha boundaries. **Resolution of H-01 true-node completeness and
  H-02 the ingress classification seam.** Boundary-proximity indicators where sensitivity warrants."
  Note that H-01/H-02 are already singled out here, in the scope row itself, with the word
  "Resolution" attached specifically to them - boundary-proximity indicators get no equivalent verb,
  only a bare noun phrase.
- Certification gates (same section): "Per capability: declared conventions in a calculation profile;
  independent external reference for the astronomical parts; the varga template of frozen rule, second
  transcription, dense sweep, ULP battery, external oracle and independent validator for the
  classification parts; protected holdout; regenerable artifact; collected pinning test; ADR." This is
  what "production certified" concretely requires per capability under the first sentence of the exit
  criteria - a real, substantive bar, not satisfied by an ADR alone.
- Phase G's structurally comparable exit criteria (`Q8_CLOSURE_MATRIX.md` s3, ratified by the same
  `ADR-0048`): "G2, G3, G4, G5, G7 complete. DP-001 answered so ADR entries can leave PROPOSED. **The
  three BLOCKER findings B-01, B-02, B-03 either resolved or explicitly deferred by decision.**" Checked
  against how this actually played out: `ADR-0049` records that **all three of B-01, B-02, B-03 were
  fully remediated** - the "or explicitly deferred" branch was never actually exercised for any of them.
  So the repository has no case, in either phase, of the owner accepting a bare-deferral resolution for
  an exit-criteria item under either phrasing.

**Three possible characterizations of the carve-out's reach, stated with their textual support and
consequences, per the task's explicit requirement not to silently pick one:**

**(a) Explicitly limited to H-01/H-02 by name.** Support: the alternate path appears only in the second
sentence, which names H-01 and H-02 specifically; the first sentence's blanket "every capability above"
requirement is not itself qualified by any deferral option. The scope row's own asymmetric phrasing
("Resolution of H-01... and H-02..." vs. a bare, un-verbed "Boundary-proximity indicators...") reinforces
that H-01/H-02 were drafted as a distinguished pair. Phase G's parallel structure - a blanket clause plus
a SEPARATE, named-subset clause carrying its own alternate path - is consistent with this pattern
recurring by design, not accident. A further, non-textual but structural point: H-01 and H-02 are both
**defects in an already-built, reachable capability** (TRANSIT_V1), where "block the dependent domain"
names a concrete action (refuse the reachable bad path, as `ADR-0066` did). Boundary-proximity indicators
is a **capability that was never built at all** - there is no reachable, silently-wrong code path for a
deferral decision to "block," so even a generous reader extending the pattern by analogy would need to
explain what blocking a never-built capability's "dependent domain" would concretely mean. **Consequence
if this characterization governs:** boundary-proximity indicators (and, on the same reading, civil-date
rendering's existing `ADR-0063` deferral) cannot close FOUNDATION exit via a bare deferral decision;
either actual implementation is required, or the exit checkpoint must be restructured to not require it
(Option 3 below), or the owner must separately amend/reinterpret the ratified text.

**(b) Generally applicable to FOUNDATION scope.** Support: Phase G's own exit criteria used the softer
"resolved or explicitly deferred by decision" form for its entire named list (B-01/B-02/B-03), not a
two-item subset of a longer list - so there is a same-document precedent for treating "resolved or
deferred" as the general FOUNDATION-family convention for flagged findings, and a reader could take
H-01/H-02's fuller wording ("with the dependent domains blocked accordingly") as simply elaborating that
same convention for this phase rather than narrowing its reach. **Consequence if this characterization
governs:** a bare, well-recorded deferral decision (matching `ADR-0063`'s form) would be sufficient for
boundary-proximity indicators too, though the "blocked accordingly" language would still need an answer
for what "blocked" means when there is no existing reachable path (see (a)'s point above, which
applies under this reading too, not only the narrow one).

**(c) Genuinely ambiguous, requiring owner interpretation.** Support: both (a) and (b) are textually
defensible from the same sentence and the same document; nothing else in `Q8_CLOSURE_MATRIX.md`
(sections 1, 2, or 14's cross-phase invariants) or in `ADR-0021` D2 (which established that Q8 requires
named exit criteria per phase, but says nothing about how to read a specific phase's wording) resolves
which was intended. **Consequence if this characterization governs:** the owner's answer becomes the
authoritative reading going forward - worth recording as its own short interpretive ruling (either
inside the ADR that also picks a Question-3 option, or as a standalone addendum to `Q8_CLOSURE_MATRIX.md`
itself) since it will recur for civil-date rendering and any future FOUNDATION-family exit criteria
that use similar language.

**This paper does not select (a), (b), or (c).** It matters directly: under (a), or under (c) resolved
toward (a), boundary-proximity indicators cannot exit FOUNDATION via deferral alone. Under (b), or (c)
resolved toward (b), deferral remains textually available but still needs the "blocked accordingly"
question answered given there is nothing reachable to block. **The carve-out is not extended to
boundary-proximity indicators by this paper under any of the three.**

## 4. Question 1 restated: the H-01/`ADR-0066` finding (confirmation only - not reopened, not reconsidered)

Carried forward unchanged from the prior task's independent re-verification, restated here only because
the owner asked for it to be kept explicitly separate from Questions 2 and 3, not because anything about
it is uncertain or open for revision:

- `ADR-0066` is a decision. The dependent domain it names - true-node transit-event search via
  `find_crossings()` - is blocked at the code level (`UnsupportedNodePolicyError`), not merely deferred
  in a document. This satisfies the literal text of the H-01/H-02 carve-out quoted in section 3.
- Checked for repository precedent: **none exists.** `ADR-0049` (Phase G's B-01/B-02/B-03) had an
  equivalent, even less restrictive alternate path available in its own exit criteria and did not use it
  for any of the three findings - all three were fully remediated instead. No prior entry in
  `docs/DECISION_LOG.md` records the owner accepting a "gap blocked, not fixed" treatment as satisfying
  an exit criterion.
- **Conclusion, restated exactly as before:** the carve-out is textually valid for H-01, and its
  application there is legitimate - but it is a **novel application, not a precedented one**, and must
  not be cited as precedent for how boundary-proximity indicators (or anything else) should be treated.
  This paper does not do so anywhere in sections 3, 5, or F.
- H-01's code, `ADR-0066`, and the underlying finding are **not reopened, re-examined, or reconsidered**
  by this paper in any way. This section exists only to keep Question 1 visibly separate from Questions
  2 and 3, per the owner's explicit instruction.

## 5. Question 3 preview: options against each Question 2 characterization

Full option detail is in section F; this table gives the CEO-package cross-reference the owner asked
for, mapping each Question-2 characterization to what each Question-3 option would actually mean.

| | (a) Limited to H-01/H-02 | (b) Generally applicable | (c) Ambiguous -> owner picks |
|---|---|---|---|
| **Option 1 - Implement** | Only path that certainly satisfies exit criteria for this item. | Also satisfies exit criteria; sidesteps needing to answer (b)'s own "blocked accordingly" gap. | Satisfies exit criteria under either resolution of (c). |
| **Option 2 - Defer** | Does **not**, by itself, satisfy the exit criteria's blanket "production certified" sentence - FOUNDATION exit would need a separate resolution (e.g. Option 3, or amending the text). | Textually available, but "blocked accordingly" has no concrete referent since nothing reachable exists to block - a documentation-only deferral, weaker than `ADR-0066`'s. | Owner's resolution of (c) determines which of the two columns to the left applies. |
| **Option 3 - Decouple from exit checkpoint** | Sidesteps the question entirely by removing this item from what "FOUNDATION exit" is defined to require - itself a scope-of-the-checkpoint decision, not an interpretation of existing text. | Same as under (a) - a sequencing choice orthogonal to which characterization governs. | Same as under (a)/(b) - available regardless of how (c) resolves. |

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

### Option 2 - Explicitly defer, subject to section 3's characterization being resolved first

Record a decision explicitly deferring boundary-proximity indicators until a consuming feature (BTR,
principally) actually needs one. **`DP-012`/`ADR-0063`'s civil-date-rendering deferral is a prior case
of the owner choosing this same kind of decision for a different FOUNDATION scope item, but it is
explicitly NOT treated as precedent here that deferral satisfies FOUNDATION's exit bar** - under
section 3's characterization (a), civil-date rendering's own deferral is exactly as textually open as
this one would be, so it cannot be used to settle the question for either; it would need the same
Question-2 answer this item does. Because nothing today silently depends on a boundary-proximity
indicator existing (unlike H-01, where a reachable code path was silently wrong), there is also no
"dependent domain" that needs code-level blocking the way `ADR-0066` blocked true-node transit search -
deferral here would be a pure documentation-level decision, with nothing to enforce mechanically, which
is itself a reason section 3(a)'s "nothing reachable to block" point weighs against this option even
under a generous reading of the carve-out.

- **Advantages:** zero implementation cost; correct if "sensitivity warrants" is judged, today, to mean
  "nowhere yet" (a defensible reading, given BTR itself is phases away and its own spec never mentions
  the concept).
- **Disadvantages:** per section 3, a pure-deferral decision may not, under characterization (a) or (c)
  resolved toward (a), actually satisfy "every capability above at the level ADR-0017 defines as
  production certified" - the same open question that already, independently, applies to civil-date
  rendering's existing deferral (not resolved by this paper, and not settled by citing that deferral as
  though it were established precedent). Choosing this option without the owner also resolving section 3
  risks a FOUNDATION-exit acceptance later being challenged on textual grounds.
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
deferral), contingent on the owner resolving Question 2 (section 3) toward a characterization that
permits it** - because (i) nothing today is silently wrong in the way H-01 was (there is no live defect
to stop), (ii) the one FOUNDATION-adjacent precedent that exists (KP's `nearest_boundary_arcsec`) is
itself unfinished and a caution against building this quickly, and (iii) BTR, the stated primary
beneficiary, is phases away and its own spec does not yet reference the concept. This lean does **not**
rest on `DP-012`/`ADR-0063` as precedent (see section F Option 2's own caveat) and is explicitly **not**
a strong recommendation - Option 1 is equally legitimate if the owner resolves Question 2 toward
characterization (a) and judges implementation the only way to satisfy it, and Option 3 is a legitimate
sequencing choice regardless of how Question 2 resolves.

**Confidence: low.** This is a weaker basis for a recommendation than any other decision paper this
session has produced - there is no audit-authored "proposed solution" to extract (unlike H-01/H-02),
and the governing text itself carries a live interpretive question (section 3) that sits upstream of the
substantive choice.

## M. What is NOT being decided by this paper

Whether boundary-proximity indicators are built; which FOUNDATION capabilities they would cover; what
they would compute; whether H-07 is fixed; whether the FOUNDATION and JATAKA (dasha) boundary-proximity
needs share one mechanism; which of section 3's three characterizations governs FOUNDATION's exit
criteria generally (surfaced, not resolved - and note this also bears on civil-date rendering's already-
recorded deferral, `ADR-0063`, not only on this item); and the H-01/`ADR-0066` finding, which is
confirmed-and-restated only (section 4), never reopened or reconsidered.

## N. Exact CEO/owner decision required

Three genuinely separate decisions, matching section 0's package exactly:

1. **Question 1 (confirmation only):** confirm or correct section 4's restatement - the H-01/`ADR-0066`
   carve-out reading is textually valid but novel, with no repository precedent, and is not itself being
   reopened.
2. **Question 2 (interpretation required):** which of section 3's three characterizations governs the
   Q8 deferral carve-out's reach - (a) limited to H-01/H-02 by name, (b) generally applicable to any
   FOUNDATION scope item, or (c) something else the owner states directly? This answer governs not only
   boundary-proximity indicators but also whether civil-date rendering's existing deferral (`ADR-0063`)
   already satisfies FOUNDATION exit - a question this paper surfaces but does not resolve on its own.
3. **Question 3 (option selection):** given the answer to Question 2, select Option 1 (implement, naming
   which capabilities), Option 2 (defer explicitly), or Option 3 (decouple from the exit checkpoint) for
   boundary-proximity indicators specifically - per section 5's cross-reference of what each option means
   under each possible answer to Question 2.

Recorded together as a new, numbered decision-log entry citing this paper - this paper alone authorizes
nothing, implements nothing, and extends the H-01/H-02 carve-out to nothing.

## Change history

| Version | Date | Change |
|---|---|---|
| 2.0.0 | 2026-08-21 | Restructured into an explicit three-question CEO decision package per owner instruction: Question 1 (H-01/`ADR-0066` finding, confirmation-only, new section 4) kept visibly separate from Question 2 (Q8 deferral-carve-out scope, section 3 rewritten to present three named characterizations - limited to H-01/H-02, generally applicable, or ambiguous - each with exact governing language, surrounding context, and consequences, per the owner's explicit "do not silently extend the carve-out") and Question 3 (boundary-proximity treatment options, section F, cross-referenced against each Question-2 answer in new section 5). Removed all "established precedent"/"owner-accepted pattern" framing around `DP-012`/`ADR-0063` per the owner's explicit instruction not to treat it as precedent - civil-date rendering's own deferral is now stated as equally open under characterization (a), not as settled ground. Added a structural argument (H-01/H-02 are defects in a built, reachable capability; boundary-proximity indicators is a never-built capability with nothing reachable to "block") that applies under any characterization. New section 0 gives the owner a single, cleanly separated summary of exactly what to decide. No option chosen; no carve-out extended; H-01 not reopened. |
| 1.0.0 | 2026-08-21 | Created. Investigates the FOUNDATION-scope "boundary-proximity indicators where sensitivity warrants" gap: confirms nothing ratified governs it, traces the only related code (KP_CHAIN_V1's `nearest_boundary_arcsec` and its own unresolved H-07 defect) and the only related planning document (`DASHA_CERTIFICATION_ROADMAP.md`, PROPOSED), and surfaces a textual ambiguity in `Q8_CLOSURE_MATRIX.md` s4's exit criteria about whether the explicit-deferral path is scoped to H-01/H-02 only. Presents three treatment options with a low-confidence lean toward deferral. Options only; decides nothing; not implementation-authorized. |
