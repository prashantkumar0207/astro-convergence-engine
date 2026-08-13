# ARCHITECTURE AND IMPLEMENTATION AUDIT, 2026-08-11

Scope: adversarial read-only audit of the certified calculation layers, performed inside the G1
work package as authorised secondary work item D. Subjects: `engine/dasha/`, `engine/kp/`,
`engine/transits/`, `engine/parashari/`, the Generic Varga framework, provenance, and the
certification harness.

Method: four independent audits, each reading the source, the specification, the validator, the
certifier and the tests, and verifying claims by execution in throwaway processes. Nothing was
modified. Working tree clean throughout.

**No finding below has been fixed.** Every one of them touches certified calculation behaviour,
a certified artifact, or a certification methodology, which the work package places outside
authorised scope. This document is the escalation record required by execution rules 3 and 19.

Dated evidence. Preserved as written; later evidence is added by superseding note.

---

## How to read this

Findings are classified BLOCKER, HIGH, MEDIUM, LOW. The classification describes **engineering
risk to the eventual product**, not urgency of repair. Nothing here indicates a wrong number in
any currently published certification: every gate still passes, and the G1 fingerprint check
confirms calculation behaviour is unchanged from `1f861f6`.

What the findings do indicate is that several gates prove less than the documents claim they
prove. That distinction is the substance of this audit.

Each finding carries the six fields execution rule 3 requires: why it appears necessary, the
affected module, expected behavioural impact, certification impact, proposed solution, and tests
required.

---

## BLOCKER-class

### B-01. The varga registry never checks that a rule matches the division it is registered under

**Why it matters.** `engine/astrology/varga_registry.py:36-67` validates rule type, the D1/D9/D10
refusal, a non-empty school string and duplicate keys. It never relates `division` to
`rule.divisions` or to `len(rule.segments[s])`. Verified by execution: registering
`D12_PARASHARA` under division 4 is accepted, as are divisions 13, 0 and -5. A future D4 served
by a twelve-division rule would be silently and completely wrong, and no gate would notice
because every Gate D compares registry **keys** only.

**Module.** `engine/astrology/varga_registry.py`.

**Behavioural impact.** None today: all five registered rules are correct. The impact is entirely
prospective and lands on the next varga added, which is precisely the operation the roadmap
plans to repeat eight more times.

**Certification impact.** Gate D in all five varga certifiers becomes materially stronger. No
existing certified value changes.

**Proposed solution.** In `register_varga_rule`, assert `isinstance(division, int)`, a sane range
(2 to 300), and for `CyclicVargaRule` that `rule.divisions == division`; for `SegmentVargaRule`
that every source sign has the same segment count and that widths sum to 30.

**Tests required.** Rejection tests for each violation; a positive test that all five current
registrations still succeed unchanged; re-run all five varga certifiers to confirm byte-identical
gate values.

### B-02. A certified rule can be swapped at runtime and every non-invasiveness gate still passes

**Why it matters.** `unregister_varga_rule` (`varga_registry.py:70-72`) is unguarded and
`_REGISTRY` is plain mutable module state. Verified by execution: unregistering D3 and
re-registering `D30_PARASHARA` under `(3, "parashara")` leaves `registered_vargas()` byte-identical
while `classify(15.0, get_varga_rule(3, "parashara"))` returns the D30 answer. Rule **content** is
pinned nowhere in the default test run.

**Module.** `engine/astrology/varga_registry.py` and every varga gate-4 test.

**Behavioural impact.** None in normal operation. This is a gate-strength defect: the guard that
is supposed to prove the framework did not disturb certified behaviour cannot detect substitution
of the thing it guards.

**Certification impact.** The non-invasiveness claim in ADR-0009 through ADR-0011 is weaker than
stated. The claim itself remains true; its evidence is thinner than the wording implies.

