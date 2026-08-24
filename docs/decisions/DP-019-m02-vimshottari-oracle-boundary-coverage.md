<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ADDRESSED by ADR-0072** (2026-08-24) - owner ratified Option 1 (root-find genuine oracle-gate cases; correct the mislabeled cases). This paper's own text is unedited below as the options record; see `ADR-0072` for the ratifying instruction and implementation record. |
| Version | 1.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-24 |
| Review cadence | TBD |

# DP-019. M-02: the Vimshottari oracle gate's two cases named "boundary_moon" are not boundary cases -
should genuine near-boundary Moon coverage be added?

## 1. The question

`docs/DASHA_CERTIFICATION_ROADMAP.md` section 5 names M-02 as step 5 of the six JATAKA-entry
prerequisites (`Q8_CLOSURE_MATRIX.md` s5: "near-boundary Moon cases" is the fifth of six required
steps). Steps 1-4 (H-04, H-05, H-06, H-08) are already closed (`ADR-0053`, `ADR-0069`, `ADR-0070`,
`ADR-0071`). This paper is the decision-readiness work for step 5, authorized by the owner's explicit
"Authorize M-02 decision-readiness as the next Dasha/Jataka-entry prerequisite" instruction, following
`DASHA_CERTIFICATION_ROADMAP.md`'s own established order. It investigates the exact problem, what
governs it today, and the legitimate treatment options - it does not implement anything, does not choose
an option, and does not authorize the dasha boundary-proximity indicator or any JATAKA implementation.

## 2. What is already established, and what is not

**Established (direct citation and direct code/data inspection this session, not re-derived from the
roadmap document alone):**

- `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` M-02, quoted in full: "The Vimshottari certification's
  two named boundary cases are not boundary cases. Measured Moon distance to the nearest nakshatra
  boundary: 6.46 degrees and 5.0 degrees. Both are farther from a boundary than a case not labelled as
  one. The oracle gate contains zero near-boundary Moon cases, in the layer where boundary proximity has
  the largest downstream effect."
- **The claim independently reproduced live against the current tree, unchanged since the audit, at the
  audit's own exact reported precision:** `scripts/certify_vimshottari.py`'s `HOLDOUT` list names eleven
  cases; two are explicitly labelled `H10_boundary_moon_a` (2025-03-01, Delhi) and `H11_boundary_moon_b`
  (2025-03-02, Delhi). Computed this session, through the same `engine.calculations.calculations.
  calculate()` path the certifier itself uses (`PARASHARI_LAHIRI` profile): `H10`'s sidereal Moon is
  339.79199 degrees, **6.4587 degrees** from the nearest nakshatra boundary (`NAK_SPAN = 360/27`);
  `H11`'s is 351.68640 degrees, **5.0197 degrees** from the nearest boundary - matching the audit's "6.46
  degrees and 5.0 degrees" exactly. Computed the same distance for all nine other holdout cases (`H1`
  through `H9`): every one of them is closer to a boundary than `H10` (6.4587 deg); eight of the nine are
  closer than `H11` (5.0197 deg) as well - only `H6_quito_2010` (5.5014 deg) is farther than `H11`, and
  it is still closer than `H10`. This independently confirms the audit's "both are farther from a
  boundary than a case not labelled as one" claim precisely, not merely by name-matching: the two cases
  whose names promise boundary-adjacent Moon positions are, in fact, near the *median* boundary distance
  of the entire holdout set, and `H10` specifically is the single farthest-from-any-boundary case in the
  whole gate.
- **No case anywhere in the current oracle gate, hermetic-tier tests, or independent validator is
  genuinely near a nakshatra boundary.** Confirmed by direct search: `engine/tests/
  test_vimshottari_hermetic_baseline.py`'s five H-05 seed cases (`ADR-0069`) were frozen for anchor-JD
  regression coverage, not boundary proximity - none of their seed Moon longitudes is within even one
  degree of a boundary (checked directly this session). `engine/tests/
  test_vimshottari_h08_boundary_convention.py`'s six pinned floats (`ADR-0071`) are exactly *on* the
  boundary by synthetic construction (`float(k * 360/27)`), which is a different, deliberately
  degenerate case (testing the boundary-ownership *rule itself*, at floats no real ephemeris Moon will
  ever land on bit-exactly) - not a substitute for a *realistic* near-boundary case reachable from actual
  birth data, which is what M-02 and the roadmap's own step-5 wording ("near-boundary Moon cases")
  actually call for.
