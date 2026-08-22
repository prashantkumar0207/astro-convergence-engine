<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and recommends one. DECIDES NOTHING. Requires owner approval. |
| Version | 1.2.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-21 |
| Review cadence | TBD |

# DP-013. H-02 ingress-classification seam: reproduction methodology and fix option

## 1. The question

`docs/DECISION_LOG.md` `ADR-0020` D5 states: "H-02 is a potential blocker for Muhurta and must be
independently reproduced. Before any production Muhurta implementation, the reported transit ingress and
nakshatra boundary classification defect must be independently reproduced, NOT assumed correct because
it appears in an audit. If confirmed, the underlying calculation is repaired and certified before
dependent Muhurta work." This paper extracts and formalizes only that already-written analysis into a
citable decision paper, per the owner's explicit, scoped authorization ("Scope is strictly the existing
H-02 analysis contained in `ADR-0020` D5"). **It does not ratify `ADR-0020`, any of its other nine
items, or D5 itself** - `ADR-0020` remains `Status: PROPOSED` in its entirety; this paper's own
eventual ratification (via its own future ADR entry) is what would actually bind a reproduction
methodology or fix option, independent of `ADR-0020`'s fate. This paper decides nothing and does not
resolve H-02.

## 2. What is already established, and what is not - stated separately, per the task's own requirement

**Established (by the original audit, not this paper) - the measured finding, preserved verbatim in
substance:** `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` finding H-02, "Ingress instants are classified
into the wrong division by the engine's own certified classifier": the transit root-finder's residual
bound (`1e-4` arcsec, `2.78e-8` degrees) is roughly 278 times wider than the boundary-promotion window
(`1e-10` degrees) division classification uses, so bisection returns a bracket midpoint that lands on
either side of the true root effectively at random. Measured on 2024 under `parashari_lahiri`: **2 of 12
Sun sankranti instants classified into the previous sign; 12 of 28 Moon nakshatra ingress instants
classified into the previous nakshatra.** The existing certification gate misses this because it samples
the classifier 0.05 degrees (Sun) or 0.002 days (Moon) *after* the event instant, not *at* it. Neither
`TRANSIT_V1` nor the varga/nakshatra classification certifications is wrong in isolation - "the defect is
in the seam between them, which no certification covers because no certification spans both" (G1 s.H-02).

**Re-verified against the live codebase, not merely the audit's own wording** (decision-readiness
audit, 2026-08-20): `engine/astrology/longitude_utils.py`'s `BOUNDARY_TOLERANCE` is still exactly `1e-10`
and `engine/transits/crossing.py`'s `RESIDUAL_BOUND_ARCSEC` is still exactly `1e-4` - the 278x mismatch
the audit computed still holds precisely, unchanged since 2026-08-11. The defect has not been silently
fixed or altered in the intervening period.

**Established (by `ADR-0020` D5, itself still PROPOSED) - the procedural requirement, not reopened here:**
the measured percentages above were produced by "a delegated read-only audit," not personally
re-executed by the builder (`ADR-0020` consequence 6). Independent reproduction is required before the
figure is trusted, and before any production Muhurta work depends on it.

**Not established - genuinely open, and what this paper exists to present:**

1. **The reproduction methodology itself.** Neither the G1 audit nor `ADR-0020` D5 specifies how
   "independent reproduction" should be carried out (which holdout instants, which independent reference,
   what counts as confirmation vs. refutation).
2. **Which of the three fix options G1 s.H-02 itself names should be adopted, if reproduction confirms
   the defect** (verbatim from the audit, "for owner decision rather than builder choice"):
   - report the event with an explicit signed residual and an accompanying declared division, so the
     consumer never has to reclassify;
   - bias the returned event instant to the side of the root that classifies into the target division;
   - widen the classifier tolerance to exceed the residual bound.
3. **Whether any fix is a certification-methodology change, a new capability, or both**, and what
   certification evidence it would need - not analyzed by the original audit, which stopped at
   identifying the seam and naming the three options.

## 3. Options (reproduction methodology - the more immediately actionable sub-question)

