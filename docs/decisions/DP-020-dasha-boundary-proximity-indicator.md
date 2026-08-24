<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ADDRESSED by ADR-0073** (2026-08-24) - owner ratified Option 1 (build the narrow, seed-only boundary-proximity field). This paper's own text is unedited below as the options record; see `ADR-0073` for the ratifying instruction and implementation record. |
| Version | 1.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-24 |
| Review cadence | TBD |

# DP-020. The dasha-specific boundary-proximity indicator (Dasha roadmap step 6, final JATAKA-entry
prerequisite) - whether and how to expose one

## 1. The question

`docs/DASHA_CERTIFICATION_ROADMAP.md` section 5 names "Add a boundary-proximity indicator to the
timeline" as step 6 of six - the last remaining `Q8_CLOSURE_MATRIX.md` s5 JATAKA-entry prerequisite.
Steps 1-5 (H-04, H-05, H-06, H-08, M-02) are already closed and CI-confirmed (`ADR-0053`, `ADR-0069`,
`ADR-0070`, `ADR-0071`, `ADR-0072`). This paper is the decision-readiness work for step 6, authorized by
the owner's explicit "AUTHORIZE FINAL DASHA-ROADMAP ITEM — DECISION-READINESS ONLY" instruction. It
investigates the exact capability the roadmap is asking for, what already exists that could be confused
with it, the legitimate treatment options, and their certification consequences - it does not implement
anything, does not choose an option, and does not authorize general JATAKA implementation.

**This item is not `DP-015`/`ADR-0067`'s own boundary-proximity item, and this paper does not reopen
that one.** `DP-015` investigated a *different*, FOUNDATION-scope requirement (`Q8_CLOSURE_MATRIX.md` s4:
"Boundary-proximity indicators where sensitivity warrants," a capability-agnostic FOUNDATION
implementation-scope line covering rise/set, panchanga, trikalam, etc.) and was decoupled from the
FOUNDATION-exit checkpoint by `ADR-0067`'s ratification of "Option 3 (AMENDED)." That decision is already
final and is not revisited here. It is, however, directly relevant precedent - see section E.

## 2. What is already established, and what is not

**Established (direct citation and direct code/data inspection this session, not re-derived from the
roadmap document alone):**

- `docs/DASHA_CERTIFICATION_ROADMAP.md` section 4, quoted in full: "**Boundary sensitivity as an
  output.** The KP layer exposes a boundary-proximity indicator precisely so consumers can flag critical
  classifications. The dasha layer, where the amplification is hundreds of days per degree, exposes
  nothing equivalent. This is arguably the single most valuable addition for BTR." Section 1's own
  numerical framing: Moon longitude error propagates to dasha dates at `lord_years * 365.256364 /
  (40/3)` days per degree - "164 days per degree for a Sun-lord seed, 192 for Ketu or Mars, and 548 days
  per degree for Venus." Section 5's own sequencing note: "Steps 1 through 6 change no calculated
  value" - step 6 is explicitly meant to be additive, matching every other step already closed this
  session.
- **`Q8_CLOSURE_MATRIX.md` s5's own JATAKA entry-criteria text, re-read fresh:** "The Dasha roadmap's
  steps 1 to 6 complete: depth-3 gate, frozen dasha baseline, profile allow-list, the H-08 convention
  decision, near-boundary Moon cases, boundary-proximity indicator." A plain, non-alternative six-item
  list - the same textual structure `DP-016`/`DP-017`/`DP-018`/`DP-019` already independently confirmed,
  each time, gives no `DP-015`-style carve-out opening. **This is a materially different situation from
  `DP-015`'s own FOUNDATION-exit text**, which explicitly named a deferral-with-blocking clause for
  H-01/H-02 specifically - JATAKA's own six-step list carries no equivalent clause. Deferring step 6
  would not close this entry criterion the way `ADR-0067` closed the FOUNDATION-scope item; it would
  leave JATAKA blocked.
