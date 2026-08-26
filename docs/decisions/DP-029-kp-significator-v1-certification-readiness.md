<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents readiness state and options. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-26 |
| Review cadence | TBD |

# DP-029. `KP_SIGNIFICATOR_V1` certification-readiness

## 0. Authorization and scope

Authorized by "CEO AUTHORIZATION — KP_SIGNIFICATOR_V1 CERTIFICATION-READINESS": continue from
`docs/KP_SIGNIFICATOR_SPEC.md` v0.2.0 (commit `923c6b6`); methodology is treated as **already approved
for this investigation** and is **not** re-researched: primary K.S. Krishnamurti Reader II-IV evidence
accepted; V1 = narrow 7th-cusp marriage promise/denial judgment; positive houses 2/7/11; negative houses
1/6/10/12; strength order star-of-occupant > occupant > star-of-owner > owner; retrograde/node rules
frozen as documented (`KP_SIGNIFICATOR_SPEC.md` sections 19.1-19.3); the horary-to-natal application is
an explicitly disclosed inference/non-claim. This paper investigates **certification feasibility only**:
what inputs V1 needs, what already exists, what's genuinely new, oracle availability, test-corpus and
certification design, and comparison to existing patterns. It does not implement anything, does not
execute certification, does not create `engine/kp/significators.py`, and does not push or merge.

## 1. Exact production inputs `KP_SIGNIFICATOR_V1` requires

For the 7th cusp of a natal chart, under the `KP_KRISHNAMURTI` profile:
1. The 7th cusp's own longitude and its KP chain (SL/NL/SB/SS) - to get the cuspal sub-lord planet.
2. For every planet (to evaluate what the sub-lord planet itself signifies, per Ordering A): its
   longitude, its own KP chain (SL/NL/SB/SS), its house occupancy (which of the 12 houses it falls in),
   its retrograde/direct status.
3. A classical sign-lordship table (which planet rules which sign - to determine "owner of a house").
4. For the Rahu/Ketu-as-sub-lord case specifically: conjunction and aspect determination against other
   planets (the substitution rule, section 19.3) - and, absent either, the sign lord fallback (already
   covered by item 3).
5. Provenance carrying the `KP_KRISHNAMURTI` profile identity through to the result, per this project's
   own established disclosure pattern.

## 2. Which inputs are already certified

Verified directly against the code, not assumed:

- **Cusp SL/NL/SB/SS** - `engine/kp/chart.py::kp_chart()`/`kp_chart_from_snapshot()` already builds all
  twelve `KpCusp` entries with their own chain, via the already-certified `KP_CHAIN_V1`
  (`certification/KP_CHAIN_V1_certification.json`, `ADR-0006`). The 7th cusp's sub-lord is directly
  available at `kp_chart(...).cusps[6].chain.sub_lord` - **zero new astronomical calculation**.
- **Planet SL/NL/SB/SS** - same `KP_CHAIN_V1` substrate, already computed for every body in `kp_chart()`.
- **Sign-lordship table** - `engine/astrology/sign_lord.py::SIGN_LORDS`/`sign_lord()`, already
  cross-validated against KP's own separate `engine/kp/tables.py::KP_SIGN_LORDS` per
  `docs/KP_CHAIN_SPEC.md` §7's own consistency test. **Reusable as-is.**
- **Retrograde status** - not a stored field on the base planet-position model, but an already-
  established, already-used derivation convention (`speed_longitude < 0`), present today on `KpBody`
  itself (`engine/kp/chart.py`) and on `ChartPlanet` (`engine/astrology/chart_planet_builder.py`).
  **Zero new calculation, reuses an existing convention.**
- **House cusp system** - confirmed Placidus (`engine/astronomy/profile.py::KP_KRISHNAMURTI`,
  `house_system=b"P"`), matching `KP_CHAIN_V1`'s own profile exactly. Placidus is `PARTIALLY_CERTIFIED`
  per `certification/ENGINE_CAPABILITY_INVENTORY.json` (exercised only to 64.1°N/S, per `DP-025`, still
  `Status: OPEN`, not reopened by this paper) - the same disclosed polar non-claim
  `KP_SIGNIFICATOR_SPEC.md` section 7/16 already plans to carry.

## 3. What is genuinely new