**Option A. Reuse this repository's own established boundary-precision-testing discipline**: an
independent, differently-coded exact-rational reference (mirroring `certify_current_engine.py`'s
`exact_nakshatra_reference` and this session's own `validate_panchanga_holdout.py`/
`validate_trikalam_holdout.py` pattern) that classifies sign/nakshatra division directly from an
independently-computed longitude at the exact reported event instant, compared against
`engine/transits/crossing.py`'s own reported classification for the same instant, across a protected
holdout of real sankranti/ingress instants (the G1 audit's own 2024 sample, or a newly-selected one).
Directly reuses infrastructure this repository already trusts and has exercised repeatedly this session;
its cost is that it re-derives the SAME residual-vs-tolerance mismatch the audit already reasoned about
analytically, rather than sourcing an independent astronomical reference (e.g. an external oracle) for
the ingress instant itself.

**Option B. Cross-check the reported ingress instant against PyJHora's own sankranti/nakshatra-ingress
detection** (the same external-oracle mechanism `ADR-0059`/`ADR-0061` already established and CI-verified
for this repository's other classification certifiers), comparing the classified division at PyJHora's
independently-computed instant against this engine's. Strongest independence (a second, differently-
implemented system, not just differently-coded arithmetic over the same inputs), consistent with this
repository's now-established preference for a genuine external oracle over an internally-coded reference
where one is reachable (the exact preference the Panchanga Gate F CEO-audit finding enforced earlier this
session). **Feasibility independently verified, not assumed** (PyJHora 4.8.7 wheel downloaded and its
source directly inspected, no execution needed for this check): a reachable API exists -
`jhora.panchanga.drik.next_sankranti_date_from_jd`/`previous_sankranti_date_from_jd` (Sun sign ingress)
and `next_planet_entry_date_general` (general planet/nakshatra/raasi entry, `nakshathra` parameter
covers the Moon-nakshatra half of H-02 directly) - so Option B is a real, not merely assumed, path.
**A genuine, previously-unstated cost this inspection surfaced:** every one of these functions defaults
to `precision=0.1` (degrees) - about four orders of magnitude coarser than this engine's own residual
bound (`2.78e-8` degrees) and the H-02 defect's `1e-10` degree boundary-promotion window. Used at its
default, PyJHora's own search would not resolve the boundary any more precisely than the defect being
investigated, and could not serve as a meaningful independent check. `precision` is a caller-supplied
parameter (not hardcoded), so tightening it is possible, but PyJHora's own search loop (a simple
step-until-within-precision bisection-style walk, read directly in `next_planet_entry_date_general`'s
source) has not been verified to converge reliably at the precision this comparison would need - that
verification is itself part of Option B's cost, not a detail to discover mid-implementation.

**Option C. Both A and B**, since they check different things - A verifies the residual-vs-tolerance
mechanism itself (does perturbing the classifier by the stated ~278x margin actually flip the
classification, reproducing the *mechanism* the audit describes), while B verifies the *magnitude* of the
real-world impact (does an independently-computed oracle instant actually classify differently, at the
audit's claimed 17%/43% rate, or some other rate). Highest confidence, highest cost; matches this
repository's general pattern of combining an independent-reference validator with a genuine oracle gate
(the Gate B/E plus Gate F template) rather than choosing one or the other.

## 4. Recommendation

**Option C** (both), confidence: medium-high, revised down slightly from the first draft now that s3's
Option B cost is concretely known rather than assumed - tightening PyJHora's `precision` parameter and
verifying its search loop's convergence at that precision is real, scoped effort, not a large new
undertaking, but it is no longer a "fresh verification task" of unknown size; it is now a specific,
boundable one. The reasoning otherwise stands: this repository's own established methodology template -
"the varga template of frozen rule, second transcription, dense sweep, ULP battery, external oracle,
independent validator" (`Q8_CLOSURE_MATRIX.md` s4) - already implies exactly this combination for a
classification-seam defect of this kind, and G1's own finding is precise enough (a stated 278x tolerance
mismatch, exact measured percentages) that confirming both the mechanism and the real-world magnitude is
tractable at the same holdout scale this repository already certifies at (11-24 cases).