- **A directly relevant, already-certified mechanism exists in this repository for locating a real
  instant at which the Moon crosses an exact target longitude:** `engine.transits.crossing.
  find_crossings()` (`TRANSIT_V1`, `ADR-0008`). Verified live this session:
  `find_crossings("Moon", NAK_SPAN * 5, jd_start, jd_end, PARASHARI_LAHIRI)` over a one-month window
  found one crossing, at `residual_arcsec` of about `1.0e-6` arcsec - a root-found instant where the real
  ephemeris Moon is, to sub-microarcsecond precision, exactly on a nakshatra boundary. The Moon crosses
  each of the 27 nakshatra boundaries roughly once per sidereal month (~27.3 days), so a full year's
  window yields on the order of a dozen crossings per boundary, more than enough candidate instants to
  build genuine near-boundary holdout cases from.
- **No prior ADR or decision paper addresses M-02 directly.** Confirmed by direct search of `docs/
  DECISION_LOG.md` and `docs/decisions/` for "M-02": only citations noting it remains open, including
  `docs/decisions/DP-015-foundation-boundary-proximity-indicators.md`, which cites the audit's M-02
  finding as supporting evidence for a **different, related-but-distinct** roadmap item (the
  boundary-proximity *indicator*, `Q8_CLOSURE_MATRIX.md` s4's FOUNDATION-scope item and the Dasha
  roadmap's own separate step 6) - `DP-015` does not resolve, implement, or decide M-02 itself, and this
  paper does not reopen `DP-015`/`ADR-0067`.
- **`certification/VIMSHOTTARI_V1_certification.json`'s `explicit_non_claims` does not disclose the
  absence of near-boundary coverage.** Confirmed by direct read (current list, post-`ADR-0071`): "other
  dasha systems," "depths beyond pratyantardasha," "year conventions other than the certified profile,"
  "transit or event overlays," and the H-08 boundary-convention disclosure `ADR-0071` added. None of
  these states that the gate's boundary-case labels do not reflect genuine boundary proximity.

**Not established (explicitly not decided by this paper):** whether new near-boundary cases are added to
the oracle gate; whether `H10`/`H11` are corrected, renamed, or replaced; how many new cases, at how many
boundaries, on which side(s) of the crossing; whether `explicit_non_claims` is updated in the interim.

## A. The exact M-02 problem

Two of the Vimshottari oracle gate's eleven holdout cases are named to imply they exercise near-boundary
Moon behaviour (`H10_boundary_moon_a`, `H11_boundary_moon_b`). Neither one does: their actual Moon
longitudes are 6.46 and 5.02 degrees from the nearest nakshatra boundary respectively, farther from a
boundary than most of the gate's own ordinary (non-boundary-labelled) cases. The oracle gate - the only
gate in `VIMSHOTTARI_V1` that cross-checks this engine's dasha timeline mathematics against an
independent external computation (PyJHora) - therefore contains **zero cases that genuinely exercise
Moon-near-a-nakshatra-boundary behaviour**, in the one layer the audit identifies as having the largest
downstream sensitivity to boundary-adjacent Moon positions (dasha boundaries move by "hundreds of days
per degree" of Moon longitude error, per `docs/DASHA_CERTIFICATION_ROADMAP.md` s1).

## B. Classification

**Primarily an oracle/holdout coverage gap, with a secondary certification-label-accuracy defect - not a
calculation defect.** Two genuinely separate aspects:

1. **Coverage gap:** no case anywhere in the certified evidence chain (oracle gate, hermetic tests,
   independent validator) exercises a real, ephemeris-derived Moon position genuinely close to a
   nakshatra boundary. This is the primary finding, matching the audit's own framing ("the oracle gate
   contains zero near-boundary Moon cases").
2. **Label-accuracy defect:** the two existing cases are explicitly *named* to claim boundary coverage
   they do not provide - unlike a merely absent gate (which is honest about what it does not test),
   `H10`/`H11`'s names actively misstate what they test. This is a smaller, distinct problem from (1):
   even without adding any new coverage, correcting the misleading names would already remove a false
   claim from the certified evidence.

Neither aspect is a defect in `VIMSHOTTARI_MEAN_SIDEREAL_YEAR`'s own arithmetic, which the audit
confirms is not in question here - the certified computation itself is not implicated; the gap is
entirely in what the oracle gate's holdout set actually exercises.

## C. Whether existing certified Vimshottari values are affected

**No, under any option this paper considers.** Adding new holdout cases changes the gate's own `total_
rows`/`cases` counts and adds new per-case entries to `certification/VIMSHOTTARI_V1_certification.json`;
it does not change any existing case's own computed result, and it does not touch `VIMSHOTTARI_MEAN_
SIDEREAL_YEAR`'s certified year-length value, the exact-rational period arithmetic, or any of the
already-closed H-04/H-05/H-06/H-08 fixes. This matches the additive-evidence pattern already established
for H-05's hermetic baseline (`ADR-0069`) and H-08's pinning test (`ADR-0071`): new committed evidence,
zero change to any existing certified figure.

## D. Precedents checked (H-04, H-05, H-06, H-08) - applicable and not, explicitly

- **H-04** (the missing depth-3 oracle comparison, `ADR-0053`) is the closest precedent in *kind*: both
  are "a gate that should exist and does not." H-04's fix was to run the already-designed depth-3
  comparison and confirm it passes - a comparison the codebase already knew how to perform, just hadn't
  executed and gated on. M-02 differs: no near-boundary comparison methodology exists yet to simply
  "turn on" - genuinely new holdout cases must be located and constructed first. H-04's precedent applies
  to the *spirit* (close a documented-but-missing gate), not the mechanics.
- **H-05** (the hermetic tier's blind spot, `ADR-0069`) is the closest precedent in *remedy shape*: a new,
  frozen, protected set of cases added to close a coverage gap, with zero impact on existing certified
  values. But H-05's fix was **hermetic only** (an in-repository frozen baseline, no oracle
  re-verification required, because the values being frozen were already independently oracle-validated
  for their own anchor construction). M-02's own audit language and the roadmap's own step-5 wording both
  specifically call for coverage **in the oracle gate** - a stronger bar than H-05's own remedy met. This
  paper does not blindly reuse H-05's hermetic-only shape; section E below evaluates whether a
  hermetic-only remedy would actually satisfy M-02, or only partially address it.
- **H-06** (the missing profile allow-list, `ADR-0070`) and **H-08** (the boundary-convention seam,
  `ADR-0071`) are not close precedents for *remedy shape* - both were architectural/convention questions
  resolved by adding a guard or a disclosure field, not by adding new holdout data. Their relevance here
  is procedural only: both established this session's now-consistent pattern of independently
  reproducing the audit's own numbers before proposing options, which this paper's section 2 follows.
- **A more directly relevant precedent than any of H-04/H-05/H-06/H-08, not named by the owner's list but
  found by inspecting the codebase for "how has this project built genuine boundary coverage before":**
  `KP_CHAIN_V1`'s own Gate 1 ("51,429 dense + full boundary battery + ULP neighbors + adversarial
  spellings, zero mismatches," `docs/KP_CHAIN_SPEC.md`) and `TRIKALAM_V1`'s "exact-sunrise-boundary ULP
  battery with negative control" (`docs/ACE_EXECUTION_STATE.md` change history, v1.3.0) are both cases
  where this project built genuine near-boundary coverage by root-finding an exact boundary instant and
  then testing ULP-adjacent neighbours on both sides. Section E's Option 1 follows this established
  shape, not H-05's.

## E. All legitimate treatment options

### Option 1 - Root-find genuine near-boundary Moon instants and add them as new oracle-gate cases

Use the already-certified `engine.transits.crossing.find_crossings()` (`TRANSIT_V1`) to locate real
Julian Days, within a reasonable calendar window, at which the ephemeris Moon crosses one or more
nakshatra boundaries under `PARASHARI_LAHIRI` (and, separately, `KP_KRISHNAMURTI`, since the gate already
certifies both profiles). Construct new `HOLDOUT` entries at those instants (or at a fixed short offset
before/after the exact crossing, to exercise both sides of the boundary, mirroring `KP_CHAIN_V1`'s and
`TRIKALAM_V1`'s own "ULP neighbours on both sides" methodology), and let the existing `run_case()`
machinery cross-check them against PyJHora exactly as it does today - no change to the oracle-comparison
methodology itself, only to which instants are tested.

**Two genuinely open sub-questions this paper surfaces but does not resolve:**
- **How many boundaries, and how close.** Testing at the exact root-found crossing (sub-microarcsecond
  residual) verifies "exactly at a boundary"; testing at a small fixed offset on each side (a few
  arcseconds of Moon motion, translating to a few seconds of real time given the Moon's ~0.5 deg/hour
  motion) verifies "just inside" and "just outside." Both are needed to genuinely exercise the boundary,
  not just touch it once; how many of the 27 boundaries to sample (all of them, a representative subset,
  or the same six the H-08 pin already found interesting) is an implementation-time judgment call with no
  single objectively correct answer.
- **What happens to `H10`/`H11`.** They could be corrected (renamed to reflect what they actually test,
  since they are otherwise ordinary, valid, already-passing cases) and kept as ordinary coverage, or
  replaced outright by the new genuinely-boundary cases. Either resolves the label-accuracy defect in
  section B item 2; which one is a judgment call, not a technical necessity.

- **Certification implications:** additive only - new `cases` entries, a larger `total_rows`/`oracle_
  pratyantar_rows_compared` count, no schema change, no change to any existing case's own recorded
  result. Requires re-running `certify_vimshottari.py` against the PyJHora oracle (available only in the
  isolated exploration venv on this host, per the established Windows/Linux gate-parity note) to confirm
  the new cases genuinely PASS, not merely that they were added.
- **Blast radius:** `scripts/certify_vimshottari.py` (new `HOLDOUT` entries, and possibly a small,
  additive helper to compute a crossing-adjacent JD given a target boundary and window - test/certifier
  code only, no production module touched), `certification/VIMSHOTTARI_V1_certification.json` (new case
  entries via regeneration), optionally `explicit_non_claims` (removing or narrowing the now-closed gap).
  No change to `engine/dasha/`, `engine/astrology/`, or `engine/kp/`.
- **Certified-value impact:** **none** on any existing certified value - confirmed by the same reasoning
  already established for `ADR-0069`'s and `ADR-0071`'s own additive-evidence changes.

### Option 2 - Hermetic-only near-boundary coverage (H-05's remedy shape, adapted)

Add near-boundary Moon cases as a new, frozen, hermetic (non-oracle) holdout, following H-05's own
precedent exactly: pick Moon longitudes close to boundaries, compute the certified engine's own exact
timeline for them, freeze the results as a committed baseline (with a negative control proving the
freeze would catch a regression), without requiring a fresh PyJHora oracle run.

- **Rationale available to support this option:** does not require the PyJHora oracle venv at all
  (available on this host only in the isolated exploration environment, unrunnable in ordinary CI without
  the hash-pinned oracle job); faster to build; matches an already-accepted precedent in this exact
  repository for closing a dasha-layer coverage gap with zero certified-value impact.
- **Disadvantages, weighed directly against the audit's own words:** the audit's M-02 finding and the
  roadmap's own step-5 wording both specifically name **the oracle gate** as where the coverage is
  missing - "the oracle gate contains zero near-boundary Moon cases." A hermetic-only fix would add
  in-repository boundary coverage, but would **not** close the specific gap the audit and roadmap
  describe: it would leave the oracle gate itself exactly as under-covered as it is today, merely adding
  a second, independent form of coverage alongside it. This is a materially weaker claim than Option 1's
  - "we have a hermetic near-boundary baseline" is not the same evidentiary strength as "our near-boundary
  behaviour independently agrees with an external oracle," which is precisely what makes the oracle gate
  more valuable than the hermetic tier for exactly this kind of sensitivity (per the roadmap's own
  section 1 framing of why dashas need Tier-1, oracle-grade treatment).
- **Certification implications:** additive only, no PyJHora dependency required for this specific
  addition.
- **Blast radius:** `engine/tests/` (a new hermetic test file, mirroring `test_vimshottari_hermetic_
  baseline.py`'s own structure), no certifier-script or certification-artifact change unless the artifact
  is also updated to reference the new hermetic coverage.
- **Certified-value impact:** none.

### Option 3 - Fix the label-accuracy defect only; document the coverage gap explicitly; do not build new coverage yet

Rename `H10`/`H11` to remove the misleading "boundary_moon" claim (they remain valid, ordinary,
already-passing cases under an accurate name), and add an `explicit_non_claims` entry stating the oracle
gate does not yet contain genuine near-boundary Moon coverage. Build no new near-boundary cases.

- **Advantages:** closes the honesty/label-accuracy defect (section B item 2) immediately, at near-zero
  cost, without requiring the oracle venv or any new root-finding work; mirrors the general discipline
  this session has applied throughout (an artifact's own documented scope should never overclaim, per
  `H-06`'s and `H-08`'s own `explicit_non_claims` treatment).
- **Disadvantages:** does **not** close M-02 as the roadmap's own step-5 language defines it ("Add
  near-boundary Moon cases to the oracle gate, closing M-02") - this option only stops the gate from
  *implying* coverage it lacks; it does not add the coverage itself. `Q8_CLOSURE_MATRIX.md` s5's own
  wording is a plain, non-alternative six-step list (the same structure `DP-016`/`DP-017`/`DP-018` already
  confirmed gives no `DP-015`-style carve-out opening), so this option alone would likely not satisfy
  JATAKA's own entry criterion for this step, even though it is a genuine, worthwhile improvement in its
  own right.
- **Certification implications:** metadata-only (renamed case IDs, one new `explicit_non_claims` entry).
- **Blast radius:** `scripts/certify_vimshottari.py` (rename two case IDs), `certification/
  VIMSHOTTARI_V1_certification.json` (regeneration reflecting the rename and the new disclosure).
- **Certified-value impact:** none.

### Option 4 - Defer entirely

Leave `H10`/`H11` mislabeled and the oracle gate without genuine near-boundary coverage, record an
explicit deferral decision.

- **Advantages:** zero implementation cost.
- **Disadvantages:** the roadmap's own six-step list names this explicitly as required for JATAKA entry;
  Option 1's technical feasibility is now independently confirmed via already-certified infrastructure
  (`find_crossings()`), so the remaining cost is oracle-venv availability and case-selection judgment, not
  a genuine engineering unknown - a materially weaker cost/benefit case for deferral than existed before
  this session's own verification. Even the cheapest available fix (Option 3) is not achieved by
  deferring.
- **Certification implications:** none.
- **Blast radius:** none.
- **Certified-value impact:** none.

## F. Recommendation

**Option 1, at medium-high confidence, with Option 3's label correction folded in as part of it (not
pursued as a separate, lesser fix).** Reasoning: (i) the audit's and roadmap's own language both name
the oracle gate specifically, which only Option 1 actually satisfies; (ii) Option 1's technical
feasibility is now independently confirmed this session using existing, already-certified infrastructure
(`find_crossings()`), not a speculative engineering plan - the residual open questions are case-selection
judgment calls, not open technical risk; (iii) Option 1 has zero certified-value impact, matching every
other closed item in this sequence; (iv) Option 2 (hermetic-only) is faster but demonstrably does not
close what the audit and roadmap actually describe, so it is not recommended as a substitute, though it
could be a reasonable *supplement* if the owner wants both forms of evidence; (v) Option 3 alone is
strictly dominated by Option 1, since Option 1's own implementation naturally also resolves the labelling
defect Option 3 targets - there is little reason to choose Option 3 over Option 1 unless oracle-venv
availability becomes a genuine blocker at implementation time, in which case Option 3 remains available
as a fallback. Option 4 (defer) has a weak cost/benefit case, matching this session's now-consistent
finding for every other roadmap step it was checked against.

**Confidence: medium-high.** Comparable to `DP-018`'s own H-08 lean - the recommended option's technical
path is now independently verified feasible with low blast radius, and the two remaining sub-questions
(exactly how many boundaries/offsets to sample; what becomes of `H10`/`H11`) are implementation-time
judgment calls, not open risks that could change the recommendation itself.

## G. What is NOT being decided by this paper

Whether new near-boundary cases are added to the oracle gate; how many boundaries or offsets are
sampled; whether `H10`/`H11` are renamed or replaced; whether `explicit_non_claims` is updated in the
interim; whether Option 2's hermetic coverage is built in addition to Option 1. The dasha
boundary-proximity indicator (the roadmap's step 6, a distinct item from M-02 despite sharing the word
"boundary" and being cited together in `DP-015`) and any JATAKA implementation are untouched and not
addressed. `DP-016`/H-05, `DP-017`/H-06, `DP-018`/H-08, `DP-015`/its own FOUNDATION-scope
boundary-proximity carve-out, FOUNDATION, and every already-closed item remain exactly as ratified - none
is reopened or reconsidered by this paper.

## H. Exact CEO/owner decision required

Select Option 1 (root-find genuine near-boundary cases and add them to the oracle gate, with `H10`/`H11`
corrected as part of the same work), Option 2 (hermetic-only coverage, faster but does not satisfy the
oracle-gate-specific wording), Option 3 (fix only the label-accuracy defect, defer genuine coverage), or
Option 4 (defer entirely) for M-02. If Option 1, the owner may additionally specify a preference on
either open sub-question in section E (how many boundaries/offsets to sample; what becomes of `H10`/
`H11`), or leave both to implementation-time judgment, since neither choice changes any certified value.
Recorded as a new, numbered decision-log entry citing this paper - this paper alone authorizes nothing,
and does not authorize the dasha boundary-proximity indicator or any JATAKA implementation.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-08-24 | Marked ADDRESSED by `ADR-0072` (Option 1 accepted and implemented: six root-found near-boundary cases added via `engine.transits.crossing.find_crossings()`, `H10`/`H11` corrected). Paper's substantive text below unchanged. |
| 1.0.0 | 2026-08-22 | Created. Fourth authorized JATAKA-entry-prerequisite decision-readiness paper, extracting `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`'s M-02 finding and `docs/DASHA_CERTIFICATION_ROADMAP.md` step 5, with every claim independently re-verified against the live `scripts/certify_vimshottari.py` HOLDOUT set and the current tree - not trusted from the audit's own summary. Independently reproduced the audit's own exact reported distances (6.46 and 5.02 degrees) for `H10_boundary_moon_a`/`H11_boundary_moon_b`, and additionally measured all nine other holdout cases, confirming eight of nine are closer to a boundary than at least one of the two cases labelled "boundary." Independently verified Option 1's technical feasibility live using the already-certified `engine.transits.crossing.find_crossings()` (`TRANSIT_V1`), locating a real Moon-boundary crossing at sub-microarcsecond residual within a one-month window. Checked H-04/H-05/H-06/H-08 as precedents explicitly, finding H-05's own hermetic-only remedy shape does not actually satisfy M-02's oracle-gate-specific wording, and identifying `KP_CHAIN_V1`'s/`TRIKALAM_V1`'s own boundary-battery precedent as the more directly applicable shape. Classifies M-02 as an oracle/holdout coverage gap combined with a smaller label-accuracy defect - not a calculation defect. Presents four options (root-find genuine oracle-gate cases; hermetic-only coverage; label-fix only; defer), medium-high-confidence lean toward Option 1 with Option 3's label fix folded into it. Options only; decides nothing; not implementation-authorized. |