**Proposed solution.** Assert identity in each varga's gate-4 test, `get_varga_rule(N, school) is
DN_PARASHARA`, and hash the rule tables into Gate D alongside the D9/D10 sweep hashes.

**Tests required.** Identity assertions for all five; a negative test proving a substituted rule
now fails the gate.

### B-03. Rule-content pinning reads a stored artifact instead of recomputing, contrary to VALIDATION_STANDARD rule 8

**Why it matters.** `engine/tests/test_sign_convention_certification.py:52-58` compares
`CERTIFIED_SWEEP_HASHES` against values read out of
`SIGN_CONVENTION_V1_certification.json`. `docs/VALIDATION_STANDARD.md` s2 rule 8 states
plainly that stored results are history, not proof, and that every certification re-executes.
Editing `navamsa_sign()` and not re-running the certifier leaves this gate green.

**Module.** `engine/tests/test_sign_convention_certification.py`, `scripts/certify_sign_convention.py`.

**Behavioural impact.** None. Gate-strength only.

**Certification impact.** Directly contradicts the project's own validation standard, in the gate
whose purpose is proving certified outputs did not move.

**Proposed solution.** Recompute the sweep live inside a collected test. Measured cost is roughly
one second for 53,019 points, which is affordable in the default gate.

**Tests required.** The recomputing test itself, plus a mutation check proving it fails when a
certified varga function is altered.

---

## HIGH

### H-01. `node_policy="true"` produces silently incomplete transit results

**Why it matters.** `engine/transits/speeds.py:46-49` sizes the search grid from a bound on
**speed**, but the algorithm's correctness requires at most one station per grid interval, which
is a bound on **station spacing**. Nothing in the repository bounds station spacing. Measured for
the true node: maximum speed 0.233 degrees per day, within the declared bound, but sixteen speed
sign changes in one hundred days, roughly one station every 6.25 days, against a grid step of
37.5 days. A sweep of sixty targets over four hundred days found four targets where production
reported fewer crossings than a fine scan; worst case reported one crossing where three exist.

`NODE_POLICY_TRUE` is defined in `engine/astronomy/profile.py:29` and supported by
`engine/transits/crossing.py:49-52`, so this is a reachable supported path. No shipped profile
selects it and no test exercises it.

**Module.** `engine/transits/crossing.py`, `engine/transits/speeds.py`.

**Behavioural impact.** Missing transit events, silently, with no error. For the two shipped
profiles a hundred-target randomised sweep found zero mismatches, so no published result is
affected.

**Certification impact.** TRANSIT_V1's completeness claim is scoped to mean-node bodies in
practice while the code advertises a broader contract.

**Proposed solution.** Either bound station spacing per body explicitly and size the grid from
that, or gate the true-node path behind an explicit refusal until it is certified. Do not simply
shrink the step: the correct invariant needs stating, not tightening by guess.

**Tests required.** A station-density test per supported body; a completeness comparison against a
fine scan for the true node; a refusal test if the path is gated.

### H-02. Ingress instants are classified into the wrong division by the engine's own certified classifier

**Why it matters.** The transit residual bound is `1e-4` arcsec, which is `2.78e-8` degrees. The
varga and D1 boundary tolerance is `1e-10` degrees. The residual envelope is therefore about 278
times wider than the boundary-promotion window, and bisection returns a bracket midpoint that
lands on either side of the true root at random. Measured on 2024 under `parashari_lahiri`: two of
twelve Sun sankranti instants classify into the **previous** sign, and twelve of twenty-eight Moon
nakshatra ingress instants classify into the previous nakshatra.

The existing gate misses this because it samples the classifier 0.05 degrees later for the Sun and
0.002 days later for the Moon, rather than at the event instant.

**Module.** `engine/transits/crossing.py`, `engine/astrology/longitude_utils.py`, and any future
consumer that joins a transit event to a classification.

**Behavioural impact.** A consumer asking "which sign holds the Sun at this sankranti instant?"
gets the previous sign roughly seventeen percent of the time, and the previous nakshatra roughly
forty-three percent of the time. This is the first bug a naive interpretation layer will produce.

**Certification impact.** Neither TRANSIT_V1 nor the varga certifications is wrong. The defect is
in the seam between them, which no certification covers because no certification spans both.

**Proposed solution.** Options, for owner decision rather than builder choice: report the event
with an explicit signed residual and an accompanying declared division so the consumer never has
to reclassify; or bias the returned instant to the side of the root that classifies into the
target division; or widen the classifier tolerance to exceed the residual bound. The first
preserves both existing conventions and is the only one that changes no certified behaviour.

**Tests required.** A cross-layer seam test asserting that classifying at an ingress instant
yields the target division, for every body and both profiles.

### H-03. The transit oracle gate cannot detect a systematic astronomical bias

**Why it matters.** `scripts/certify_transits.py:85-91` derives the per-event tolerance as
`delta_deg / speed + 120 seconds`, where `delta_deg` is measured **at our own event time**. Since
our longitude equals the target at that instant by construction, `delta_deg / speed` is exactly the
time disagreement, so a bias in our astronomy shifts the event and inflates the tolerance in exact
proportion. Verified by injection: a pure root-finder error of 72 minutes correctly FAILS, but a
systematic longitude bias of 1 arcmin, 5 arcmin, and even 20 arcmin, shifting every event by 24
minutes, 118 minutes and 7.9 hours respectively, all PASS, with the ratio asymptoting toward 1.0
without crossing it. Across all twenty-four anchors the derived tolerance exceeds the observed
disagreement by 119.999961 to 120.183753 seconds, that is, by the fixed slop term alone.

**Module.** `scripts/certify_transits.py`.

**Behavioural impact.** None on calculated values.

**Certification impact.** Material. Gate C is effectively subsumed by Gate A at a threshold about
fifty thousand times looser, and contributes no independent evidence. `README.md` describes
transits as verified by twenty-four PyJHora sankranti anchors, which overstates what the gate
establishes. This is the clearest instance in the repository of a tolerance derived in a way that
cannot fail.

**Proposed solution.** Compare the oracle's own reported ingress longitude and instant against
ours independently, rather than deriving the tolerance from the divergence being tested. If the
approximately 20.5 arcsec Sun divergence must be tolerated, bound it from an independent source,
for example swetest, and state the bound as a constant rather than recomputing it per event from
the quantity under test.

**Tests required.** The injection battery above, retained as a permanent adversarial gate: a
certification that cannot fail on a planted bias is not a certification.

### H-04. The stated Vimshottari depth-3 oracle certification does not exist

**Why it matters.** `scripts/certify_vimshottari.py:111` passes `depth=2` and compares
`timeline.antardashas()`. The oracle call leaves `dhasa_level_index` at its antardasha default. Every
"1,782 rows" figure is level-2 only. Meanwhile ADR-0007 records "Certify depths 1-3 only" and
`docs/ENGINE_STATUS.md` states timelines to three levels certified against the external oracle with
1,782 comparisons. Pratyantardasha rests solely on the in-repository closed-form validator.

This is a documentation-versus-evidence conflict, which the governance hierarchy classifies as a
**defect** requiring explicit resolution rather than a silent choice.

The audit ran the missing comparison in memory: 729 rows per case at pratyantar depth, zero lord
mismatches, maximum start delta 1.86e-09 days. **The gate would pass. It simply is not run.**

**Module.** `scripts/certify_vimshottari.py`, `docs/ENGINE_STATUS.md`, ADR-0007.

**Behavioural impact.** None. The mathematics appears correct.

**Certification impact.** A claim in two documents is not backed by the artifact they cite.

**Proposed solution.** Extend the gate to depth 3, regenerate the artifact, and correct whichever
of the two statements remains inaccurate. Do not correct the documents alone.

**Tests required.** The depth-3 oracle comparison itself, plus a pinning assertion on the recorded
row count so the level cannot silently regress.

### H-05. The hermetic tier cannot detect a wrong dasha anchor

**Why it matters.** Mutation test: flipping the sign at `engine/dasha/vimshottari.py:122` from
`birth_jd - float(elapsed_years * year_length)` to `+` injects a 4,748-day error into every dasha
date and passes every oracle-free gate. The JD-consistency test passes because both sides are
relative to the mutated anchor. The boundary test passes because anchor equals birth when elapsed
is zero. The independent validator is unaffected because it compares `Fraction` year offsets and
never inspects a Julian Day. Only the PyJHora oracle job catches it.

No committed numeric baseline of dasha calendar dates exists anywhere in the repository.

**Module.** `engine/dasha/vimshottari.py`, `validate_vimshottari_holdout.py`.

**Behavioural impact.** None currently. The anchor is correct.

**Certification impact.** The hermetic tier, which is the network-free reproducible one that runs
on both interpreters, provides no protection for the calendar half of the dasha layer.

**Proposed solution.** Commit a small frozen baseline of dasha instants for a handful of fixed
seeds and assert against it hermetically. This is a genuine protected holdout, which the layer
currently lacks entirely.

**Tests required.** The frozen-baseline test, plus the anchor mutation as a documented negative
control.

### H-06. No allow-list for dasha profiles; an uncertified year convention flows through production entry points

**Why it matters.** Verified: `vimshottari_parashari(birth, dasha_profile=DashaProfile('i_made_this_up',
Fraction(360), 'no source'))` returns a fully provenance-stamped timeline. Nothing rejects it.
Further, `DashaProfile.year_length_days` is annotated `Fraction` but unchecked, so passing a float
silently converts the entire timeline to float arithmetic and destroys the exactness guarantee the
module docstrings advertise, with no error and no failing test.

The varga layer refuses exactly this class of thing through `CERTIFIED_PRODUCTION_VARGAS` and
`UnsupportedVargaError`. The dasha layer has no equivalent.

**Module.** `engine/dasha/profile.py`, `engine/dasha/vimshottari.py`.

**Behavioural impact.** An uncertified year convention produces plausible-looking certified-shaped
output.

**Certification impact.** VIMSHOTTARI_V1 certifies one year convention. The code accepts any.

**Proposed solution.** A `CERTIFIED_DASHA_PROFILES` constant mirroring the varga pattern, with a
refusal error, plus runtime type enforcement on `year_length_days`.

**Tests required.** Refusal tests for an unregistered profile and for a float year length; a
positive test for the certified profile.

### H-07. `nearest_boundary_arcsec` is blind to the sign boundary while its docstring claims all levels

**Why it matters.** `engine/kp/chain.py:36-43` minimises over nakshatra, sub and sub-sub edges
only. There is no thirty-degree term. `engine/models/kp_chain.py:37-41` documents the field as the
distance to the closest owning-interval boundary **at any level**, and states that small values mean
the classification is boundary critical. Verified: `kp_chain(29.999999999)` returns `sign_lord='Ma'`
with `nearest_boundary_arcsec = 380.000004`. The sign lord is a few microarcseconds from flipping
and the safety indicator reports 380 arcsec of margin.

**Module.** `engine/kp/chain.py`, `engine/models/kp_chain.py`.

**Behavioural impact.** The layer's own boundary-criticality signal is wrong for one of its four
certified outputs. Any consumer instructed to flag boundary-critical results cannot flag sign-lord
criticality at all. This matters directly for BTR, where boundary proximity is the primary
sensitivity.

**Certification impact.** The field is not compared in any gate.

**Proposed solution.** Include the thirty-degree term, or rename the field and correct the
docstring. Changing the value changes a published output, so this needs an owner decision.

**Tests required.** Boundary-proximity assertions at all six unexercised sign boundaries.

### H-08. The KP boundary convention is exported into the Parashari-labelled dasha layer

**Why it matters.** `engine/dasha/vimshottari.py:59-62` is a third copy of the KP
`Decimal(str(x))` conversion rule, and `test_vimshottari_consistency.py:41-53` deliberately binds
the dasha seed to `kp_chain` including at exact boundaries. Consequence, verified: at six float
spellings of nakshatra boundaries a **Parashari-seeded** timeline disagrees with the engine's own
Parashari `nakshatra()` about which nakshatra the Moon occupies, and therefore about the entire
mahadasha sequence. A chart display and its dasha table can disagree.

The KP layer's differing convention is documented and deliberate. Its export into a
Parashari-facing layer is not documented anywhere.

**Module.** `engine/dasha/vimshottari.py`, `engine/kp/intervals.py`, `engine/astrology/longitude_utils.py`.

**Behavioural impact.** Confined to a `1e-10` degree window, so no realistic chart is affected. The
architectural point stands regardless: this is a school-isolation leak, and school isolation is a
charter non-negotiable.

**Certification impact.** None of the three layers is individually wrong. No gate spans them.

**Proposed solution.** An owner decision on which convention a Parashari-seeded dasha follows,
recorded in an ADR, then a pinning test that makes the choice explicit and visible.

**Tests required.** A cross-layer convention test enumerating the divergent boundaries, which the
KP specification already promises and which does not exist.

---

## MEDIUM

**M-01. The promised KP convention-divergence pinning test does not exist.** `docs/KP_CHAIN_SPEC.md:79`
commits to a documented test pinning exactly where and why the two conventions diverge. The two
tests that exist both sample at `+0.001`, off-boundary, so nothing would fail if
`BOUNDARY_TOLERANCE` were widened even to `1e-6`. The six divergent boundaries are unrecorded.

**M-02. The Vimshottari certification's two named boundary cases are not boundary cases.** Measured
Moon distance to the nearest nakshatra boundary: 6.46 degrees and 5.0 degrees. Both are farther
from a boundary than a case not labelled as one. The oracle gate contains zero near-boundary Moon
cases, in the layer where boundary proximity has the largest downstream effect.

**M-03. Anti-fitting scan does not cover the code most likely to contain fitting.**
`scripts/certification_support.py:80` defaults to `targets=("engine",)`, so all eleven certifiers,
all eleven root validators and the fixture module are never scanned. Combined with a
nine-fragment keyword grep, the gate is evadable by anyone not using the word "fudge".

**M-04. `DrishtiChart` provenance mislabels the house convention of its own output.** Provenance
records `house_system == 'P'` (Placidus) while `aspected_houses` are whole-sign. A consumer joining
those houses against the snapshot's Placidus cusps silently mixes house systems, and nothing on
the model records which convention the houses use.

**M-05. Transit events carry no provenance object.** `TransitEvent` carries `profile_name` as a bare
string: no ayanamsa mode, node policy, ephemeris mode or time basis. `TransitView` validates the
natal provenance and then discards it, so the returned object cannot say which natal chart it is
relative to. Two facts from these modules cannot be safely joined by a convergence layer, which is
precisely what the provenance model exists to prevent.

**M-06. Profile guarding is inconsistent across layers.** Drishti checks profile name and ayanamsa
mode. The transit view checks name only. `find_crossings`, `returns` and `natal_conjunctions` check
nothing and accept bare float natal longitudes, so a Lahiri natal Sun can be passed under a
Krishnamurti profile and yield a solar return about six hours off. The methodology-isolation rule is
enforced on the view but not on the primary event API.

**M-07. `provenance.ephemeris_mode` is asserted rather than observed.** The real mode returned by the
checked call is discarded, and houses and ayanamsa get no return-flag inspection at all.
`docs/ENGINE_STATUS.md` describes the kernel as running strict Swiss Ephemeris with return-flag
inspection, which is accurate for planets and over-broad for the snapshot as a whole.

**M-08. `VargaClassification.d_sign` is undeclared in the sign-convention completeness gate.** The
framework's authoritative output sits in the gate's blind spot.

**M-09. D1 and the varga layers disagree about the source sign inside the `1e-10` window.**
Documented as pre-existing locked behaviour and never resolved. Both sign-convention gates step
around it by probing at `+0.0007`, described in the code as off exact boundaries by design. A gate
that avoids a known inconsistency is not evidence about it, and this seam is exactly where the
convergence layer will have to join D1-derived and varga-derived facts.

**M-10. The varga boundary arithmetic has no independent external attestation.** All root validators
import `classify` from production as the subject and independently re-derive only the table. The
PyJHora oracle is deliberately probed at midpoints. Two validators copy the implementation's
`+1e-10` verbatim into the supposedly independent reference. The tables are independently certified;
the boundary arithmetic is verified against itself. Porting the existing exact-rational reference
from the D1 primitives to the varga classifier would close this cheaply.

**M-11. Transit events at exact window endpoints are silently dropped.** The docstring documents a
closed interval, but a zero difference at the start sample causes the piece to be skipped. Measured:
a solar return window starting exactly at birth loses the birth-instant event, and moving the window
start back by 0.001 day recovers it. A dead branch in the code shows the author saw the case and
left it unhandled with a comment that misdescribes the outcome.

**M-12. The transit certifier's advertised completeness gate does not exist.** The runner docstring
and ADR-0008's evidence block both cite completeness against an independent fine scan, but the file
contains no such gate function and the artifact's gate keys are residual, oracle and validator only.
The pinning test does not notice.

**M-13. The drishti oracle gate tests only integer arithmetic.** The oracle's input is constructed
from our own placements, so from that point both sides are pure integer arithmetic on identical
input. Eleven holdout charts spanning six continents contribute eleven integer permutations; any one
of them would have caught a wrong offset, and eleven add no power over one. Separately, the aspect
offset numbers are transcribed four times inside the repository and validated against a classical
source zero times, and `aspected_houses` is discarded by the oracle comparison entirely.

**M-14. `LOCK_MANIFEST.json` has no KP_CHAIN entry** although ADR-0006 explicitly requires one.

---

## LOW

L-01 Fabricated ascendant speed: KP charts hardcode `speed_longitude=0.0` for the Ascendant in a
model documented as facts only; the ascendant moves at roughly 360 degrees per day. L-02 `kp_chain`
silently accepts strings and booleans through the lenient `Decimal` conversion, and raises three
different unhandled exception types for NaN, infinity and None. L-03 `seed_moon_longitude` records
the un-normalised input, so a consumer cannot reproduce the classification from the provenance
field. L-04 `depth` accepts `True` because `True == 1`. L-05 Stale Phase A claims in four production
docstrings assert the registry is empty, contradicted by five shipped vargas. L-06 `varga_rules.py:9`
claims `CyclicVargaRule` covers D3, contradicted three times elsewhere. L-07 Duplicated boundary
tolerance literals in three modules, with D9 and D10 using different float operations that agree
today but need not for a future width. L-08 Two near-vacuous assertions in the D7/D30/D2 boundary
battery whose disjunctions pass for almost any input. L-09 `natal_conjunctions` returns a shape
asymmetric with every sibling and loses the natal label when events are taken alone. L-10 Redundant
grid rebuilds make multi-target transit scans about twenty-seven times more expensive than needed,
which will dominate any backtesting or BTR sweep. L-11 The eleven-case matrix is duplicated in two
files with no drift guard. L-12 `find_crossings` does not enforce its own residual bound at runtime.

---

## What was checked and found clean

Stated explicitly so these are not re-litigated. Vimshottari exact hierarchical sums at every level,
exact float-JD contiguity and nesting across all 819 periods, chronological ordering, 120-year
closure, lord-cycle wraparound, nakshatra-boundary continuity, determinism, and absence of Moshier
fallback at the ephemeris range edges. PyJHora's ayanamsa mode does not leak into the engine, because
both engine paths set the sidereal mode explicitly before every computation, so interleaving oracle
and engine calls in a certifier is safe. The node-cast aspect exclusion in drishti is airtight: no
node can enter the caster set. `aspected_signs` is exhaustively correct over all 84 pairs. Transit
completeness held over one hundred randomised targets for all shipped bodies under both shipped
profiles. The KP interval walk's fall-through is genuinely unreachable under exact rational
arithmetic. No fitted constants or per-case corrections were found. No cross-school imports were
found. No production code imports `legacy/`. The KP and engine nakshatra name spellings differ but
are compared by index, which is correct and is the reason the divergence is invisible.

---

## Assessment

The exact-rational cores of these layers are, as far as this audit could test them, correct. The
deficits cluster in three places, and the pattern is consistent enough to be worth naming.

**First, gates that cannot fail.** H-03 is the clearest case: a tolerance derived from the quantity
it is meant to bound. B-03 and M-03 are the same species. A gate that passes by construction is
worse than no gate, because it is counted as evidence.

**Second, seams.** H-02, H-08, M-09 and M-04 are all defects that live between two individually
correct, individually certified layers. No certification spans a seam, and the convergence layer is
made entirely of seams.

**Third, claims outrunning evidence.** H-04, M-01, M-12 and M-13 are all cases where a document
states something the artifact does not establish. This is the same class as audit finding B-3, which
G1 exists to close, and it suggests the class is systemic rather than incidental.

None of this undermines the calculation work, which remains the strongest part of the project. It
does mean the certification vocabulary should be applied more conservatively than the current
documents apply it, and it argues for the C0 to C5 taxonomy landing sooner rather than later, since
several of these components are described in absolute terms that a graded vocabulary would have
prevented.
