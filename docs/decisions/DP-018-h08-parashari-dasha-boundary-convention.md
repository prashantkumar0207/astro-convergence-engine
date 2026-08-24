<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ADDRESSED by ADR-0071** (2026-08-22) - owner ratified Option 3 (ratify the status quo + add an additive convention-disclosure field). This paper's own text is unedited below as the options record, apart from one placeholder-identifier correction (see the change history); see `ADR-0071` for the ratifying instruction and implementation record. |
| Version | 1.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-22 |
| Review cadence | TBD |

# DP-018. H-08: the KP exact-boundary conversion rule is exported into the Parashari-labelled dasha
seed - which convention should a Parashari-seeded dasha follow?

## 1. The question

`docs/DASHA_CERTIFICATION_ROADMAP.md` section 5 names H-08 as step 4 of the six JATAKA-entry
prerequisites (`Q8_CLOSURE_MATRIX.md` s5: "The Dasha roadmap's steps 1 to 6 complete... the H-08
convention decision"). Steps 1-3 (H-04, H-05, H-06) are already closed (`ADR-0053`, `ADR-0069`,
`ADR-0070`). This paper is the decision-readiness work for step 4, authorized by the owner's explicit
"Authorize H-08 decision-readiness as the next Dasha/Jataka-entry prerequisite" instruction, following
`DASHA_CERTIFICATION_ROADMAP.md`'s own established order. Unlike H-04/H-05/H-06, the roadmap's own text
is explicit that this step is different in kind: "Decide H-08, which is an owner decision about which
convention a Parashari-seeded dasha follows, **not a builder choice**." This paper investigates the
exact problem, what governs it today, and the legitimate conventions the owner could choose between -
it does not implement anything, does not choose a convention, and does not authorize M-02, the dasha
boundary-proximity indicator, or any JATAKA implementation.

## 2. What is already established, and what is not

**Established (direct citation and direct code/test inspection this session, not re-derived from the
roadmap document alone):**