Three things, precisely scoped:

1. **The significator-determination algorithm** (Ordering A applied to a target house: union of {star of
   occupant, occupant, star of owner, owner}, in that strength order) - new code, but low-ambiguity, fully
   specified by the frozen methodology. Consumes only already-certified inputs (section 2).
2. **The cuspal-sub-lord promise/deny judgment** (does the sub-lord's own signification set intersect
   {2,7,11} vs. only {1,6,10,12}) - new code, low-ambiguity, fully specified.
3. **A conjunction/aspect determination for the Rahu/Ketu-as-sub-lord substitution rule** - genuinely
   open, not merely new code:
   - **No conjunction-orb definition exists anywhere in the certified engine.** The only existing
     "conjunction"-adjacent logic (`engine/transits/events.py`) is a moving-body-crosses-a-longitude
     transit event, not a natal planet-planet orb test. No orb value was found in the retrieved primary
     text either (section 8 below).
   - **Graha drishti (aspects) is certified but profile-locked, not reusable as-is.**
     `engine/parashari/drishti.py::graha_drishti_from_snapshot()` is `PARASHARI_DRISHTI_V1`
     (`ADR-0012`/`ADR-0036`), and **raises `ParashariProfileError` unless
     `provenance.profile_name == "parashari_lahiri"`** - it cannot be called on a `KP_KRISHNAMURTI`
     snapshot without either (a) a new decision to extend its profile lock to also accept KP profiles, an
     edit to a certified capability, or (b) a fresh, KP-scoped aspect calculation duplicating the same
     classical angle rules under KP's own isolation discipline. `DP-025` also flags `PARASHARI_DRISHTI_V1`'s
     own `provenance.house_system` field as mislabeled ("P" despite computing whole-sign houses) - a
     pre-existing, unrelated defect, noted only so it is not mistaken for evidence either way here.
   - This substitution rule is **not a rare edge case**: KP's own nine-lord sub-lord cycle gives Rahu and
     Ketu a combined, non-trivial share of possible sub-lords across the zodiac (their combined nakshatra
     span, per `docs/KP_CHAIN_SPEC.md`'s own table, is a meaningful fraction of the full cycle) - a
     dense sweep across the 7th cusp's possible longitudes will genuinely land on a node sub-lord in a
     material share of cases, not a negligible tail. Silently excluding it would be a scope narrowing that
     needs owner sign-off, not a detail to skip past.

**House occupancy** (which of the 12 houses a planet falls in) already exists
(`engine/astrology/house.py::whole_sign_house()`/`equal_house_from_ascendant()`, used by
`chart_planet_builder.py`) but is exercised today only inside Parashari/whole-sign-house chart building.
The function itself takes raw `(longitude, ascendant)`, not a profile-tagged snapshot, and appears
profile-agnostic in its own signature - unlike `graha_drishti_from_snapshot()`/`kp_chart()`, which both
validate the snapshot's profile before running. This is a real distinction worth the owner's own
confirmation before certification design assumes it: **is `whole_sign_house()` safe to call directly on
KP/Krishnamurti-ayanamsa longitudes because the math is profile-agnostic, or does reusing it under KP
require its own explicit decision**, the way `graha_drishti_from_snapshot()`'s reuse would? This paper
does not decide it; flagged as part of the certification-design work, not a blocker on its own (either
answer is straightforward to execute once chosen).

## 4. Oracle availability

**Confirmed: no computational oracle exists for KP significators**, reaffirming `DP-028` section D's own
finding and the explicit instruction not to assume PyJHora is one - PyJHora's only KP-adjacent function
(`utils.py::kp_lords_for_longitude()`) is a generic lordship-chain calculator, not a significator/
promise-deny function. No other external astrology library or service was identified this task as a
significator-determination oracle (none was searched for again this task, per the instruction not to
re-investigate methodology - this restates `DP-028`'s already-established finding, not new research).

## 5. Certification strategy given no oracle

The only defensible strategy is the one the instruction itself names: **independent-from-scratch
derivation + primary-source rule verification + protected holdout** - the same category of approach
already used for `D45`'s own independent validator (`validate_d45_holdout.py`) and `KP_CHAIN_V1`'s own
(`validate_kp_holdout.py`), but here **without** either of those capabilities' own additional oracle
corroboration (D45 had PyJHora cross-checks; `KP_CHAIN_V1` had the separately-authored `legacy/kp.py`
kernel as an equivalence oracle). Concretely:
1. Production code implements the frozen rule (Ordering A, promise/deny house sets, retrograde
   disclosure, node substitution) directly against `KP_CHAIN_V1`'s and the other already-certified
   substrates named in section 2.
2. An independent validator re-derives the same rule from scratch, in its own code, importing nothing
   from the production module (mirroring the D45/`KP_CHAIN_V1` precedent's own isolation discipline).
3. A dense sweep drives the 7th cusp through the full 360° zodiac, comparing production against the
   independent validator with zero-mismatch tolerance (per root `DECISION_LOG.md` `D-003`'s own zero
   categorical tolerance standard for the KP hierarchy generally).
4. A protected holdout, prime-step sampled and independent of the dense sweep, per the established
   pattern.
5. Genuine negative controls (planted mutations, confirmed detected) - see section 9.

## 6. Test corpus design

- **Positive cases**: 7th-cusp longitudes whose sub-lord's own significations include 2, 7, or 11.
- **Negative cases**: 7th-cusp longitudes whose sub-lord's own significations are confined to
  {1, 6, 10, 12} - and, per `D-003`'s zero-tolerance standard, cases whose sub-lord signifies *neither*
  set fully must be explicitly categorized (undetermined/mixed), not silently forced into one bucket.
- **Boundary cases**: longitudes at/adjacent to `KP_CHAIN_V1`'s own already-documented sub-boundary
  floating-point cases (inherited convention, section 10 of the spec) - confirming a sub-lord change at
  a boundary correctly flips the downstream judgment.
- **Retrograde cases**: charts where the 7th cusp's sub-lord planet is retrograde at the test epoch -
  confirming the conditional/disclosed-qualifier output fires correctly (section 19.2).
- **Rahu/Ketu cases**: charts where the sub-lord is a node - blocked on section 3's own conjunction/
  aspect-reuse resolution; cannot be populated until that is resolved (or explicitly excluded from V1).
- **Strength-order cases**: constructed charts where the four-level Ordering A hierarchy is actually
  load-bearing - i.e. different planets occupy the "star of occupant" vs. "occupant" vs. "star of owner"
  vs. "owner" roles for the same house, and the choice between them changes the promise/deny verdict -
  needed to prove Ordering A is genuinely implemented, not vacuously satisfied by cases where all four
  levels happen to agree.
- **Cusp/sub-lord cases**: the dense sweep itself (section 5.3), exercising every KP sub-interval at the
  7th cusp position, mirroring the "51,429-point" scale already established for `KP_CHAIN_V1`/`D45`.
- **Protected holdout**: prime-step deterministic sampling, independent of all of the above, per section
  5.4.

## 7. Certifiability of the horary-to-natal application as an ACE-defined V1 inference

**Yes, this can be certified as such, provided it is labelled precisely as an ACE-defined inference, not
a direct primary-source citation for the natal case.** This project has an established, precedented
mechanism for exactly this situation: a disclosed, school/scope-specific convention that is *not* itself
drawn verbatim from the classical source but is a documented, deliberate engineering choice built on top
of it - matching the KP layer's own `Decision KP-A` (`docs/KP_CHAIN_SPEC.md` §4: the 1e-10 boundary-
tolerance convention is an explicit, disclosed *policy* choice, not itself part of the classical KP
methodology, carried on every result via `nearest_boundary_arcsec`). The same discipline applies directly
here: certify the horary-derived house-group rule as `KP_SIGNIFICATOR_V1`'s **own defined convention for
natal application**, with an explicit provenance field/non-claim on every result stating the rule's own
origin (Krishnamurti's Reader III horary chapter) and that its natal application is an ACE-level inference
- exactly the disclosure pattern this project already uses successfully elsewhere. This does **not**
require re-opening the methodology question `KP_SIGNIFICATOR_SPEC.md` v0.2.0 already settled; it is a
certification-and-disclosure design choice, not a new methodology claim.

## 8. Remaining methodology ambiguity that genuinely blocks certification

**None, for the frozen V1 scope itself.** Every methodology element the CEO's own instruction lists as
already approved (positive/negative houses, strength order, retrograde rule, node substitution priority,
horary-to-natal disclosure) is fully specified and sufficient to write both the production rule and an
independent validator without further research. The one open item - a conjunction orb for the node
substitution rule - is **not** a methodology ambiguity in the sense of "which classical rule applies";
Reader III's own text (already retrieved, not re-searched this task) states the *priority order*
(conjoined > aspecting > sign lord) but was not found to state a numeric orb anywhere in the passages
already found. This is an **engineering-definition gap**, not a live methodological dispute - it needs a
specific value chosen and disclosed (see section 11's decision options), not new primary-source research.

## 9. Certification artifact, independent validator, negative controls, drift protection, CI gates

Mirrors the established `D45`/`KP_CHAIN_V1` pattern directly, with one structural simplification noted:

- **Certification artifact**: `certification/KP_SIGNIFICATOR_V1_certification.json`, same gate-lettering
  convention (table/rule integrity; dense sweep vs. independent validator; independent validator gate;
  boundary cases; protected holdout; negative controls; non-invasiveness/registry-identity check;
  explicit non-claims block, including the polar-Placidus and horary-to-natal disclosures).
- **Independent validator**: a new root-level `validate_kp_significator_holdout.py`, importing nothing
  from the production module, re-deriving the rule from the frozen specification directly (mirroring
  `validate_d45_holdout.py`/`validate_kp_holdout.py`).
- **Negative controls**: planted mutations (swap the positive/negative house sets; corrupt Ordering A's
  own priority sequence; tamper with the sign-lordship copy the validator uses) confirmed genuinely
  detected - mirroring `D45`'s own gate H, including its own lesson that a negative control must be
  checked for degenerate/no-op mutations before being trusted (a real bug found and fixed live during
  `D45`'s own certification execution).
- **Drift protection**: add the new certifier/validator to
  `scripts/certification_support.py`'s `CERTIFIER_SOURCES`/`VALIDATOR_SOURCES` scan scope - with the
  now-documented caveat (this project's own prior CI-drift incident, `docs/ACE_EXECUTION_STATE.md` v7.2.0)
  that doing so shifts `modules_scanned` for **every** other certifier's own artifact, requiring every
  affected artifact to be regenerated in the same change, not just the new one.
- **CI gates**: because there is no oracle (section 4), this certifier needs **no network access and no
  PyJHora dependency** - unlike `D45`'s own oracle-tier placement, `KP_SIGNIFICATOR_V1`'s certifier can
  run in the standard hermetic/no-oracle CI tier, on every push, including the Windows-hermetic legs.
  This is a genuine, positive structural simplification relative to every oracle-backed certifier this
  project has added to date, worth noting as a real advantage, not just a limitation of having no oracle.

## 10. Comparison against existing certified-capability patterns

| Dimension | `D45` (Akshavedamsa) | `KP_CHAIN_V1` | `KP_SIGNIFICATOR_V1` (proposed) |
|---|---|---|---|
| External oracle | PyJHora (corroboration only) | `legacy/kp.py` (in-repo equivalence oracle) | **None found** |
| Independent validator | Yes, from-scratch | Yes, from-scratch | Yes, from-scratch (only evidentiary leg) |
| New astronomical calculation | None (registry dispatch only) | Ported, not new | **None** (orchestrates existing certified substrates) |
| Genuinely new logic | None | Chain-interval math (ported) | Significator-determination + promise/deny (new, low-ambiguity) |
| CI tier | Oracle-tier (network, PyJHora) | Oracle-tier at original certification | Hermetic/no-oracle tier (no dependency) |
| Cross-school reuse question | None | None | Yes - drishti/house-occupancy reuse under KP profile (section 3) |

**KP_SIGNIFICATOR_V1 would be this project's first certified capability with no computational oracle of
any kind (external or in-repository legacy) as corroboration** - not disqualifying (the instruction's own
item 5 anticipates exactly this path), but a genuinely weaker evidentiary posture than every precedent
checked this task, worth the owner's own explicit awareness rather than treating it as routine. It would
also be the first KP-scope capability to need a cross-school reuse decision (Parashari drishti/house
logic consumed under a KP profile) - `KP_CHAIN_V1`'s own school-isolation design never needed this,
since it built its own self-contained astronomical layer.

## 11. Determination and the exact decision required

**B. CERTIFIABLE WITH BLOCKER.**

Certification design is otherwise concrete, fully specified, and ready: every input except the node-
substitution aspect/conjunction logic is already certified and directly reusable (section 2); the two
genuinely new pieces of logic are low-ambiguity and fully specified by the already-frozen methodology
(section 3.1-3.2); no oracle exists but a defensible from-scratch-derivation-plus-holdout strategy is
available and precedented (section 5); the test corpus, certification artifact, validator, negative
controls, drift protection, and CI placement are all concretely designable now (sections 6, 9); the
horary-to-natal application is certifiable as a disclosed ACE-defined inference using an already-
precedented disclosure mechanism (section 7); no residual methodology ambiguity blocks certification
(section 8).

**The exact unresolved prerequisite: a conjunction-orb definition and an aspect-computation reuse-vs-
rebuild architecture decision for the Rahu/Ketu-as-sub-lord substitution rule (section 3.3)**, which is
not a rare edge case and cannot be silently skipped without narrowing V1's own scope. Three resolution
paths, presented as options, not decided here:

1. **Define a specific conjunction orb and extend `PARASHARI_DRISHTI_V1`'s own profile lock** to accept
   `KP_KRISHNAMURTI` snapshots for aspect computation - reuses certified code, but edits a certified
   capability's own profile validation, which needs its own explicit authorization and its own regression
   check that Parashari-Lahiri behavior is unchanged.
2. **Define a specific conjunction orb and build a fresh, KP-scoped aspect calculation**, duplicating the
   same classical angle rules under KP's own school-isolation discipline (never touching
   `engine/parashari/`) - more code, but zero risk to an already-certified capability, consistent with
   the isolation pattern `KP_CHAIN_V1` itself established.
3. **Narrow V1 further**: explicitly exclude the node-sub-lord case from V1's own scope via a disclosed
   non-claim (mirroring `RISE_SET_V1`'s own polar non-claim precedent) - eliminates the blocker entirely
   at the cost of leaving a material share of possible charts out of V1's own coverage; the exact
   fraction excluded is not quantified in this paper and would need to be before this option is chosen
   with confidence.

A conjunction-orb value, once chosen (options 1-2), should itself be verified against Reader III/IV text
already retrieved (or, if genuinely absent there, against a further, narrowly-scoped primary-source check)
before being treated as frozen - this is a small, bounded follow-up, not a reopening of the settled
methodology.

## 12. Explicit non-claims

This paper does not implement `KP_SIGNIFICATOR_V1`. It does not create `engine/kp/significators.py`. It
does not execute certification or create a certification artifact. It does not choose among section 11's
three resolution paths. It does not reopen `KP_SIGNIFICATOR_SPEC.md`'s own frozen methodology (sections
19.1-19.4) or re-investigate Reader II-IV. It does not resolve `DP-025`'s own still-open polar-Placidus
gap. It does not touch FOUNDATION, closed Dasha items, H-03, H10/H11, or `DP-024`. It does not push or
merge.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-26 | Created. Per "CEO AUTHORIZATION — KP_SIGNIFICATOR_V1 CERTIFICATION-READINESS": investigates certification feasibility only, treating `KP_SIGNIFICATOR_SPEC.md` v0.2.0's methodology as already approved and not re-researched. Confirms most production inputs already certified and directly reusable (`KP_CHAIN_V1` cusp/planet chains, sign-lordship table, retrograde derivation convention, Placidus cusps); confirms the two genuinely new logic components (significator determination, promise/deny judgment) are low-ambiguity and fully specified; confirms no computational oracle exists (reaffirming `DP-028`, not re-researching); designs an independent-derivation-plus-holdout certification strategy, test corpus, artifact/validator/negative-control/CI plan, and certifies the horary-to-natal application as a disclosed ACE-defined inference via an already-precedented mechanism (`KP_CHAIN_SPEC.md` Decision KP-A). Identifies one genuine blocker - a conjunction-orb definition and aspect-computation reuse-vs-rebuild decision for the Rahu/Ketu-as-sub-lord case, not a rare edge case - and presents three resolution options without deciding among them. Determination: B, CERTIFIABLE WITH BLOCKER. Does not implement, does not execute certification, does not push or merge. |