- **KP's own boundary-proximity indicator, directly inspected:** `engine/kp/chain.py`'s `kp_chain()`
  computes `nearest_boundary_arcsec = min(distance to nakshatra edge, distance to sub edge, distance to
  sub-sub edge) * 3600`, exposed on `KpChain.nearest_boundary_arcsec`. **This indicator has its own
  known, unresolved completeness defect - H-07** (`reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`):
  the minimum omits the 30-degree sign-boundary term entirely, despite the field's own docstring
  (`engine/models/kp_chain.py:37-41`) claiming coverage "at any level." **Independently reproduced live
  this session, exactly matching the audit's own reported case:** `kp_chain(29.999999999)` returns
  `sign_lord='Ma'` with `nearest_boundary_arcsec=380.0000036` - a few microarcseconds from the sign lord
  flipping, while the safety indicator itself reports 380 arcsec of margin. H-07 remains open, is not
  part of the Dasha roadmap's six steps, and is not addressed by this paper.
- **No boundary-proximity signal currently exists on `VimshottariTimeline`**, confirmed by direct
  inspection of every field: `school`, `dasha_profile_name`, `year_length_days`, `birth_jd`, `anchor_jd`,
  `seed_moon_longitude`, `seed_nakshatra_number`, `seed_lord`, `seed_elapsed_fraction`, `balance_years`,
  `periods`, `provenance`, `seed_boundary_convention` (`H-08`, `ADR-0071`). None of these is a
  proximity/distance-to-boundary measurement.
- **A related, already-existing signal that must NOT be silently treated as equivalent (this paper's
  answer to the owner's own item 8):** `seed_elapsed_fraction` is the exact fractional position of the
  birth Moon within its nakshatra, already certified and already exposed. A distance-to-boundary value
  is **exactly and losslessly derivable from it** (`min(elapsed, 1 - elapsed) * NAK_SPAN` degrees) -
  verified directly this session: for one of M-02's own near-boundary cases (`B1_lahiri_boundary_before`,
  Moon `119.95579900`), `seed_elapsed_fraction` yields a derived distance of `0.044201` degrees,
  matching a direct measurement of the same Moon longitude to nine decimal places. **But nothing today
  performs, documents, or certifies this derivation as a safety signal** - a consumer would have to know
  to do it themselves, with no field name, docstring, or certification artifact telling them it exists or
  what its own scope is (unlike KP's `nearest_boundary_arcsec`, which is purpose-built and documented,
  even though H-07 shows that documentation currently overclaims). `seed_boundary_convention` (`H-08`)
  is a second, differently-purposed signal that must also not be conflated: it names *which rule* was
  used for boundary ownership, not *how close* the classification came to flipping.
