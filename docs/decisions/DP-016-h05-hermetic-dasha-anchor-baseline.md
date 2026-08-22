<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and recommends one. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-22 |
| Review cadence | TBD |

# DP-016. H-05: the hermetic tier cannot detect a wrong dasha anchor

## 1. The question

`docs/DASHA_CERTIFICATION_ROADMAP.md` section 5 names H-05 as step 2 of the six JATAKA-entry
prerequisites (`Q8_CLOSURE_MATRIX.md` s5: "The Dasha roadmap's steps 1 to 6 complete"). Step 1 (H-04) is
already closed (`ADR-0053`, 2026-08-17). This paper is the decision-readiness work for step 2, authorized
by the owner's explicit "Authorize the next JATAKA-entry prerequisite work: H-05 decision-readiness only"
instruction. It investigates the exact problem, what governs it today, what legitimate treatment options
exist, and their certification implications - it does not implement anything, does not choose an option,
and does not authorize H-06, H-08, M-02, or the dasha boundary-proximity indicator.

## 2. What is already established, and what is not

**Established (direct citation and direct code/test inspection this session, not re-derived from the
roadmap document alone):**

- `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-05, quoted in full: a mutation test flipping the sign
  at `engine/dasha/vimshottari.py:122` from `birth_jd - float(elapsed_years * year_length)` to `+`
  injects a 4,748-day error into every dasha date and **passes every oracle-free gate**. "No committed
  numeric baseline of dasha calendar dates exists anywhere in the repository." Proposed solution: "Commit
  a small frozen baseline of dasha instants for a handful of fixed seeds and assert against it
  hermetically." Tests required: "The frozen-baseline test, plus the anchor mutation as a documented
  negative control."
- **Re-verified live against the current tree, unchanged since the audit:** `engine/dasha/
  vimshottari.py:122` still reads `anchor_jd = birth_jd - float(elapsed_years * year_length)` exactly.
  `elapsed_years = seed_years * elapsed` (the portion of the seed nakshatra's dasha-years already elapsed
  at birth); `anchor_jd` is the JD at which the current mahadasha would theoretically have begun, derived
  by stepping backward from birth by that many years. **Behavioural impact today: none - the anchor is
  correct.** This is a certification-coverage gap probed by a hypothetical mutation, not a discovered
  production defect.
- **Each of the three "passes every oracle-free gate" claims individually re-verified by direct code
  reading, not trusted from the audit's own summary:**
  - `engine/tests/test_vimshottari_invariants.py::test_jd_view_is_consistent_with_exact_offsets` (the
    "JD-consistency test") asserts `period.start_jd == timeline.anchor_jd + float(period.start_years *
    year_length)` - relative to `anchor_jd` itself, so a sign-flipped `anchor_jd` would still satisfy
    this identity. Confirmed insensitive to the mutation.
  - `test_moon_exactly_on_boundary_starts_full_dasha` (the "boundary test") asserts `timeline.anchor_jd
    == timeline.birth_jd` only for the `elapsed == 0` case, where `elapsed_years == 0` regardless of
    sign. Confirmed insensitive to the mutation.
  - `validate_vimshottari_holdout.py` (the independent validator, Gate 4 of `ADR-0007`) confirmed by
    direct reading: its `compare()` function checks `seed_nakshatra_number`, `seed_lord`,
    `seed_elapsed_fraction`, `balance_years`, and `(lords, start_years, end_years)` tuples - every
    comparison is in `Fraction` **year offsets relative to the anchor**; `start_jd`/`end_jd`/`anchor_jd`
    are never read anywhere in the file. Confirmed insensitive to the mutation.
- **The oracle-tier gate is the only one that would catch it, and only when it actually runs:**
  `scripts/certify_vimshottari.py` unconditionally imports PyJHora at module load (`try: from jhora
  import const...`) and `sys.exit(3)` if unavailable - fails closed exactly like every other oracle-tier
  certifier in this repository, so it cannot run at all on this Windows host (no PyJHora installed
  outside an isolated exploration venv). Its comparison (`delta = abs(our_period.start_jd -
  oracle_jd)`) does read `start_jd`, an absolute date, against PyJHora's own independently-computed
  Julian Day - this WOULD catch the mutation. Confirmed via `.github/workflows/ci.yml` line 284:
  `certify_vimshottari.py` runs only inside the `oracle` job (hash-pinned PyJHora, Linux runner), never
  inside the `hermetic` job (network-free, runs on both Python interpreters on every commit).
- **`certification/VIMSHOTTARI_V1_certification.json`'s own schema confirmed by direct inspection:** no
  lettered gate structure (unlike most other certifiers' A-E pattern); its `gates` object contains only
  oracle-derived fields (`oracle_pratyantar_rows_compared`, `oracle_lord_mismatches`,
  `oracle_max_start_delta_days`, `independent_validator`, `cases`) plus `start_tolerance_days`. Its
  `explicit_non_claims` list ("other dasha systems," "depths beyond pratyantardasha," "year conventions
  other than the certified profile," "transit or event overlays") does **not** mention the hermetic-tier
  gap - the limitation is real and currently undocumented anywhere in the certified artifact.
- **The established "committed frozen baseline" pattern in this repository, for reference, not
  prescription:** `brihat_fixtures.py` holds real-chart comparison data "transcribed from screenshots"
  of independent third-party software, explicitly labelled "COMPARISON FIXTURES, not astronomical ground
  truth" - the precedent this repository already uses for an independently-sourced, hermetically-usable
  reference. Confirmed by direct inspection: its existing cases record lord sequences (mahadasha through
  a deeper level), **not** Julian-Day-level dasha transition dates - it does not already contain what
  H-05 needs; a genuinely new data-gathering step would be required regardless of which option is chosen
  to build a baseline, since no existing fixture currently carries dasha *instants*.
- **No prior ADR or decision paper addresses H-05.** Confirmed by direct search of `docs/DECISION_LOG.md`
  for "H-05": zero hits before this paper. `ADR-0053` closed H-04 and M-03 (a documentation-versus-
  evidence gap, and an anti-fitting scan-coverage gap) - a different pair of findings from the same audit,
  not H-05.

**Not established (explicitly not decided by this paper):** whether a frozen hermetic baseline is built;
what its data source would be; how many seed cases; whether H-05's fix is bundled with H-06's (both
touch `engine/dasha/`) or kept separate.

## A. Exact H-05 problem statement

`engine/dasha/vimshottari.py`'s anchor computation (`anchor_jd = birth_jd - float(elapsed_years *
year_length)`) has no certification coverage that would independently confirm its sign or its absolute
correctness in the **hermetic tier** - the network-free tier that runs on every commit, on both
supported Python interpreters, without requiring PyJHora. Every hermetic-tier test currently in the
repository either compares values *relative to* the very `anchor_jd` under test (so a systematic error in
it is invisible), or never inspects a Julian Day at all (so it cannot see the error class in the first
place). Only the oracle-tier certifier, which needs PyJHora and runs solely in CI's Linux `oracle` job,
would catch a defect of this shape - and it does not run locally, does not run on every commit, and does
not run on both interpreter versions the hermetic tier covers.

## B. What "hermetic-tier protected dasha baseline" means in the current architecture

"Hermetic tier" is this repository's own established term (`.github/workflows/ci.yml`'s `hermetic` job;
used identically in `ADR-0053`'s own H-04 discussion) for the network-free, PyJHora-free certification
and test path that runs on both Python 3.11 and 3.12 on every commit. A "protected baseline" in this
tier, by the pattern every other certifier in this repository already uses (the H1-H11 real-world holdout
via `brihat_fixtures.py`; the D9/D10/D-varga holdouts; `RISE_SET_V1`'s own H1-H11 reuse), means a
committed, versioned set of expected values - here, dasha period *instants* (Julian Days or the
equivalent civil timestamps) for a handful of fixed seed inputs - sourced independently of the
production code under test, checked by a hermetic (no-network, no-oracle) assertion. For H-05
specifically, this means at minimum: a frozen `anchor_jd` (or equivalent absolute-date) value per seed
case, so a sign error or any other systematic anchor defect is caught by `pytest` alone, with no PyJHora
dependency and no CI oracle-job wait.

## C. What the anchor sign-flip finding demonstrates

Two distinct things, both real: (1) a **coverage gap**, precisely characterized above - three
independent-looking checks (JD-consistency, boundary, independent validator) all happen to be structurally
blind to this exact error class, for three different reasons, so their number is not a proxy for actual
protection; (2) a **methodological point about self-referential testing**, consistent with this
repository's own `.claude/rules/validation.md` ("A test that compares a function's output to itself...
proves internal consistency, not correctness"): every hermetic test currently in place is, with respect
to the anchor's *absolute* correctness, exactly this kind of self-referential check. It does not
demonstrate that the anchor is currently wrong - direct re-verification this session confirms it is not.

## D. Classification

A **certification/governance coverage gap combined with a genuinely missing baseline** - not a
calculation defect. The shipped formula is correct today, confirmed by direct re-reading; nothing behaves
incorrectly for any user of the engine right now. What is missing is independent, hermetic-tier evidence
that it stays correct, and a fixture that would let a future regression of this specific shape be caught
without needing PyJHora or a CI run.

## E. All legitimate options

### Option 1 - Build the frozen hermetic baseline, per the audit's own proposed solution

Commit a small set of fixed-seed cases (moon longitude, birth JD, dasha profile) with frozen, independently-
sourced expected `anchor_jd`/period-instant values, asserted in a new hermetic pytest test; add the
documented anchor-sign mutation as a paired negative control (proving the new test actually fails when
the defect is reintroduced, not merely that it currently passes).

**Two genuinely open sub-questions this paper surfaces but does not resolve, since either is a legitimate
implementation choice, not obviously compelled by the evidence:**
- **Data source for the frozen values.** (a) Transcribe from an independent third-party classical
  software's own displayed dasha dates, mirroring `brihat_fixtures.py`'s existing "transcribed from
  screenshots" precedent - genuinely independent, but requires sourcing software that displays dates
  (not just lord sequences, which is all the current fixture module records) and manual transcription
  with its own transcription-error risk (mitigated the same way `ADR-0011`'s trikalam work already did:
  second transcription, or cross-check against a second source). (b) Capture PyJHora's own oracle output
  once, in the same isolated exploration venv this session already uses, and freeze it as a hermetic
  fixture - converts "protected only when the CI oracle job runs" into "protected on every commit,
  permanently," using the same oracle already trusted for the certifier's own live comparison, at the
  cost of the frozen baseline no longer being independent of PyJHora specifically (though it would still
  be independent of *this engine's own code*, which is what the hermetic gate needs to protect against).
- **Whether to also add H-06's `CERTIFIED_DASHA_PROFILES` allow-list in the same pass.** Both touch
  `engine/dasha/`; `ADR-0053` closed H-04 and the unrelated M-03 together because both were authorized
  in one instruction. This paper's own scope is H-05 only, per the owner's explicit instruction not to
  start H-06 yet - noted here only because a future implementer will find the files adjacent, not as a
  recommendation to combine them.

- **Certification implications:** a new hermetic pytest test (and its negative control), not a change to
  `certify_vimshottari.py` or to `VIMSHOTTARI_V1_certification.json`'s schema - the hermetic tier and the
  oracle-tier certifier are architecturally separate paths in this repository (confirmed above), so
  closing H-05 does not require touching the oracle certifier at all. `explicit_non_claims` could be
  updated to remove the now-closed gap, mirroring how `ADR-0053` updated `VIMSHOTTARI_V1`'s own evidence
  after H-04 closed.
- **Blast radius:** `engine/tests/` (new test, and/or a new or extended fixture module) only. No change
  to `engine/dasha/vimshottari.py` or any other production code - the formula is already correct and
  does not need to change for this option.
- **Certified-value impact:** **none.** `VIMSHOTTARI_V1_certification.json`'s own fields (oracle
  comparison results, tolerances, verdict) are untouched, since this option adds hermetic-tier test
  coverage, not a certifier or artifact change. Matches `docs/DASHA_CERTIFICATION_ROADMAP.md` section 5's
  own explicit claim: "Steps 1 through 6 change no calculated value" - independently confirmed here for
  step 2 specifically, not merely quoted.

### Option 2 - Defer: document the gap explicitly, rely on the existing oracle-tier gate

Record a decision explicitly deferring the hermetic-tier baseline until JATAKA-entry work actually
proceeds past this step, or until a specific reason to prioritize it arises; add the hermetic-tier
limitation to `VIMSHOTTARI_V1_certification.json`'s `explicit_non_claims` (a documentation-only change)
so the gap is at least visible rather than silently absent, as it is today.

- **Advantages:** zero implementation cost; the anchor is confirmed correct today, so nothing is
  currently at risk; matches this session's own established deferral precedent (`DP-012`/`ADR-0063`,
  `DP-015`/`ADR-0067`'s amended Option 3) for gaps with no live defect behind them.
- **Disadvantages:** JATAKA's own entry criteria explicitly name this step as required - deferring it
  does not close that prerequisite, so JATAKA entry would still need this work eventually, unless the
  owner also separately decides (mirroring the boundary-proximity/civil-date-rendering precedent) that
  the JATAKA entry criteria's own reach can be narrowed by explicit decision - a distinct, larger
  question this paper does not raise or invite, since `Q8_CLOSURE_MATRIX.md` s5's "Dasha roadmap's steps
  1 to 6 complete" wording is a plain, non-alternative list, unlike s4's H-01/H-02 carve-out; nothing in
  this repository's record suggests that clause admits the same kind of narrow decoupling treatment.
- **Certification implications:** a documentation-only edit to `explicit_non_claims`, if made; otherwise
  none.
- **Blast radius:** none, or (if the `explicit_non_claims` edit is made) `certification/
  VIMSHOTTARI_V1_certification.json` and its rendered report only - a metadata-level change, not a gate
  or value change.
- **Certified-value impact:** none under either variant.

## F/G/H. Certification implications, blast radius, and certified-value impact

Stated inline under each option in section E; no certified value changes under either option.

## I. Recommendation

**Option 1, at medium-high confidence** - higher than this session's usual decision-paper confidence,
because: (i) the fix is the audit's own specifically-proposed solution, not something this paper had to
construct; (ii) it is architecturally the same class of work as H-04/M-03 (`ADR-0053`), already closed
successfully in this repository with an identical "zero certified-value impact, additive test coverage
only" profile; (iii) JATAKA's own entry criteria name this step explicitly, so the work is needed
eventually regardless, and `Q8_CLOSURE_MATRIX.md` s5's wording gives no textual opening for the kind of
narrow decoupling `ADR-0067`/the `ADR-0063` addendum used elsewhere; (iv) unlike H-08 (an explicit
owner-only convention choice) or the FOUNDATION-scope boundary-proximity work (genuinely undesigned),
H-05's fix has a clear, bounded shape with an established architectural precedent to build from
(`brihat_fixtures.py`). Option 2 remains legitimate if the owner prefers to sequence differently or
judges the JATAKA timeline does not yet warrant this work.

## J. Exact CEO/owner decision required

Select Option 1 (build the frozen hermetic baseline and negative control) or Option 2 (defer, optionally
documenting the gap) for H-05. If Option 1, the owner may additionally specify a preferred data source
for the frozen baseline (independently-transcribed third-party output, or a frozen PyJHora snapshot) or
leave that to implementation-time judgment, since neither choice changes any certified value or the
certification implications already stated in section E. Recorded as a new, numbered decision-log entry
citing this paper - this paper alone authorizes nothing, and does not authorize H-06, H-08, M-02, the
dasha boundary-proximity indicator, or any JATAKA implementation.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-22 | Created. First authorized JATAKA-entry-prerequisite decision-readiness paper, extracting `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`'s H-05 finding and `docs/DASHA_CERTIFICATION_ROADMAP.md` step 2, with every claim independently re-verified against the live `engine/dasha/vimshottari.py`, its test suite, its independent validator, its certifier, and CI wiring, not trusted from the roadmap's own summary. Presents two options (build the hermetic baseline; defer) with a medium-high-confidence lean toward building it. Options only; decides nothing; not implementation-authorized. |
