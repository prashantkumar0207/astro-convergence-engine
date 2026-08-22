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

# DP-017. H-06: no allow-list for dasha profiles; an uncertified year convention flows through production entry points

## 1. The question

`docs/DASHA_CERTIFICATION_ROADMAP.md` section 5 names H-06 as step 3 of the six JATAKA-entry
prerequisites (`Q8_CLOSURE_MATRIX.md` s5: "The Dasha roadmap's steps 1 to 6 complete"). Steps 1 (H-04)
and 2 (H-05) are already closed (`ADR-0053`, `ADR-0069`). This paper is the decision-readiness work for
step 3, authorized by the owner's explicit "Authorize the next JATAKA-entry prerequisite: H-06
decision-readiness" instruction, following `DASHA_CERTIFICATION_ROADMAP.md`'s own established order. It
investigates the exact problem, what governs it today, what legitimate treatment options exist, and
their certification implications - it does not implement anything, does not choose an option, and does
not authorize H-08, M-02, the dasha boundary-proximity indicator, or any JATAKA implementation.

## 2. What is already established, and what is not

**Established (direct citation and direct code/test inspection this session, not re-derived from the
roadmap document alone):**

- `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-06, quoted in full: verified,
  `vimshottari_parashari(birth, dasha_profile=DashaProfile('i_made_this_up', Fraction(360), 'no
  source'))` returns a fully provenance-stamped timeline; nothing rejects it. `DashaProfile.
  year_length_days` is annotated `Fraction` but unchecked, so passing a float silently converts the
  timeline's calendar arithmetic to float and destroys the exactness guarantee the module docstrings
  advertise, with no error and no failing test. "The varga layer refuses exactly this class of thing
  through `CERTIFIED_PRODUCTION_VARGAS` and `UnsupportedVargaError`. The dasha layer has no
  equivalent." Proposed solution: "A `CERTIFIED_DASHA_PROFILES` constant mirroring the varga pattern,
  with a refusal error, plus runtime type enforcement on `year_length_days`." Tests required: "Refusal
  tests for an unregistered profile and for a float year length; a positive test for the certified
  profile."
- **Both claims independently reproduced live against the current tree, unchanged since the audit:**
  `engine/dasha/profile.py`'s `DashaProfile` is a plain `@dataclass(frozen=True)` with no `__post_init__`
  and no validation of any kind - `name`, `year_length_days`, and `source` are all unchecked. Constructed
  directly this session: `DashaProfile('i_made_this_up', Fraction(360), 'no source')` passed to
  `vimshottari_from_moon()` returns a normal `VimshottariTimeline` with `dasha_profile_name:
  'i_made_this_up'` and a computed `anchor_jd` - no exception. Separately: `DashaProfile('float_year',
  365.25, 'no source')` (a Python `float`, not `Fraction`) is accepted identically; `type(t2.
  year_length_days)` is confirmed `<class 'float'>`. Verified the exactness-destruction claim
  numerically, not just the type: `Fraction(7) * 365.256364` (the certified exact convention) and
  `Fraction(7) * 365.25` (a plausible but wrong float substitute) produce different results
  (`2556.794548` vs `2556.75`) with **no exception raised either way** - Python's numeric tower silently
  promotes `Fraction * float` to `float` arithmetic, so an uncertified year length is not merely
  "unchecked," it is silently computed and returned as a normal result.
- **`engine/dasha/vimshottari.py`'s four entry points all route through the same unchecked path**,
  confirmed by direct reading: `vimshottari_from_moon()` (line 120: `year_length = dasha_profile.
  year_length_days`, used immediately with no check), `vimshottari_from_snapshot()`,
  `vimshottari_parashari()`, and `vimshottari_kp()` all accept `dasha_profile` as a plain keyword
  argument with the certified default and forward it unchecked. No allow-list, no type guard, anywhere
  in the call chain.
- **Zero existing test coverage of this gap**, confirmed by direct search: no test in `engine/tests/
  test_vimshottari_*.py` constructs an uncertified `DashaProfile` or a float `year_length_days`. The
  audit's own "no failing test" claim is still accurate today.
- **`certification/VIMSHOTTARI_V1_certification.json`'s own `explicit_non_claims` already lists "year
  conventions other than the certified profile"** - the certification artifact's own documentation is
  accurate and does not overclaim; the gap is specifically that nothing in the **code** enforces the
  scope the artifact already, correctly, disclaims.
- **The established allow-list precedent this session inspected directly, since H-06's own proposed
  solution names it as the pattern to mirror:** `engine/astrology/__init__.py`'s
  `CERTIFIED_PRODUCTION_VARGAS` is a static tuple, "the single source of truth for the sanctioned
  registry state," each entry commented with its own ADR; `engine/astrology/varga_registry.py`'s
  `get_varga_rule()` raises `UnsupportedVargaError(NotImplementedError)` naming what *is* registered
  when a `(division, school)` key is not found. The varga layer's mechanism is a dynamic runtime
  registry (rules are registered by import side-effect); the dasha layer has no equivalent registration
  step - `DashaProfile` instances are constructed directly and passed as plain arguments, an
  architecturally simpler situation than vargas', not a plugin system.
- **`DashaProfile(...)` is constructed exactly once anywhere in the tracked tree** - the certified
  `VIMSHOTTARI_MEAN_SIDEREAL_YEAR` instance itself, in `engine/dasha/profile.py`. Confirmed by a
  repository-wide search. No production code, and no committed test, currently constructs an
  uncertified profile - **the gap is entirely latent in the current shipped tree**, exactly as the
  audit's own "Behavioural impact: an uncertified year convention produces plausible-looking
  certified-shaped output" implies a hypothetical caller, not a discovered live defect.
- **No prior ADR or decision paper addresses H-06.** Confirmed by direct search of `docs/
  DECISION_LOG.md` and `docs/decisions/` for "H-06": only citations noting it remains open (including
  this session's own `DP-016`, which explicitly deferred it).

**Not established (explicitly not decided by this paper):** whether an allow-list is built; where the
type-enforcement check would live (`DashaProfile.__post_init__` versus an entry-point check); how many
or which profile names the allow-list would name (only one profile is currently certified, so this is
close to fixed, but not this paper's decision).

## A. The exact H-06 problem

`DashaProfile` carries no enforcement of any kind - not of which convention it names, and not of the
type of its own `year_length_days` field, despite that field being annotated `Fraction` specifically
because the module's own docstrings advertise "exact rational arithmetic throughout" as the layer's
central guarantee. Every Vimshottari entry point accepts and uses an arbitrary `DashaProfile` with no
check, so a caller - today, only a test or a future feature, since nothing in the shipped tree does this
- can silently obtain a fully-formed, provenance-stamped, plausible-looking timeline built on a
convention `VIMSHOTTARI_V1` never certified, with no error and no signal that anything is wrong.

## B. Whether this is a defect, certification gap, governance gap, missing protection, or a combination

**A combination of a certification/governance gap and a missing input-validation protection - not a
calculation defect.** The certified profile (`VIMSHOTTARI_MEAN_SIDEREAL_YEAR`) computes correctly in
every case; nothing about its own arithmetic is wrong. Two genuinely separate sub-gaps, worth keeping
distinct since they may warrant different treatment: (1) a **certification-scope enforcement gap** -
nothing stops an uncertified profile *name* from reaching production, mirroring the varga layer's own
already-solved problem exactly; (2) a **type-safety gap** - nothing stops `year_length_days` from being
a `float` (or any other numeric type) instead of the `Fraction` its own type annotation promises,
independent of whether the profile's *name* is certified. A profile could fail either check without the
other (a certified-named profile constructed with a float by accident; an uncertified-named profile that
happens to use an exact `Fraction`).

## C. All legitimate treatment options

### Option 1 - Build the allow-list and type enforcement, per the audit's own proposed solution

Add `CERTIFIED_DASHA_PROFILES` (a static tuple/set naming sanctioned profile identities, mirroring
`CERTIFIED_PRODUCTION_VARGAS`'s role) and `UnsupportedDashaProfileError(NotImplementedError)` (mirroring
`UnsupportedVargaError`'s convention) to `engine/dasha/profile.py`; add a refusal check to the shared
entry point(s) in `engine/dasha/vimshottari.py`; add runtime type enforcement on `year_length_days`.

**Two genuinely open sub-questions this paper surfaces but does not resolve:**
- **Where the type-enforcement check lives.** (a) `DashaProfile.__post_init__` - frozen dataclasses can
  still validate and raise in `__post_init__` (raising needs no mutation), so this would enforce every
  `DashaProfile` ever constructed, anywhere, as a structural invariant of the type itself, independent
  of certification status. (b) An entry-point check inside `vimshottari_from_moon()`, alongside the
  allow-list check, treating "is this a well-typed profile" as a usage-site concern rather than a
  construction-time one. The two are not mutually exclusive, but a decision paper should not silently
  pick the design that changes where a future test would need to target its negative control.
- **Whether the allow-list is keyed on the profile's name alone, or on identity (the exact frozen
  instance).** The varga registry's own precedent keys on `(division, school)` - a value tuple, not
  object identity - suggesting name-keying is the more directly analogous choice, but this paper does
  not choose it.

- **Certification implications:** matches H-05's own precedent (`ADR-0069`) closely - this is additive
  test/guard coverage, not a change to `certify_vimshottari.py` or to `VIMSHOTTARI_V1_certification.
  json`'s schema. The certification artifact's `explicit_non_claims` already correctly states "year
  conventions other than the certified profile" is out of scope; this option makes that scope
  *enforced*, not merely documented. A follow-up addition to `explicit_non_claims` explicitly noting the
  new refusal behaviour is optional, not required, mirroring `DP-016`'s own treatment of the equivalent
  question for H-05.
- **Blast radius:** `engine/dasha/profile.py` (new constant + exception class), `engine/dasha/
  vimshottari.py` (the refusal check, at whichever entry point(s) the owner's answer to the first
  sub-question implies), `engine/tests/` (new refusal tests plus a positive test for the certified
  profile, matching the audit's own "Tests required" line exactly). No change to any other module.
- **Certified-value impact:** **none.** The certified profile's own computation path is completely
  unaffected by adding a guard that only *rejects* other inputs - confirmed by the same reasoning
  already established for `ADR-0066` (H-01) and `ADR-0069` (H-05): a refusal guard changes what is
  rejected, never what a certified input produces.

### Option 2 - Defer: document the gap explicitly, rely on the fact that nothing currently exercises it

Record a decision explicitly deferring the allow-list/type-enforcement work, since the gap is entirely
latent (confirmed: `DashaProfile` is constructed exactly once anywhere in the tracked tree, and that one
construction is the certified profile itself) and JATAKA has not yet begun.

- **Advantages:** zero implementation cost; matches this session's own established deferral precedent
  (`DP-012`/`ADR-0063`, `DP-015`/`ADR-0067`'s amended Option 3) for gaps with no live defect behind
  them; the risk profile here is arguably *lower* than H-05's own (which had a documented mutation
  scenario with a concrete magnitude) since H-06's exposure requires a future caller to deliberately
  construct a non-default `DashaProfile`, which nothing in the current codebase does or is close to
  doing.
- **Disadvantages:** JATAKA's own entry criteria explicitly name this step as required (`Q8_CLOSURE_
  MATRIX.md` s5's wording is a plain, non-alternative list of six steps, the same textual structure
  `DP-016` already found gives no opening for a `DP-015`-style decoupling) - deferring it does not close
  that prerequisite, so the work is needed eventually regardless if JATAKA is ever entered. Unlike H-05,
  where the fix required a genuine data-sourcing effort (frozen baseline values), H-06's fix is smaller
  and more self-contained (a constant, an exception class, an entry-point check), so the cost/benefit
  case for deferring is weaker than it might first appear.
- **Certification implications:** none, or (if a documentation-only note is added to `explicit_non_
  claims`) a metadata-level change only.
- **Blast radius:** none.
- **Certified-value impact:** none under either variant.

## D/E. Certification implications and blast radius

Stated inline under each option in section C; no certified value changes under either option.

## F. Whether existing certified dasha values change under each option

**No, under either option.** `VIMSHOTTARI_MEAN_SIDEREAL_YEAR`'s own computation path is never touched by
Option 1's guard (which only rejects other inputs) or by Option 2 (which changes nothing). Confirmed
directly, not merely by analogy: the certified profile's `year_length_days` is already a `Fraction`
(`Fraction(365256364, 1000000)`), so a type-enforcement check would pass it trivially, and its `name`
(`"vimshottari_mean_sidereal_year"`) would be the sole entry - by construction - of any allow-list Option
1 might build.

## G. Recommendation

**Option 1, at medium confidence** - lower than H-05's own medium-high lean (`DP-016`), because: (i) the
fix is audit-authored and architecturally analogous to the varga layer's own already-solved problem,
which favours building it; but (ii) unlike H-05, H-06's gap is entirely latent today with no concrete
reproduction scenario reachable from any shipped code path, which favours deferring it; and (iii) two
genuine implementation sub-questions (section C) remain open enough that "the evidence supports an
option" is true but not as cleanly as it was for H-05, where the audit's proposed solution left almost
nothing to design. Option 2 (defer) is equally legitimate if the owner judges JATAKA's own eventual entry
work is the more natural point to build this, since nothing today is silently wrong.

**Confidence: medium.** Weaker than `DP-016`'s own lean, for the reasons in (ii) and (iii) above; stronger
than a toss-up, because the fix - whichever sub-question answers are chosen - is small, additive, and has
a directly analogous precedent already built and certified in this repository (the varga registry).

## H. What is NOT being decided by this paper

Whether the allow-list/type-enforcement is built; where the type check lives (construction-time versus
entry-point); how the allow-list is keyed; whether `explicit_non_claims` is updated. H-08, M-02, the
dasha boundary-proximity indicator, and any JATAKA implementation are untouched and not addressed. `DP-
016`/H-05, FOUNDATION, and every already-closed FOUNDATION item remain exactly as ratified - none is
reopened or reconsidered by this paper.

## I. Exact CEO/owner decision required

Select Option 1 (build the allow-list and type enforcement, per the audit's own proposed solution) or
Option 2 (defer) for H-06. If Option 1, the owner may additionally specify a preference on either open
sub-question in section C (type-check location; allow-list keying), or leave both to implementation-time
judgment, since neither choice changes any certified value or the certification implications already
stated. Recorded as a new, numbered decision-log entry citing this paper - this paper alone authorizes
nothing, and does not authorize H-08, M-02, the dasha boundary-proximity indicator, or any JATAKA
implementation.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-22 | Created. Second authorized JATAKA-entry-prerequisite decision-readiness paper, extracting `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`'s H-06 finding and `docs/DASHA_CERTIFICATION_ROADMAP.md` step 3, with every claim independently re-verified against the live `engine/dasha/profile.py`/`vimshottari.py`, the varga-registry precedent it cites, and the certification artifact's own `explicit_non_claims`, not trusted from the roadmap's own summary. Confirmed `DashaProfile` is constructed exactly once anywhere in the tracked tree (the certified instance itself) - the gap is entirely latent today. Presents two options (build the allow-list/type guard; defer) with a medium-confidence lean toward building it. Options only; decides nothing; not implementation-authorized. |