- **A second related, freshly-created signal from this session's own M-02 work, also not to be
  confused:** `scripts/certify_vimshottari.py`'s `run_case()` now computes and records `moon_distance_
  to_nearest_boundary_deg` per case (`ADR-0072`) - this is a **certifier-script-only diagnostic**, used
  to verify M-02's own near-boundary holdout cases are genuinely near a boundary. It is not exposed on
  `VimshottariTimeline`, is not part of any production API, and is not itself a certified consumer-facing
  indicator.
- **`DP-015`/`ADR-0067`'s own already-ratified "Option 3 (AMENDED)" is directly relevant, forward-binding
  precedent, not something this paper re-derives:** its item 4 states "No future production capability
  may consume a boundary-proximity signal, for any FOUNDATION-tier or later-phase output, as if it were
  certified" and its item 5 requires any future consumer to either certify the methodology first or
  explicitly refuse/gate the dependency. Its item 8 anticipated "a future decision paper... when a
  consuming feature (chiefly BTR...) actually needs one" - **this paper is squarely that kind of
  follow-up, for the dasha-specific instance the Dasha roadmap's own step 6 names**, not a reopening of
  `ADR-0067` itself.
- **No current consumer of a dasha boundary-proximity signal exists**, confirmed directly: `docs/
  Q8_CLOSURE_MATRIX.md` places BTR (the roadmap's own stated motivating consumer) at section 13, "not a
  phase," becoming possible "once EVIDENCE... decision" - EVIDENCE itself requires JATAKA exit first, and
  JATAKA has not even been entered (blocked on this very item). This exactly mirrors `DP-015`'s own
  finding for the FOUNDATION-scope item ("no current consumer exists") - independently re-confirmed here
  for the dasha-specific case, not assumed from the earlier paper.
- **`docs/DASHA_CERTIFICATION_ROADMAP.md` section 4 treats "Boundary sensitivity as an output" and
  "Boundaries in time" as two textually separate groups.** "Boundaries in time" - an explicit
  interval-membership convention for period *transitions* ("nothing decides which period owns an instant
  equal to it") - is a materially different, deeper problem, and is **not named anywhere in the roadmap's
  numbered six-step sequence** (`section 5`). Step 6 is specifically "Boundary sensitivity as an output"
  - the *seed* classification's own spatial (degree) proximity to a nakshatra boundary, the direct
  analogue of KP's existing indicator - not a period-transition membership rule. This paper is scoped to
  step 6 only; "Boundaries in time" remains a separate, not-yet-authorized, not-required-for-JATAKA-entry
  problem.
- **No prior ADR or decision paper addresses the dasha-specific boundary-proximity indicator.** Confirmed
  by direct search of `docs/DECISION_LOG.md` and `docs/decisions/`: every existing citation either names
  it as an open roadmap step (this session's own `DP-016` through `DP-019`) or is `DP-015`/`ADR-0067`'s
  own, textually distinct, already-closed FOUNDATION-scope item.

**Not established (explicitly not decided by this paper):** whether a boundary-proximity field is built
for the dasha layer; what it would be named or exactly compute; whether it includes only the raw
degree/arcsec distance or also a dasha-specific amplified (days-of-uncertainty) figure; whether
`seed_elapsed_fraction`'s own documentation is updated to warn against ad hoc derivation.

## A. What the indicator is intended to mean, and what claim it would make

Per the roadmap's own framing, a dasha boundary-proximity indicator would tell a consumer: "how close was
this chart's seed classification to a nakshatra boundary, and therefore how sensitive is this chart's
entire mahadasha sequence to small errors or ambiguity in the birth Moon's position." Unlike KP's own
indicator (which reports proximity to *any* of four classification levels - sign, nakshatra, sub,
sub-sub), the dasha-relevant boundary is specifically the **nakshatra** boundary, since that is the only
classification that determines `seed_lord` and therefore the entire mahadasha/antardasha/pratyantardasha
structure. The roadmap's own emphasis on "amplification... hundreds of days per degree" suggests the
indicator's *value* lies not merely in reporting a degree/arcsec distance (a spatial quantity any
consumer could, in principle, already derive from `seed_elapsed_fraction`) but in making the
**dasha-specific consequence** of that proximity legible - the amount of calendar-date uncertainty a
given proximity represents, which requires the roadmap's own lord-specific days-per-degree multiplier and
is not otherwise obvious from a raw degree figure.

## B. Whether the current architecture already has a related signal that must not be silently treated
as equivalent

**Yes, two, both directly investigated in section 2 above:** `seed_elapsed_fraction` (an exact,
certified, but purpose-agnostic field from which a proximity value is losslessly derivable, but which is
not documented, named, or certified for that purpose) and `moon_distance_to_nearest_boundary_deg` (a
certifier-script-only diagnostic added this session for M-02, not a production or certified signal).
Neither may be silently treated as the dasha boundary-proximity indicator the roadmap's step 6 calls for
- both lack the purpose-built naming, documentation, and (if built) certification a genuine indicator
requires, matching `DP-015`/`ADR-0067`'s own forward-binding rule that no signal may be consumed as
certified without either certifying it first or explicitly refusing/gating it.

## C. Classification

**A combination: primarily a missing capability, with a secondary methodology gap - not a calculation
defect, and not itself a certification gap in the sense of an unverified existing claim, since nothing
currently claims to provide this signal.** Three aspects, worth keeping distinct:

1. **Missing capability:** no field, on `VimshottariTimeline` or elsewhere, currently exposes a
   boundary-proximity value for the dasha layer, purpose-built or otherwise.
2. **Methodology gap:** even if built, *what* it should measure (raw degrees only, or also a dasha-
   specific amplified days-of-uncertainty figure) is not specified anywhere, and inventing that
   methodology unilaterally would repeat the exact failure mode this session has been instructed to avoid
   throughout (choosing a convention without owner authorization).
3. **A precedent-quality gap, worth naming explicitly:** the most obvious existing pattern to mirror
   (KP's own `nearest_boundary_arcsec`) carries a known, unresolved completeness defect (H-07) - a
   genuine risk if "mirror the KP pattern" were applied mechanically, per the owner's own explicit
   caution (item 13).

## D. Whether existing certified Vimshottari values are affected

**No, under every option this paper considers.** A boundary-proximity field, however scoped, would be
computed from data already certified and already exact (`seed_elapsed_fraction`, or the underlying
`seed_moon_longitude`) - a pure re-expression, not a new calculation path, matching the roadmap's own
explicit "Steps 1 through 6 change no calculated value" framing and every other step already closed this
session.

## E. Precedents reviewed (H-05, H-06, H-08, M-02) - what applies, and what does not

- **H-05** (`ADR-0069`): a coverage gap closed by adding a new, frozen, hermetic baseline with a genuine
  negative control, zero certified-value impact. *Applies* as a verification-shape precedent if a field
  is built: pinning the field's own reported values for known cases (including the six near-boundary
  cases M-02 already built) would directly mirror this pattern. *Does not apply* to the prior question of
  whether to build the field at all - H-05 closed a gap in testing an *existing* computation, not in
  deciding whether to add a new capability.
- **H-06** (`ADR-0070`): a missing-guard gap closed by mirroring an *existing, certified* pattern (the
  varga registry) closely. *Applies* as the general shape "when this project adds a protective or
  informational layer, it usually mirrors an existing certified precedent" - and the most directly
  analogous existing precedent here is KP's own `nearest_boundary_arcsec`. **Explicitly not mechanically
  copied**, per the owner's own instruction: H-07 shows that exact precedent has an unresolved scope-
  overclaim defect, so copying it as-is would import a known defect into a new capability rather than
  avoid one.
- **H-08** (`ADR-0071`): a convention/documentation gap closed by (i) ratifying the status quo explicitly
  and (ii) adding a small, additive, well-documented **disclosure field** (`seed_boundary_convention`)
  mirroring `ADR-0065`'s own `TransitEvent.declared_division` precedent. *Applies directly*: this is the
  most structurally similar precedent to what a dasha boundary-proximity field would actually be - a
  small, additive, purpose-scoped field disclosing a fact about the seed classification, with zero
  calculated-value impact. Its own careful, narrow scoping (explicitly documenting what the field does
  and does not cover) is the direct antidote to H-07's own overclaim problem, if Option 1 below is
  chosen.
- **M-02** (`ADR-0072`): a holdout-coverage gap closed by root-finding *genuine* near-boundary cases via
  the already-certified `engine.transits.crossing.find_crossings()`, plus a certifier-script diagnostic
  (`moon_distance_to_nearest_boundary_deg`) computed per case. *Applies directly and concretely*: the six
  `BOUNDARY_HOLDOUT` cases M-02 already built are, by construction, real, oracle-verified, genuinely
  near-boundary Vimshottari timelines - the natural, already-available test data for certifying any new
  boundary-proximity field's own correctness, requiring no new case construction if Option 1 is chosen.

## F. All legitimate treatment options

### Option 1 - Build and certify a purpose-built, seed-only boundary-proximity field

Add a new, additive field to `VimshottariTimeline` (e.g. `seed_boundary_distance_arcsec` or similarly
named) reporting the exact distance from the birth Moon to the nearest nakshatra boundary, computed as a
direct, lossless re-expression of the already-certified `seed_elapsed_fraction` (verified this session:
zero new astronomical calculation required). Scoped explicitly and narrowly - **learning directly from
H-07's own defect** - to cover only the nakshatra (seed) boundary, with an explicit docstring stating
what it does *not* cover (deeper antardasha/pratyantardasha period-transition boundaries; the KP layer's
own sign/sub/sub-sub levels), so the field cannot silently overclaim the way `nearest_boundary_arcsec`'s
own docstring currently does. Certified via a new oracle/hermetic battery reusing M-02's own six
`BOUNDARY_HOLDOUT` cases (already root-found, already oracle-verified) to assert the new field's reported
value matches an independently-measured distance for each.

**Two genuinely open sub-questions this paper surfaces but does not resolve:**
- **Raw distance only, or also a dasha-specific amplified figure** (a "days of dasha-date uncertainty"
  value using the roadmap's own lord-specific multiplier)? The roadmap's own framing suggests the
  amplified figure is what makes this valuable for BTR, but choosing its exact formula, rounding, and
  presentation is a genuine design decision this paper does not make unilaterally.
- **Field naming and units** (arcsec, matching KP's own convention, or degrees, matching this session's
  own M-02 diagnostic) - a small but real consistency choice.

- **Certification implications:** additive only - a new field, a new (or extended) test/certification
  battery reusing existing `BOUNDARY_HOLDOUT` evidence; no schema-breaking change; no existing certified
  figure changes.
- **Blast radius:** `engine/models/dasha.py` (one new field), `engine/dasha/vimshottari.py` (populate it
  at the existing computation point), `engine/tests/` and/or `scripts/certify_vimshottari.py` (new
  assertions reusing M-02's own cases). No change to `engine/kp/`, `engine/astrology/`, or any other
  capability.
- **Certified-value impact:** **none** - confirmed directly, matching every other step this session
  closed.

### Option 2 - Option 1 plus the dasha-specific amplified (days-of-uncertainty) figure, resolved now

Build both the raw distance and the amplified days-of-uncertainty figure in the same pass, resolving
Option 1's first sub-question rather than leaving it open.

- **Advantages:** delivers the roadmap's own stated highest-value framing directly, in one step.
- **Disadvantages:** requires choosing a specific formula/convention now (which lord's own multiplier
  applies; how it is rounded/presented) without a dedicated sub-decision - a materially larger, less
  narrow scope than Option 1, and closer to the "invent a convention without authorization" risk this
  session has been repeatedly instructed to avoid.
- **Certification implications / blast radius / certified-value impact:** same as Option 1, plus the
  additional formula-choice surface.

### Option 3 - Disclosure-only, mirroring H-08's own status-quo-plus-documentation shape

Build no new field. Instead, explicitly document (in `VimshottariTimeline`'s own docstring, and in
`certification/VIMSHOTTARI_V1_certification.json`'s `explicit_non_claims`) that no boundary-proximity
signal exists for the dasha layer today, that `seed_elapsed_fraction` is **not** a certified proximity
indicator and must not be derived-and-used as one without its own certification, and record the
dasha-specific application of `DP-015`/`ADR-0067`'s own already-ratified forward-binding rule (certify
first, or explicitly refuse/gate) locally and discoverably in the Dasha roadmap's own status.

- **Advantages:** near-zero implementation cost; consistent with the project's own existing, already-
  ratified project-wide rule (which already covers this in principle); removes the "silent conflation"
  risk (section B) without committing to a specific field design prematurely.
- **Disadvantages:** does **not**, by itself, satisfy `Q8_CLOSURE_MATRIX.md` s5's own plain wording
  ("boundary-proximity indicator" as one of six required, completed steps) unless the owner explicitly
  rules, as was done for `DP-015`'s own FOUNDATION-scope item, that documentation-plus-forward-binding
  constitutes "complete" for this step too - and, per section 2's own finding, JATAKA's entry-criteria
  text carries no textual carve-out equivalent to FOUNDATION's, so that ruling would be a fresh
  interpretive act, not a mechanical extension of `ADR-0067`.
- **Certification implications:** metadata-only.
- **Blast radius:** documentation only.
- **Certified-value impact:** none.

### Option 4 - Explicit refusal mechanism

Add a guard (mirroring `UnsupportedVargaError`/`UnsupportedNodePolicyError`'s own established refusal
pattern) that would raise if some future code path attempted to consume a boundary-proximity signal
without it being certified.

- **Advantages:** matches the roadmap's own "certify first, or explicitly refuse" framing literally.
- **Disadvantages:** **no current call site exists to attach a refusal to** (section 2's own finding: no
  consumer exists yet) - this option would add unreachable, untriggered code today, a weaker and more
  speculative choice than Option 3's pure documentation, which achieves the same practical protection
  without dead code.
- **Certification implications / blast radius:** small, but for a mechanism with nothing to guard yet.
- **Certified-value impact:** none.

### Option 5 - Defer entirely, matching DP-015's own FOUNDATION-scope treatment

Record an explicit deferral for the dasha-specific indicator too, following the same reasoning `DP-015`
used for the FOUNDATION-scope item (no current consumer; "arguably valuable," not "required now"
language).

- **Advantages:** zero implementation cost; a legitimate, evidence-supported reading of the same
  underlying facts (no consumer exists) that already persuaded the owner once this session.
- **Disadvantages, materially different from `DP-015`'s own context:** `Q8_CLOSURE_MATRIX.md` s5's JATAKA
  entry-criteria text has **no** deferral-with-blocking carve-out clause of the kind FOUNDATION's own
  text had for H-01/H-02 - `DP-016` through `DP-019` each independently confirmed this same plain,
  non-alternative six-step wording. Deferring step 6 would **not** close this JATAKA entry criterion the
  way `ADR-0067` closed the analogous FOUNDATION-exit item; it would leave JATAKA blocked indefinitely,
  not merely delay one optional enhancement. If JATAKA entry is a goal, deferral does not substitute for
  building or explicitly documenting something under this step - it only postpones the step itself.
- **Certification implications / blast radius / certified-value impact:** none.

## G. Recommendation

**Option 1, at medium confidence**, with Option 3 as a legitimate, lower-cost fallback if the owner
prefers not to commit to a field design yet. Reasoning: (i) Option 1's technical cost is genuinely low -
zero new calculation (verified directly this session), zero certified-value impact, and the certification
evidence (M-02's own six `BOUNDARY_HOLDOUT` cases) already exists and needs no new construction; (ii) it
directly satisfies `Q8_CLOSURE_MATRIX.md` s5's plain wording without requiring a fresh interpretive
carve-out ruling, unlike Option 3 or Option 5; (iii) narrowly scoping it (learning explicitly from H-07's
own overclaim defect) avoids mechanically copying a known-flawed precedent, per the owner's own explicit
caution; (iv) Option 2's added amplification-formula design question is real value but a materially
larger, less narrow commitment than this decision-readiness stage should resolve unilaterally - better
surfaced as an explicit sub-question for the owner, as done here, than decided by the builder. Option 3
remains fully legitimate if the owner judges a field design is premature before any real consumer exists,
matching `DP-015`'s own precedent almost exactly - the two options differ mainly in whether the owner
wants to close this JATAKA-entry step now or accept it stays open pending a fresh interpretive ruling.
Option 5 is not recommended given section F's own finding that it does not, by itself, unblock JATAKA the
way `DP-015`'s equivalent choice unblocked FOUNDATION.

**Confidence: medium.** Lower than `DP-018`'s own H-08 lean (where the zero-impact option left almost no
open design question) because Option 1 still carries two genuine open sub-questions (amplification
figure; field naming/units) that materially affect its final shape, even though the core "should a field
exist" question is well-supported by the evidence gathered this session.

## H. What is NOT being decided by this paper

Whether a boundary-proximity field is built for the dasha layer, or which option governs it; the field's
exact name, units, or whether it includes an amplified days-of-uncertainty figure; whether `seed_
elapsed_fraction`'s own documentation is updated. `DP-015`/`ADR-0067`'s own FOUNDATION-scope
boundary-proximity decision is not reopened or reconsidered. H-04, H-05, H-06, H-08, and M-02 (`ADR-0053`,
`ADR-0069`, `ADR-0070`, `ADR-0071`, `ADR-0072`) remain exactly as ratified - none is reopened. The eight
cross-certifier `H10`/`H11` findings `ADR-0072` flagged remain untouched and unaddressed here, exactly as
recorded - a separate, future item. General JATAKA implementation is not authorized or begun. FOUNDATION
is not reopened.

## I. Exact CEO/owner decision required

Select Option 1 (build and certify a narrowly-scoped, seed-only boundary-proximity field, reusing M-02's
own near-boundary evidence, with the amplification-figure and naming sub-questions either resolved now or
left to implementation-time judgment), Option 2 (Option 1 plus the amplified days-of-uncertainty figure,
resolved now), Option 3 (disclosure-only, no new field, matching `DP-015`'s own status-quo-plus-
documentation shape - requires the owner's own fresh interpretive ruling that this satisfies
`Q8_CLOSURE_MATRIX.md` s5's step 6), Option 4 (an explicit but currently-unreachable refusal mechanism),
or Option 5 (defer - does not by itself unblock JATAKA entry, per section F) for the dasha-specific
boundary-proximity indicator. Recorded as a new, numbered decision-log entry citing this paper - this
paper alone authorizes nothing, and does not authorize general JATAKA implementation, does not reopen
`DP-015`/`ADR-0067`, and does not touch H-04/H-05/H-06/H-08/M-02 or the eight flagged cross-certifier
findings.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-08-24 | Marked ADDRESSED by `ADR-0073` (Option 1 accepted and implemented: `VimshottariTimeline.seed_nakshatra_boundary_arcsec`, an exact re-expression of `seed_elapsed_fraction`, closing the Dasha roadmap's sixth and final step). Paper's substantive text below unchanged. |
| 1.0.0 | 2026-08-24 | Created. Fifth authorized JATAKA-entry-prerequisite decision-readiness paper, and the sixth and final Dasha-roadmap step, extracting `docs/DASHA_CERTIFICATION_ROADMAP.md` step 6 with every claim independently re-verified against the live `engine/kp/chain.py`, `engine/models/dasha.py`, `scripts/certify_vimshottari.py`, and `docs/Q8_CLOSURE_MATRIX.md`/`DASHA_CERTIFICATION_ROADMAP.md` - not trusted from either document's own summary. Independently reproduced H-07's own KP boundary-indicator completeness defect live (`kp_chain(29.999999999)`: `sign_lord='Ma'`, `nearest_boundary_arcsec=380.0000036`), confirmed no boundary-proximity signal exists on `VimshottariTimeline` today, and confirmed a proximity value is exactly and losslessly derivable from the already-certified `seed_elapsed_fraction` with zero new calculation - identifying this, and M-02's own certifier-only diagnostic field, as related signals that must not be silently treated as a certified indicator (item 8). Explicitly distinguished this item from `DP-015`/`ADR-0067`'s own FOUNDATION-scope boundary-proximity item, confirming the latter's forward-binding rule applies here without being reopened. Confirmed JATAKA's own entry-criteria text carries no deferral-with-blocking carve-out of the kind FOUNDATION's had, so deferral does not by itself unblock JATAKA the way it unblocked FOUNDATION. Reviewed H-05/H-06/H-08/M-02 as precedents per the owner's own item 13, explicitly declining to mechanically copy KP's own flawed `nearest_boundary_arcsec` pattern. Classifies the item as a missing capability plus a methodology gap, not a defect. Presents five options (build a narrow seed-only field, reusing M-02's own evidence; build it plus an amplified days-of-uncertainty figure; disclosure-only; an unreachable refusal mechanism; defer), medium-confidence lean toward Option 1. Options only; decides nothing; not implementation-authorized. |