- `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-08, quoted in full: "`engine/dasha/vimshottari.py:59-62`
  is a third copy of the KP `Decimal(str(x))` conversion rule, and `test_vimshottari_consistency.py:41-53`
  deliberately binds the dasha seed to `kp_chain` including at exact boundaries. Consequence, verified: at
  six float spellings of nakshatra boundaries a **Parashari-seeded** timeline disagrees with the engine's
  own Parashari `nakshatra()` about which nakshatra the Moon occupies, and therefore about the entire
  mahadasha sequence. A chart display and its dasha table can disagree. ... The KP layer's differing
  convention is documented and deliberate. Its export into a Parashari-facing layer is not documented
  anywhere." Behavioural impact per the audit: "Confined to a `1e-10` degree window, so no realistic
  chart is affected. The architectural point stands regardless: this is a school-isolation leak, and
  school isolation is a charter non-negotiable." Certification impact per the audit: "None of the three
  layers is individually wrong. No gate spans them." Proposed solution: "An owner decision on which
  convention a Parashari-seeded dasha follows, recorded in an ADR, then a pinning test that makes the
  choice explicit and visible." Tests required: "A cross-layer convention test enumerating the divergent
  boundaries, which the KP specification already promises and which does not exist."
- **The claim independently reproduced live against the current tree, unchanged since the audit, at the
  audit's own exact reported cardinality:** `engine/dasha/vimshottari.py`'s `_to_exact()` converts any
  float Moon longitude via `Fraction(Decimal(str(value)))` with exact `[start, end)` boundary ownership -
  the identical rule and cardinality contract as `engine/kp/intervals.py`'s `to_exact()`, used regardless
  of which school (`parashari_lahiri` or `kp_krishnamurti`) seeded the timeline. `engine/astrology/
  nakshatra.py`'s `nakshatra()` (the Parashari engine's own classifier, used for chart display and every
  other Parashari division classification) instead calls `division_index()` from `engine/astrology/
  longitude_utils.py`, which promotes a float within `1e-10` degrees *below* a boundary *up* to it - a
  materially different rule, deliberately introduced project-wide to absorb ephemeris float noise
  (documented in `longitude_utils.py`'s own module docstring, remediating findings F-04/A-3). Constructed
  directly this session: iterating `moon = float(NAK_SPAN * k)` for `k` in `0..26` (the literal boundary
  floats, exactly the construction `test_seed_agrees_with_certified_kp_chain_everywhere()` already uses)
  and comparing `nakshatra(moon)` against `vimshottari_from_moon(moon, ...).seed_nakshatra_number` for
  each - **exactly six mismatches**, at `k = 7, 11, 14, 17, 22, 25` (moon longitudes 93.333..., 146.666...,
  186.666..., 226.666..., 293.333..., 333.333... degrees), each off by exactly one nakshatra (the dasha
  seed reports the classifier's number minus one - the dasha layer treats the boundary as belonging to
  the interval starting there, the classifier's tolerance promotion pushes the float up into the same
  interval from the far side, disagreeing about which side of the true rational boundary the IEEE-754
  double actually lands on for these six specific spellings of `k * 360/27`). This is the audit's own
  reported cardinality reproduced exactly, not merely a plausible re-derivation. (A broader synthetic
  probe using floats deliberately placed a fixed tiny distance below every one of the 26 non-zero
  boundaries produces mismatches at all 26 - confirming the divergence mechanism generalizes across every
  boundary, but only six of the *specific* floats that `float(k * 360/27)` naturally produces in IEEE-754
  double precision happen to fall inside the `1e-10` promotion window; the audit's "six" figure is
  therefore about which naturally-occurring float spellings trigger it, not a claim that only six
  boundaries are structurally at risk.)
- **`test_seed_agrees_with_certified_kp_chain_everywhere()` (`engine/tests/
  test_vimshottari_consistency.py:41-52`) is the committed test that locks in today's behaviour as
  deliberate, not accidental**, confirmed by direct reading: its own docstring states "Same conversion
  rule and [start, end) ownership as the KP layer, so seeding must agree with the certified chain
  INCLUDING at exact boundaries" and asserts this for `vimshottari_from_moon()` regardless of which school
  would call it - the function is school-agnostic; `school` is recorded as metadata after the fact, never
  consulted for classification. The companion test, `test_seed_agrees_with_engine_nakshatra_off_
  boundaries()`, only checks agreement with the Parashari classifier at points offset `+0.001` degrees
  from every boundary - deliberately avoiding the boundary itself, confirmed by direct reading of its own
  loop (`moon = i * (360.0 / 997) + 0.001`). **No test anywhere checks agreement between the dasha seed
  and the Parashari classifier at or near a boundary** - the audit's "no gate spans them" claim confirmed
  directly, not merely asserted.
- **`certification/VIMSHOTTARI_V1_certification.json`'s `explicit_non_claims` does NOT mention this seam
  at all** (confirmed by direct read: it lists only "other dasha systems," "depths beyond
  pratyantardasha," "year conventions other than the certified profile," and "transit or event
  overlays"). This is a materially different starting position from H-06, where the certification
  artifact's own documentation was already accurate and only the code enforcement was missing - here,
  **neither the code nor the certification artifact's documented scope currently acknowledges the seam
  exists.**
- **`docs/KP_CHAIN_SPEC.md` s7 (Risks and mitigations) already anticipated a closely related but distinct
  problem** at KP's own original design time: "The engine float nakshatra index and the KP rational
  nakshatra index could disagree at ULP boundary points; a documented test pins down exactly where and
  why, so the difference is a recorded convention, never a surprise." This promised test is the subject
  of audit finding **M-01** ("The promised KP convention-divergence pinning test does not exist"), which
  is about the KP layer's own boundary relationship to the engine-wide classifier in general - a sibling
  finding to H-08, not the same one, and **not** in the Dasha roadmap's six-step list or in
  `Q8_CLOSURE_MATRIX.md` s5's JATAKA entry criteria. This paper is scoped to H-08 only; M-01 is not
  addressed, opened, or closed by anything here.
- **No prior ADR or decision paper addresses H-08.** Confirmed by direct search of `docs/
  DECISION_LOG.md` and `docs/decisions/` for "H-08": only citations noting it remains open (including
  this session's own `DP-016` and `DP-017`, which explicitly deferred it).
- **`VimshottariTimeline` (`engine/models/dasha.py`) has no field recording which boundary convention
  produced `seed_nakshatra_number`** - confirmed by direct reading of the full dataclass. `school` records
  only which astronomy profile seeded the Moon, never which classification rule was applied to it. This
  is the same structural absence `ADR-0065` found and additively remedied for the H-02 seam
  (`TransitEvent.declared_division`) - noted here as a candidate precedent, not yet applied.
- **H-05 and H-06 do not interact with H-08.** Confirmed directly, not assumed: `ADR-0069`'s H-05 fix
  (the hermetic anchor baseline, `engine/tests/test_vimshottari_hermetic_baseline.py`) freezes
  `anchor_jd` values for five seed cases, none of which lie on a nakshatra boundary (verified: none of
  the five seed Moon longitudes used equal any `k * 360/27`). `ADR-0070`'s H-06 fix (`validate_dasha_
  profile()`) guards `DashaProfile` identity and `year_length_days` type, an orthogonal axis to boundary
  classification. Neither is reopened, touched, or put at risk by anything investigated in this paper.

**Not established (explicitly not decided by this paper):** which boundary convention a Parashari-seeded
dasha should follow; whether `vimshottari_from_moon()` becomes school-aware for classification purposes;
whether `test_seed_agrees_with_certified_kp_chain_everywhere()`'s current universal claim is narrowed to
KP-seeded calls only; whether an additive convention-disclosure field is added to `VimshottariTimeline`.

## A. The exact H-08 problem

`vimshottari_from_moon()` classifies the seed nakshatra using the KP layer's exact `[start, end)`
boundary-ownership rule (`Decimal(str(x))`, no tolerance) for every timeline it produces, regardless of
which school's profile seeded it. The engine's own Parashari-facing classifier (`nakshatra()`, used for
chart display and every other Parashari division classification) uses a materially different rule (a
`1e-10`-degree tolerance-promotion, introduced project-wide for a different purpose: absorbing ephemeris
float noise). At six specific, independently-reproduced float spellings of nakshatra boundaries, a
Parashari-seeded dasha timeline's `seed_nakshatra_number` - and therefore its entire mahadasha lord
sequence - disagrees with what the engine's own Parashari `nakshatra()` function would report for the
identical Moon longitude. This is committed, deliberate behaviour (locked in by `test_seed_agrees_with_
certified_kp_chain_everywhere()`'s own explicit "including at exact boundaries" assertion) that was never
documented as a cross-school leak, never disclosed in the certification artifact's scope, and never
decided by an ADR.

## B. Classification

**A convention ambiguity exported across a school-isolation seam - not a calculation defect, not a
missing protection, and (per the audit's own explicit statement) not currently a certification gap in
the sense of an unverified claim, since no certified claim currently promises cross-classifier agreement
at boundaries.** Three genuinely separate aspects, worth keeping distinct:

1. **Convention ambiguity (the core of it):** two individually correct, individually documented, and (for
   KP) individually deliberate boundary-ownership rules exist in this codebase for good, separate reasons
   (KP's rule preserves bit-exact legacy-kernel equivalence under `DECISION_LOG D-003`; the engine-wide
   `1e-10` rule absorbs a different, real problem - float noise from ephemeris/trigonometric computation).
   Neither rule is "wrong." The question is which one a *Parashari-labelled* dasha timeline should use for
   its own seed classification, and that answer is not implied by either rule's own certification.
2. **A documentation gap, mirroring H-08's own audit framing exactly:** "The KP layer's differing
   convention is documented and deliberate. Its export into a Parashari-facing layer is not documented
   anywhere" - and this paper additionally confirms the certification artifact's `explicit_non_claims`
   does not disclose it either, a gap H-06's own artifact did not have.
3. **A missing test-coverage gap:** no gate, holdout, or pinning test anywhere currently exercises
   agreement (or documents disagreement) between the dasha seed and the Parashari classifier at or near a
   boundary - confirmed directly, not merely asserted by the audit.

Per the roadmap's and the audit's own framing, resolving (1) is explicitly **not a builder decision** -
it requires the owner to state which convention a Parashari-seeded dasha follows. (2) and (3) are
mechanical consequences of whichever answer (1) receives.

## C. All legitimate treatment options

### Option 1 - Ratify the status quo explicitly: Parashari-seeded dasha keeps the KP exact-boundary rule,
project-wide, for all schools; document and pin it

Record an ADR stating that `vimshottari_from_moon()`'s single, uniform `Decimal(str(x))` exact-boundary
conversion rule is the deliberate VIMSHOTTARI_V1 dasha-seeding convention for every school, including
Parashari - not an accidental leak. Add the audit's own required pinning test: a new test enumerating the
six divergent boundary floats found this session (or all reachable ones), asserting the *disagreement*
with `nakshatra()` explicitly, so the difference is a recorded, visible convention rather than an
undocumented surprise. Add the missing disclosure to `certification/VIMSHOTTARI_V1_certification.json`'s
`explicit_non_claims` ("dasha seed classification at a nakshatra boundary may differ from the engine's
general-purpose Parashari classifier by design; see the ratifying decision-log entry"). Optionally update `engine/dasha/
vimshottari.py`'s own module docstring and `docs/KP_CHAIN_SPEC.md` s7's already-partially-written
rationale to cross-reference this specific instance.

- **Rationale available to support this option:** dasha-period arithmetic is exact-rational throughout
  (`Decision DA-A`/`DA-C`) and directly consumes the seed classification to derive every subsequent
  boundary; an exact, tolerance-free ownership rule is arguably the *more* appropriate convention for a
  layer whose entire certified value proposition is "exact rational arithmetic throughout," even though it
  differs from the tolerance-promoted rule a chart-display classifier uses for an unrelated reason (noise
  absorption on general ephemeris output, not exactness preservation).
- **Certification implications:** none - this is additive test/documentation coverage only, matching
  H-05's and H-06's own precedent exactly. No `certify_vimshottari.py` change, no schema change.
- **Blast radius:** `docs/DECISION_LOG.md` (new ADR), `engine/tests/` (one new pinning test file or an
  addition to an existing one), `certification/VIMSHOTTARI_V1_certification.json` (`explicit_non_claims`
  addition, a metadata-only field), optionally `engine/dasha/vimshottari.py`'s docstring. No production
  calculation logic changes.
- **Certified-value impact:** **none.** No existing certified Vimshottari value changes under this option
  - the six divergent floats already compute exactly what they compute today; this option only makes that
  fact explicit and tested.

### Option 2 - Make Parashari-seeded dasha follow the Parashari engine's own tolerance-promoted convention

Change `vimshottari_from_moon()` (or a school-aware wrapper around it) so that when the seeding school is
`parashari`, seed nakshatra classification routes through the same `division_index()`/`nakshatra()`
tolerance-promoted rule the rest of the Parashari engine uses, rather than the KP-style exact rule -
guaranteeing a Parashari-labelled chart's own classifier and its own dasha table always agree. KP-seeded
timelines keep today's exact rule untouched.

- **Rationale available to support this option:** arguably more faithful to "school-explicit seeding"
  (`Decision DA-B`) than the status quo - today's code silently uses the KP school's own boundary
  convention for a Parashari-labelled artifact, which is precisely the kind of school-isolation leak the
  charter treats as non-negotiable, per the audit's own words.
  Directly closes the audit's "chart display and its dasha table can disagree" complaint rather than only
  documenting it.
- **Certification implications:** a genuine, though narrowly scoped, certified-value change: the six
  known floats (and the wider boundary-adjacent range the broader synthetic probe found) would produce a
  *different* `seed_nakshatra_number` (and therefore a different mahadasha lord sequence) for
  Parashari-seeded timelines than they do today. This requires `certify_vimshottari.py` re-running against
  the oracle to confirm the *new* behaviour still agrees with PyJHora's own boundary handling for Parashari
  charts (not yet checked - PyJHora's own convention at these specific floats is currently unknown and
  would need investigation before this option could be certified, not merely implemented), plus a
  `VIMSHOTTARI_V1` certification-artifact update reflecting the changed scope.
  Real-world behavioural impact is likely still small (an ephemeris-derived Moon longitude essentially
  never lands bit-exactly on a rational `k * 360/27` float), but that is a probabilistic argument, not a
  certification substitute - if chosen, the change must go through the standard certified-value-change
  process, not be waved through on low-probability grounds.
- **Blast radius:** `engine/dasha/vimshottari.py` (a school-conditional branch in classification, a more
  invasive change than Option 1's additive test), `engine/tests/test_vimshottari_consistency.py`
  (`test_seed_agrees_with_certified_kp_chain_everywhere()`'s own "including at exact boundaries" premise
  would need to be rescoped to KP-seeded calls specifically, since it would no longer hold universally -
  editing an existing, currently-passing certified-tier test, not merely adding one), `certification/
  VIMSHOTTARI_V1_certification.json` (recertification), `docs/DECISION_LOG.md` (new ADR).
- **Certified-value impact:** **yes, for Parashari-seeded timelines at the affected boundary floats.**
  Zero impact for KP-seeded timelines (untouched).

### Option 3 - Option 1's zero-impact core, plus an additive convention-disclosure field (hybrid)

Do everything in Option 1 (ratify the status quo, pin it, document it), and additionally add a new,
purely additive field to `VimshottariTimeline` (or its provenance) recording which boundary-ownership
convention produced `seed_nakshatra_number` - mirroring `ADR-0065`'s own remediation of the structurally
similar H-02 seam (`TransitEvent.declared_division`): rather than forcing two individually-correct layers
into agreement, make the layer that could disagree say explicitly which rule it used, so a downstream
consumer (a chart-display layer, a BTR convergence check) can detect and reconcile the seam itself instead
of discovering it silently.

- **Rationale available to support this option:** this repository has an established, owner-accepted
  precedent for exactly this shape of problem (`DP-013`/`ADR-0065`) - two individually correct,
  individually certified layers disagreeing at a seam, resolved by additive disclosure rather than by
  forcing one layer to defer to the other. Preserves Option 1's zero-certified-value-impact property while
  giving future consumers (M-02's near-boundary work, the not-yet-built boundary-proximity indicator, or a
  future EVIDENCE/INTERPRETATION-layer consumer) a documented, machine-readable hook rather than only a
  prose ADR.
- **Certification implications:** none beyond Option 1's - the new field is descriptive metadata, not a
  changed calculation; existing certified values are untouched, matching the reasoning already established
  for `ADR-0065`'s own `declared_division` field (additive, default-populated, no existing consumer
  affected).
- **Blast radius:** Option 1's blast radius, plus `engine/models/dasha.py` (one new field, additive
  default) and `engine/dasha/vimshottari.py` (populate it at the point of classification). Slightly larger
  than Option 1 alone but still no calculation-logic change.
- **Certified-value impact:** **none** - identical to Option 1 in this respect; the addition is purely
  descriptive.

### Option 4 - Defer

Leave H-08 undocumented and untested, as today, and record an explicit deferral decision instead of a
fix.

- **Advantages:** zero implementation cost.
- **Disadvantages:** unlike H-05/H-06's own deferral analyses, this option has a **weak** cost/benefit
  case: Option 1 (the audit's own proposed solution) is a documentation-and-test-only change with zero
  certified-value impact and no genuine implementation complexity - there is little the owner saves by
  deferring it that Option 1 does not already provide at negligible cost. `Q8_CLOSURE_MATRIX.md` s5's own
  wording names "the H-08 convention decision" as one of six required steps, a plain, non-alternative
  list (the same textual structure `DP-016`/`DP-017` already confirmed gives no `DP-015`-style carve-out
  opening) - deferring does not close that prerequisite, so the decision is needed before JATAKA entry
  regardless of when it is made.
- **Certification implications:** none.
- **Blast radius:** none.
- **Certified-value impact:** none.

## D/E. Certification implications and blast radius

Stated inline under each option in section C. Options 1, 3, and 4 change no certified value. Option 2 is
the only option with a genuine (narrowly-scoped, Parashari-only, boundary-float-only) certified-value
change, and would require oracle re-verification of PyJHora's own Parashari boundary handling before
certification - not yet investigated, out of scope for this decision-readiness paper.

## F. Whether existing certified dasha values change under each option

**No, under Options 1, 3, or 4.** The six affected floats (and any others the broader boundary geometry
admits) continue to compute exactly what they compute today; nothing in `VIMSHOTTARI_MEAN_SIDEREAL_YEAR`'s
own certified arithmetic path is touched.

**Yes, under Option 2, but only for Parashari-seeded timelines at the specific floats where the two
conventions disagree** - confirmed directly this session (the six reproduced mismatches), not merely
inferred from the audit's own count.

## G. Recommendation

**Option 1, or its Option 3 enhancement, at medium-high confidence.** Reasoning: (i) the audit's own
proposed solution is explicitly "an owner decision... recorded in an ADR, then a pinning test" - which
maps directly onto Option 1's action, not Option 2's; (ii) Option 2 would be the first change in this
entire H-04/H-05/H-06/H-08 sequence to actually alter a certified calculated value, which the roadmap
itself flags as a materially higher-cost, higher-scrutiny action ("Steps 1 through 6 change no calculated
value" is the roadmap's own stated design intent for this phase of work); (iii) Option 2's own
justification (school-isolation purity) is real but must be weighed against reopening a currently-green,
committed, deliberately-written test (`test_seed_agrees_with_certified_kp_chain_everywhere()`) whose own
docstring frames today's behaviour as intentional; (iv) Option 3's additive disclosure field is a
close-to-free enhancement with a direct, already-owner-accepted precedent in this exact repository
(`ADR-0065`) and would materially help the still-unbuilt M-02 and boundary-proximity-indicator steps that
follow H-08 in the same roadmap. Option 2 remains fully legitimate if the owner's priority is
classifier/dasha display consistency over exactness-purity for the Parashari school specifically - the
evidence does not rule it out, it only costs more to certify.

**Confidence: medium-high.** Stronger than `DP-017`'s own H-06 lean, because unlike H-06's two genuinely
open implementation sub-questions, H-08's zero-impact option (Option 1) has almost no design space left
open by the audit's own proposed solution - the only real judgment call is whether to add Option 3's
disclosure field, which is itself a directly precedented, low-risk addition.

## H. What is NOT being decided by this paper

Which convention a Parashari-seeded dasha follows; whether `vimshottari_from_moon()` becomes
school-aware; whether the currently-committed `test_seed_agrees_with_certified_kp_chain_everywhere()` is
rescoped; whether a convention-disclosure field is added to `VimshottariTimeline`; whether
`certification/VIMSHOTTARI_V1_certification.json` is amended. M-02, the dasha boundary-proximity
indicator, and any JATAKA implementation are untouched and not addressed. M-01 (the sibling KP-layer
pinning-test finding, not part of the Dasha roadmap's six steps) is not addressed. `DP-016`/H-05,
`DP-017`/H-06, FOUNDATION, and every already-closed FOUNDATION item remain exactly as ratified - none is
reopened or reconsidered by this paper.

## I. Exact CEO/owner decision required

Select Option 1 (ratify the status quo, document and pin it - zero certified-value impact), Option 2
(make Parashari-seeded dasha match the Parashari engine's own classifier - a genuine, narrowly-scoped
certified-value change requiring oracle re-verification before it could be certified), Option 3 (Option
1 plus an additive convention-disclosure field, mirroring `ADR-0065`'s own precedent), or Option 4
(defer - weak cost/benefit case given Option 1's near-zero cost) for H-08. Recorded as a new, numbered
decision-log entry citing this paper - this paper alone authorizes nothing, and does not authorize M-02,
the dasha boundary-proximity indicator, or any JATAKA implementation.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-08-22 | Marked ADDRESSED by `ADR-0071` (Option 3 accepted and implemented: status quo ratified + `SEED_BOUNDARY_CONVENTION_KP_EXACT` disclosure field + pinning test). One placeholder decision-identifier token in section C's Option 1 text (which `engine/tests/test_retired_identifier_gate_scope.py` correctly caught as a genuine identifier-family violation) corrected to non-identifier-shaped prose - a mechanical fix, not a substantive edit; the paper's options, evidence, and recommendation are otherwise exactly as drafted. |
| 1.0.0 | 2026-08-22 | Created. Third authorized JATAKA-entry-prerequisite decision-readiness paper, extracting `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`'s H-08 finding and `docs/DASHA_CERTIFICATION_ROADMAP.md` step 4, with every claim independently re-verified against the live `engine/dasha/vimshottari.py`, `engine/astrology/nakshatra.py`/`longitude_utils.py`, `engine/kp/intervals.py`, the committed consistency tests, and the certification artifact's own `explicit_non_claims` - not trusted from the audit's own summary. Independently reproduced the audit's own reported cardinality exactly (six divergent boundary floats at the literal `float(k * 360/27)` spellings), and additionally characterized the broader boundary geometry (all 26 non-zero boundaries diverge under a fixed-offset synthetic probe, clarifying the audit's "six" figure is about naturally-occurring float spellings, not a claim of only six at-risk boundaries). Classifies H-08 as a convention ambiguity across a school-isolation seam, combined with a documentation gap and a test-coverage gap - not a calculation defect. Confirmed no interaction with H-05 (`ADR-0069`) or H-06 (`ADR-0070`); neither reopened. Presents four options (ratify status quo + pin; change Parashari seeding to match its own classifier; the first option plus an additive disclosure field mirroring `ADR-0065`'s H-02 precedent; defer), medium-high-confidence lean toward the zero-impact options (1 or 3). Options only; decides nothing; not implementation-authorized. |