I would accept Option A alone if the owner judges the mechanism-level confirmation sufficient to satisfy
`ADR-0020` D5's "independently reproduced" bar without a fresh oracle-verification task - a legitimate,
lower-cost reading of "independently reproduced" that does not require B's additional PyJHora
verification effort.

## 5. What the decision must also settle, whichever reproduction option is chosen

Which of the three fix options (s2 item 2) is adopted, now that reproduction has confirmed the defect for
the Sun - s6 below performs the technical decision-readiness analysis and recommends Option 1, but the
choice itself remains the owner's, exactly as the original audit reserved it. Whether the
confirmation-or-refutation holdout is the G1 audit's own 2024
sample (already measured, but not independently reproduced) or a fresh, separately-selected one (avoiding
any risk of the reproduction unconsciously anchoring on the original figure). Whether a confirmed fix
requires its own FOUNDATION per-capability CEO checkpoint (`Q8_CLOSURE_MATRIX.md` s4), consistent with
every other certified capability this session, or is instead a correction to the existing `TRANSIT_V1`
certification requiring its own recertification discipline (`.claude/rules/certification.md`: "inside a
locked scope, a formal change decision and recertification"). Whether H-08's own convention decision
(named alongside H-02 in the Dasha roadmap's JATAKA entry criteria, `Q8_CLOSURE_MATRIX.md` s5) is related
enough to resolve together - out of scope for this paper to determine, named here only so it is not
silently conflated with H-02 later.

## 6. Fix-option decision-readiness analysis (2026-08-21)

H-02's reproduction methodology (s3) is complete and CI-confirmed (`ADR-0064`: Sun 2/12 exact match to
the original audit; Moon 15/34, comparable rate; PyJHora recorded as an evidenced limitation). This
section performs the narrow technical analysis the owner requested before choosing among the three fix
options s2 item 2 preserved from the original audit. **It recommends; it does not choose.**

**Exact affected interfaces, verified by direct inspection, not assumed:**
`engine/transits/crossing.py` `find_crossings()` (the certified event-finder: bisects to a
`REFINE_BRACKET_DAYS` = `1e-9` day bracket, reports `julian_day`, `residual_arcsec`,
`direction`); `engine/models/transit_event.py` `TransitEvent` (the frozen result dataclass: `body`,
`target_longitude`, `julian_day`, `direction`, `residual_arcsec`, `kind`, `profile_name` - no division
field exists today); `engine/transits/events.py` `sign_ingresses()`/`nakshatra_ingresses()` (thin
wrappers calling `find_crossings` once per boundary target, `_SIGN_BOUNDARIES`/`_NAKSHATRA_BOUNDARIES`);
`engine/astrology/longitude_utils.py` `division_index()`/`BOUNDARY_TOLERANCE` (the shared, engine-wide
classifier every division computation in the repository calls).

**Downstream consumers, verified by repository-wide search, not assumed:** `grep`-searched every
`.py` file for `TransitEvent`/`find_crossings`/`sign_ingresses`/`nakshatra_ingresses` imports outside
`engine/transits/` itself: the ONLY matches are `scripts/certify_transits.py`,
`validate_transits_holdout.py`, and this session's own H-02 investigation tooling
(`scripts/reproduce_h02_ingress_seam.py`, `validate_h02_reproduction.py`). **`engine.transits` has zero
production/domain consumers today** - no chart, dasha, panchanga, or report code calls it. This bounds
today's actual regression risk for Options 1 and 2 to `TRANSIT_V1`'s own certification, not to any live
feature. `division_index`, in sharp contrast, is imported by `engine/astrology/house.py`, `nakshatra.py`,
`pada.py`, `panchanga.py`, `signs.py`, and `varga_classifier.py` - i.e. essentially every certified
classification capability in the repository.

**Mathematical/semantic distinction that matters for all three options:** the H-02 seam exists only
where a longitude that is ITSELF the output of a residual-bounded search (`find_crossings`) is
re-classified by a tolerance-bounded classifier (`division_index`). Ordinary chart calculations
(a natal Moon's sign, a varga classification, a panchanga element at a given instant) classify a
directly-computed ephemeris longitude with no search residual involved, so they are not exposed to this
seam at all - confirmed by the same consumer search above finding no shared call path between
`find_crossings` and any of `division_index`'s many callers.

**Option 1 - explicit signed residual + declared division.** Add a new field to `TransitEvent` (e.g.
`declared_division`) computed once, at construction time, from `target_longitude` - which is EXACT (a
known boundary, `k*30` or `k*(40/3)`), never subject to residual noise - via the same classifier, rather
than re-classifying the noisy reported `julian_day`'s longitude after the fact. **Certified-value impact:
none** - `julian_day`, `residual_arcsec`, `direction` and every other existing field are unchanged;
this is a pure addition. **Blast radius: `TRANSIT_V1` only**, and within it, additive only - Gates A/B/C
(`certify_transits.py`) need no re-run of their existing assertions, only a new check that the added
field is populated correctly (trivial by construction, but must be tested, not assumed). **Regression
risk: near zero** - no existing certified value changes, and there are zero downstream consumers to
break. **Required tests:** a check that `declared_division == classify(target_longitude)` for every
holdout case; a negative control (deliberately omit or corrupt the field, confirm a test catches it).
**Certification/checkpoint requirement: a narrow `TRANSIT_V1` recertification addendum** (new field,
new gate assertion) - not a new FOUNDATION per-capability checkpoint (H-02 is a correction to an
already-certified capability under `ADR-0008`, not a new one), and not a Locked-scope change (`TRANSIT_V1`
is certified but not one of the four `docs/PROJECT_CONSTITUTION.md` s12 Locked artifacts).

**Option 2 - bias the returned event instant toward the target division.** Modify `find_crossings()`'s
bisection refinement so a residual that cannot reach exactly zero is deliberately resolved toward the
side that classifies into the searched-for division, for boundary-crossing calls specifically.
**Certified-value impact: real** - the reported `julian_day`/`residual_arcsec` for boundary-crossing
events would differ (at sub-microsecond scale) from today's certified values; this is a change to
`TRANSIT_V1`'s own certified algorithmic output, not an addition. **Blast radius: `TRANSIT_V1`'s Gates
A (residual battery), B (completeness), and C (oracle anchors)** - each would need a fresh run and
comparison against the certified holdout, since the very quantity they certify would change.
**A genuine architectural complication this analysis surfaces:** `find_crossings()` is also called
directly by `returns()` and `natal_conjunctions()` (`engine/transits/events.py`) with target longitudes
that are natal points, not division boundaries - "bias toward the target division" has no natural
meaning for those calls, so the bias logic would need to be scoped specifically to
`sign_ingresses`/`nakshatra_ingresses`' own boundary-target calls, adding conditional complexity to a
currently uniform, single-purpose primitive. **Required tests:** the full existing Gate A/B/C battery
re-run and compared; a new boundary test proving the bias activates only within the intended residual
window and never displaces an event by more than that window (an unbounded or over-eager bias would be
a worse defect than the one being fixed). **Certification/checkpoint requirement: a `TRANSIT_V1` formal
change decision and recertification** (`.claude/rules/certification.md`) - materially larger than
Option 1's, though still not Locked-scope.

**Option 3 - widen the classifier tolerance beyond the residual bound.** Change the single, engine-wide
`BOUNDARY_TOLERANCE` (`1e-10` degrees) to something `>= RESIDUAL_BOUND_ARCSEC`'s `2.78e-8` degrees.
**Certified-value impact: the most severe of the three, and global, not local.** `BOUNDARY_TOLERANCE` is
the ONE shared constant every division classification in the repository calls - not only H-02's own
Sun/nakshatra ingresses, but `house.py`, `pada.py`, `panchanga.py`, `signs.py`, and every certified varga
(`varga_classifier.py`, consumed by `certify_d2.py`/`d3`/`d7`/`d12`/`d30`). **Directly verified against
`docs/DECISION_LOG.md` `ADR-0005`/`ADR-0034`: Tier-0 is FORMALLY LOCKED with a scope that explicitly
names "the certified D9/D10 divisional mathematics"** - the same `division_index`/`BOUNDARY_TOLERANCE`
mechanism. Widening it would therefore modify a constant inside the repository's only `PROJECT_
CONSTITUTION.md` s12 Locked artifact, triggering the full four-condition Locked change-control discipline
`ADR-0034` itself required to establish the lock - not a `TRANSIT_V1`-scoped recertification, but
formally reopening Tier-0. Separately, and independent of the Locked question: a widened tolerance would
change classification for ANY boundary-adjacent value across the entire engine, including values that
were never near a search residual at all (e.g. a natal Moon computed directly, with no root-finding
involved) - `longitude_utils.py`'s own docstring states `1e-10` was chosen specifically because it is
tight enough to absorb only float-arithmetic noise (~`1e-13` degree scale) while remaining "six orders of
magnitude" inside the ephemeris's own `0.5` arcsec tolerance; widening by ~278x remains inside that
ephemeris bound but abandons the "only absorbs float noise, never an astronomically real difference"
property the current value was chosen to guarantee. **Blast radius: every certified capability in the
repository.** **Required tests:** full holdout recertification of every `division_index` consumer
(Tier-0, all five certified vargas, KP chain, sign convention, panchanga, `TRIKALAM_V1`), plus a new
negative control proving the widened tolerance still rejects a value that is astronomically
distinguishable from its boundary (a materially harder property to prove at a looser tolerance).
**Certification/checkpoint requirement: reopening the FORMALLY LOCKED Tier-0 scope** - categorically the
highest bar among the three options, and the only one touching a Locked artifact at all.

**Recommendation, evidence-based, not a choice on the owner's behalf: Option 1**, confidence high. It is
the only option with zero impact on any existing certified value, the smallest blast radius (`TRANSIT_V1`
alone, which today has zero production consumers to protect against regression in the first place), and
the lowest certification/governance bar (a narrow recertification addendum, not a formal-change decision
and not a Locked-scope reopening). Option 2 is a legitimate, more invasive alternative if the owner
judges an explicit `declared_division` field an insufficient fix (e.g. if a future consumer is expected
to read `julian_day` alone without checking the declared division) - its cost is well-bounded and
understood, just materially larger than Option 1's. **Option 3 is not recommended**: it is the only
option that touches the FORMALLY LOCKED Tier-0 scope, the only one with global (not local) blast radius,
and it fixes H-02's narrow seam by weakening the same guarantee for every other certified capability that
was never exposed to H-02's mechanism in the first place.

## 7. Change history

| Version | Date | Change |
|---|---|---|
| 1.2.0 | 2026-08-21 | Fix-option decision-readiness analysis (new s6): exact affected interfaces and downstream consumers verified by direct inspection (`engine.transits` has zero production consumers today; `division_index` is consumed by nearly every certified classifier). Mathematical/semantic, certification-impact, blast-radius, and required-test analysis for all three fix options. Verified against `ADR-0005`/`ADR-0034` that Option 3 would touch the FORMALLY LOCKED Tier-0 scope. Recommends Option 1 (confidence high); does not choose. |
| 1.1.0 | 2026-08-20 | Decision-readiness audit: re-verified `BOUNDARY_TOLERANCE`/`RESIDUAL_BOUND_ARCSEC` against the live codebase (unchanged since the 2026-08-11 audit). Directly inspected PyJHora 4.8.7's source (no execution needed) and confirmed Option B's ingress-detection API genuinely exists and is reachable, but surfaced a real, previously-unstated cost: its default `precision=0.1` degrees is ~4 orders of magnitude coarser than this defect's scale, so tightening it and verifying convergence is real, boundable effort. Research only; still presents options and decides nothing. |
| 1.0.0 | 2026-08-20 | Drafted per the owner's "ACE CONTINUE - AUTHORIZE H-02 DECISION PAPER" instruction, extracting `ADR-0020` D5's H-02 analysis. Presents options; decides nothing; does not ratify `ADR-0020`. |
