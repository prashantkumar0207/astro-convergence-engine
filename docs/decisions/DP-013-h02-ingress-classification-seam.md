<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and recommends one. DECIDES NOTHING. Requires owner approval. |
| Version | 1.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-20 |
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

Which of the three fix options (s2 item 2) is adopted if reproduction confirms the defect - this paper
does not recommend among them, since the original audit explicitly reserved that choice for the owner
and this paper's scope is limited to what `ADR-0020` D5 already analyzes, not to extending that analysis
with a new recommendation. Whether the confirmation-or-refutation holdout is the G1 audit's own 2024
sample (already measured, but not independently reproduced) or a fresh, separately-selected one (avoiding
any risk of the reproduction unconsciously anchoring on the original figure). Whether a confirmed fix
requires its own FOUNDATION per-capability CEO checkpoint (`Q8_CLOSURE_MATRIX.md` s4), consistent with
every other certified capability this session, or is instead a correction to the existing `TRANSIT_V1`
certification requiring its own recertification discipline (`.claude/rules/certification.md`: "inside a
locked scope, a formal change decision and recertification"). Whether H-08's own convention decision
(named alongside H-02 in the Dasha roadmap's JATAKA entry criteria, `Q8_CLOSURE_MATRIX.md` s5) is related
enough to resolve together - out of scope for this paper to determine, named here only so it is not
silently conflated with H-02 later.

## 6. Change history

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-08-20 | Decision-readiness audit: re-verified `BOUNDARY_TOLERANCE`/`RESIDUAL_BOUND_ARCSEC` against the live codebase (unchanged since the 2026-08-11 audit). Directly inspected PyJHora 4.8.7's source (no execution needed) and confirmed Option B's ingress-detection API genuinely exists and is reachable, but surfaced a real, previously-unstated cost: its default `precision=0.1` degrees is ~4 orders of magnitude coarser than this defect's scale, so tightening it and verifying convergence is real, boundable effort. Research only; still presents options and decides nothing. |
| 1.0.0 | 2026-08-20 | Drafted per the owner's "ACE CONTINUE - AUTHORIZE H-02 DECISION PAPER" instruction, extracting `ADR-0020` D5's H-02 analysis. Presents options; decides nothing; does not ratify `ADR-0020`. |
