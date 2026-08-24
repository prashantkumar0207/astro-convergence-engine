<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and recommends one. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-24 |
| Review cadence | TBD |

# DP-021. JATAKA architecture / first-capability decision-readiness

## 0. Authorization and scope

Authorized by the owner's explicit "CEO AUTHORIZATION — BEGIN JATAKA ARCHITECTURE / CAPABILITY
DECISION-READINESS INVESTIGATION" instruction (2026-08-24), following `ADR-0074`'s own JATAKA-entry
ratification and the merge of `phase-g-governance` into `main` (`d738520`, later `931b6d0`/`c4d571a`
via PR #4). This is a decision-readiness investigation only. **It does not implement anything, does not
choose a capability, and does not ratify itself.** Independent prior analysis from a separate Claude Web
audit was supplied as an input, explicitly NOT as a predecided architectural choice, and is tested
against repository evidence throughout, not accepted at face value (see section C).

State audit performed before this investigation began: branch `phase-g-governance`, local HEAD =
`origin/phase-g-governance` = `c4d571a340b4baf873fbefb5661eb195937d2f51`, working tree clean,
`origin/main` = `d738520ffc796d07468e24a5b1dddcfba3120c65` (the JATAKA-entry merge, PR #4). Next free
ADR confirmed as `ADR-0075` (not used here - no ADR is drafted by this paper). `DP-021` registered in
`docs/decisions/README.md` before drafting, per `ADR-0040`.

**Method note on evidence quality:** all capability-inventory claims below were independently verified
against live source code, test files, and certification JSON `"result"` fields - not inferred from
prose documentation alone, per the owner's own explicit instruction. Three parallel research passes
were run: (1) a full capability-by-capability code/test/certification inventory, (2) a deep,
dedicated investigation of house-cusp/bhava methodology specifically, (3) a survey of every governing
specification document relevant to JATAKA. Where a secondary source (`certification/
ENGINE_CAPABILITY_INVENTORY.json`) was used for cross-checking, note that this specific file is itself
dated 2026-08-11 and is now **stale relative to this session's own subsequent work** - it still cites
finding H-04 ("pratyantardasha never oracle-compared") as open, when H-04 was in fact closed on
2026-08-17 (`ADR-0053`) and re-confirmed via oracle comparison repeatedly through this session's own
M-02/boundary-proximity work (CI-verified `pratyantar rows: 20412, lord mismatches: 0`). Every claim in
this paper that could be affected by that staleness was independently re-verified against live source,
not taken from the inventory JSON alone.

## A. Current JATAKA capability inventory

Status vocabulary used below, exactly as instructed: **certified and production-usable** / **implemented
but uncertified** / **architecture/specification only** / **stub/refusal** / **explicitly deferred by a
recorded decision** / **not yet implemented**.

| # | Capability | Status | Evidence |
|---|---|---|---|
| 1 | Planetary/astronomical foundations | **Certified** | `certification/current_engine_certification.json`, `CURRENT_ENGINE_LOCK.json` (`LOCKED_TIER0_CERTIFIED`, `ADR-0034`); max planet error 0.000179 arcsec vs swetest, 528 comparisons |
| 2 | Ascendant / lagna | **Certified** | Part of the same Tier-0 kernel certification; `engine/astronomy/house_positions.py`, `engine/astrology/chart_lagna_builder.py` |
| 3 | Houses / bhava - whole-sign (D1 planet-to-house assignment) | **Certified** | `engine/astrology/house.py`, `chart_planet_builder.py`; `ENGINE_CAPABILITY_INVENTORY.json`: `D1_rashi: CERTIFIED` |
| 3b | Houses / bhava - Placidus cusp geometry | **Partially certified** | `certification/ENGINE_CAPABILITY_INVENTORY.json`: `"houses_placidus": {"status": "PARTIALLY_CERTIFIED", "note": "exercised to 64.1N only; polar behaviour NOT VERIFIED and undefined"}`; independently confirmed against `current_engine_certification.json`'s own 11-case holdout (max latitude 64.1466°N) |
| 3c | Houses / bhava - equal-house rule | **Implemented but uncertified** | `engine/astrology/house.py::equal_house_from_ascendant()`, tested in `test_boundary_hardening.py`, no certification artifact |
| 4 | Vargas D1/D2/D3/D7/D9/D10/D12/D30 | **Certified** | `engine/astrology/__init__.py::CERTIFIED_PRODUCTION_VARGAS` (D2/D3/D7/D12/D30) + hard-wired D9/D10; five `VARGA_*_V1_certification.json` files + Tier-0 lock for D9/D10 |
| 5 | Remaining vargas (D4, D16, D20, D24, D27, D40, D45, D60, ...) | **Not yet implemented** | `varga_registry.py::get_varga_rule()` raises `UnsupportedVargaError` for anything unregistered; confirmed no other varga module exists in `engine/astrology/` |
| 6 | Parashari graha drishti (full/purna aspects) | **Certified (partial scope)** | `certification/PARASHARI_DRISHTI_V1_certification.json`; explicit non-claims: fractional sputa drishti deferred, Rahu/Ketu cast no aspects (Decisions AS-A/AS-B) |
| 7 | Parashari rules/yoga evaluation (Raja yoga, Dhana yoga, etc.) | **Not yet implemented** | Zero code found anywhere; `ENGINE_CAPABILITY_INVENTORY.json`: `strength_and_yogas.yogas: ABSENT` |
| 8 | KP chart structures (SL/NL/SB/SS lordship chain on planets, cusps, ascendant) | **Certified** | `certification/KP_CHAIN_V1_certification.json`; `engine/kp/chain.py`, `engine/models/kp_chart.py` |
| 9 | KP significators (four-step, ruling planets, cuspal sub-lord technique) | **Explicitly deferred by a recorded decision** | `engine/kp/README.md`: "Explicit non-claims: significators, four-step, ruling planets, horary, dashas" - gated on `D-008` (`docs/DECISION_LOG.md` D-008 entry), which requires a frozen, independently-audited methodology spec, naming "cusp handling" as one of eleven mandatory elements, before any implementation |
| 10 | Horary (KP horary-number methodology) | **Explicitly deferred by a recorded decision** | Same non-claim as #9; `ENGINE_CAPABILITY_INVENTORY.json`: `domains.prashna_horary: PLANNED` (product-domain concept, distinct but consistent) |
| 11 | Vimshottari dasha (depths 1-3, both schools) | **Certified** | `certification/VIMSHOTTARI_V1_certification.json`; this session's own six-step Dasha roadmap closure (`ADR-0053`, `ADR-0069`-`ADR-0073`) |
| 12 | Vimshottari depths beyond 3 | **Not yet implemented (explicit guard)** | `vimshottari_from_moon()` raises `ValueError` for `depth not in (1,2,3)`; recursive `_subdivide()` machinery already exists and generalizes, but is capped by an explicit boundary check, not a missing algorithm |
| 13 | Other dasha systems (Ashtottari, Yogini, ...) | **Explicitly deferred by a recorded decision** | `docs/VIMSHOTTARI_DASHA_SPEC.md`: "no other dasha systems... each with its own ADR"; `DASHA_CERTIFICATION_ROADMAP.md` §6: "Not planned, not specified, not authorised" |
| 14 | Jaimini (karakas, aspects, dashas, Arudha padas, rashi drishti) | **Explicitly deferred by a recorded decision** | Zero code anywhere; `docs/PARASHARI_DRISHTI_SPEC.md`: "Jaimini rashi drishti... explicitly OUT of this phase... their own modules under their own ADRs" |
| 15 | BNN (Bhrigu Nandi Nadi) | **Explicitly deferred by a recorded decision** | Zero code; `CURRENT_ENGINE_LOCK.json` non-claims list "Jaimini, BNN/Nadi, numerology" together |
| 16 | Numerology | **Explicitly deferred by a recorded decision** | Same non-claim as #15 |
| 17 | Karakas - three unrelated meanings, reported separately | See below | See below |
| 17a | ... KP significator/karaka logic | Same as #9 - explicitly deferred | |
| 17b | ... Jaimini Chara karakas | Same as #14 - explicitly deferred | |
| 17c | ... static "natural significator" metadata field | **Implemented but uncertified** | `engine/models/planet_metadata.py::karakas: Tuple[str,...]`, populated from `engine/knowledge/data/planets.json`; descriptive reference data, not wired into any chart-analysis consumer; no shared code with #17a/#17b |
| 18 | Planet strength (Shadbala) | **Stub/refusal (deliberate)** | `engine/astrology/planet_strength.py::planet_strength()` raises `NotImplementedError` by explicit design - "a placeholder 0.0 was previously returned here; that was removed so unimplemented strength can never masquerade as a computed value" |
| 19 | Interpretation layer | **Architecture/specification only** | `docs/H5_INTERPRETATION_RULE_REGISTRY_SPEC.md`, `Status: PROPOSED, C0 RESEARCH`; zero implementing code |
| 20 | Provenance | **Implemented but uncertified (standalone); load-bearing everywhere** | `engine/models/provenance.py`, consumed by 58 files; no dedicated certification artifact of its own, exercised transitively by every certified capability |
| 21 | Convergence | **Architecture/specification only** | `docs/H8_CONVERGENCE_SPEC.md`; zero implementing code; `Q8_CLOSURE_MATRIX.md` §8 requires INTERPRETATION exit first, which requires EVIDENCE exit first, which requires JATAKA **exit** (not just entry) |
| 22 | Historical ledger / backtesting | **Architecture/specification only** | `docs/H2_HISTORICAL_EVENT_LEDGER_SPEC.md`; project's existing "holdout" scripts are certification fixtures, not a historical-event ledger - two unrelated concepts sharing a word |
| 23 | BTR | **Architecture/specification only** | `docs/H7_BTR_SPEC.md`; explicitly "orthogonal to the phases," becomes possible only once EVIDENCE exits (`Q8_CLOSURE_MATRIX.md` §13) |

**Complete certified-artifact list** (all `"result": "PASS"`): `current_engine_certification.json`,
`RISE_SET_V1`, `KP_CHAIN_V1`, `PANCHANGA_V1`, `PARASHARI_DRISHTI_V1`, `TRANSIT_V1`, `TRIKALAM_V1`,
`VARGA_D2/D3/D7/D12/D30_V1`, `VIMSHOTTARI_V1`, `SIGN_CONVENTION_V1`. `CURRENT_ENGINE_LOCK.json` is a lock
record, not a fresh test-run artifact.

## B. Dependency graph

**Direct dependencies** (a capability cannot function without this):
- Everything → Tier-0 kernel (sidereal longitudes, ayanamsa, provenance).
- Vargas, drishti, D1 houses, dasha seeding → sidereal planetary longitudes (already certified).
- KP chart, Vimshottari-under-KP-seeding → the KP_KRISHNAMURTI profile's own Placidus cusps (already
  certified, non-polar) and mean-node policy.
- KP significators (if ever built) → KP chart's own cuspal SL/NL/SB/SS chain (already certified) **and**
  a frozen `D-008` methodology spec (not yet written) **and**, per `D-008`'s own text, resolved "cusp
  handling" - which, per section D below, means resolved polar-Placidus behaviour specifically, since a
  significator methodology cannot leave its own cuspal input domain undefined.
- Parashari yoga detection (if ever built) → planetary sign/house/nakshatra placement (D1, already
  certified), conjunctions (derivable from longitude, already certified), graha drishti (already
  certified, full aspects only) - **and a frozen, source-cited yoga rule specification**, which does not
  yet exist in any form.
- Jaimini Chara karakas (if ever built) → **only** exact planetary longitudes (already certified) - the
  narrowest technical dependency footprint of any candidate investigated, **but** gated by the project's
  own school-isolation policy exactly as KP/BNN/Numerology are (its own ADR, its own module, no shared
  code with Parashari or KP).
- Shadbala (if ever built) → sign/house placement, aspects, possibly rise/set-derived day/night status,
  possibly divisional-chart placement depending on which of the six classical sub-components are
  included - the widest and least-well-defined dependency footprint of any candidate investigated.

**Shared dependencies, explicitly evaluated per the owner's own caution ("do not assume that a shared
mathematical dependency automatically means the methodology itself is shared"):** Parashari and KP both
consume the same certified Tier-0 kernel and the same certified sidereal longitudes - but their own
house/cusp usage is **not** shared: Parashari's certified house rule is whole-sign (a sign-membership
classification, no cusp geometry at all); KP's is cuspal Placidus with a lordship chain. These are two
architecturally separate, already-certified, non-interchangeable rules (`engine/astrology/house.py`'s own
docstring: "NOT interchangeable, audit findings F-05/A-2"), not one shared house implementation feeding
two schools. The only genuinely shared *infrastructure* (as opposed to methodology) is the underlying
`swe.houses_ex()` cusp-geometry call itself, which KP consumes directly and Parashari does not consume at
all for its own certified house rule.

**System-specific dependencies:** Jaimini/BNN/Numerology each require their own from-scratch module and
ADR under this project's own school-isolation discipline (already applied consistently to Parashari vs.
KP vs. Vimshottari's own duplicated lord/year tables) - none can share code with Parashari or KP even
where a concept (e.g. "karaka") has a superficially similar name.

**Certification dependencies:** every candidate ultimately needs, per the established template
(`docs/NEW_VARGA_IMPLEMENTATION_TEMPLATE.md`, and the KP chain build record in `docs/KP_CHAIN_SPEC.md`):
an ADR before code, a frozen rule/table, an oracle comparison, an independent from-scratch validator, a
protected holdout, a machine-readable + human-readable artifact pair, and additive documentation. See
section F.

**Methodology dependencies:** for yogas, significators, karakas (Jaimini), Shadbala, BNN, and Numerology,
the blocking dependency is **not calculation infrastructure** - it is a **frozen, source-cited,
owner-ratified methodology specification**, which does not exist for any of them yet. This is the single
most important structural finding of this investigation (see section C.6).

**Variant dependencies:** see section G.

**Highest-leverage shared foundation, stated precisely:** the Tier-0 kernel (already certified) is the
one universal dependency. Beyond that, there is no single shared foundation that unlocks multiple
higher-value capabilities at once the way Claude Web's "bhava has the highest shared-dependency value"
framing implied - Parashari's own path to yogas and KP's own path to significators diverge immediately
after Tier-0, and each is blocked primarily by its own missing methodology specification, not by shared
missing infrastructure.

## C. Testing Claude Web's independent analysis against the evidence

Presented explicitly as prior analysis to be tested, not accepted, per the owner's own instruction.

1. **"Bhava/house-cusp methodology appears to have the highest shared-dependency value."** Partially
   right, importantly mis-scoped. House/cusp work is **not** a greenfield build - whole-sign D1 houses are
   already fully certified, Placidus cusp geometry is already partially certified (non-polar), and KP's
   own cuspal lordship chains are already fully certified as part of `KP_CHAIN_V1`. The genuine remaining
   gap is narrow: polar-latitude Placidus certification (§D) and one apparently-still-open provenance
   finding (M-04, §D). Framing this as "build bhava first" overstates the remaining work; framing it as
   "close bhava's own remaining certification gap" is accurate and far cheaper.
2. **"It potentially underlies Parashari yogas and KP significators."** True for KP significators -
   `D-008`'s own text names "cusp handling" as a mandatory spec element, and the polar-cusp gap is exactly
   the kind of undefined domain a significator methodology cannot leave open. **Not really true for
   Parashari yogas** - classical yoga detection is driven by sign/house/nakshatra placement and
   conjunctions/aspects, all of which are already certified; cusp geometry is not a load-bearing input to
   Parashari yoga rules as this project has scoped houses (whole-sign, not cuspal) for that system.
3. **"Karakas are a smaller independent capability with low dependency cost."** True in the narrowest
   technical sense for Jaimini Chara karakas specifically (longitude-ranking only, no house/cusp
   dependency at all) - but this project's own school-isolation discipline still requires Jaimini's own
   ADR and module before any Jaimini karaka can be built, so "low dependency cost" applies to the
   mathematics, not to the governance/specification prerequisite. KP's own "karaka" concept is really KP
   significators (#9 above), not a separate, cheaper item.
4. **"Parashari yogas and KP significators should probably follow chart-structure work."** Partially
   right for KP significators (the polar-cusp gap is a genuine, if narrow, prerequisite); **not really
   right for Parashari yogas**, whose own chart-structure prerequisites are already certified - its actual
   blocker is a yoga-rule specification, a different kind of work than "chart structure."
5. **"KP significators require careful resolution of the relevant house-cusp methodology, including the
   previously identified polar-Placidus question."** **Confirmed, and well-evidenced** - this is the most
   validated of the six claims. `D-008` names cusp handling explicitly; the polar-Placidus gap is real,
   extensively self-documented across at least seven repository files (§D.4), and genuinely unresolved.
6. **"Interpretation, convergence, historical prediction validation, BTR, Jaimini, BNN, Numerology and
   other higher-level capabilities should not be prematurely implemented."** **Confirmed directly** by
   `Q8_CLOSURE_MATRIX.md`'s own phase-gating (EVIDENCE/INTERPRETATION/CONVERGENCE all require JATAKA
   **exit**, not merely entry) and by every one of those capabilities' own governing document being
   `Status: PROPOSED, C0 RESEARCH` with an explicit "no implementation authorised" line.

**The corrected headline finding this investigation adds, not present in the independent input:** the
real bottleneck for JATAKA's higher-value capabilities (yogas, significators, karakas beyond Jaimini's
narrow case) is **missing ratified methodology specifications, not missing calculation infrastructure.**
The calculation substrate (houses, aspects, dasha, vargas, provenance) is already substantially built and
certified. This reframes the entire "what should be first" question: it is at least as much a
methodology-specification exercise as an engineering one.

## D. Bhava/house-system investigation (in depth, per the owner's own explicit mandate)

1. **What house methodology ACE currently specifies:** two separate, explicitly non-interchangeable
   rules, both already implemented: whole-sign planet-to-house assignment (`engine/astrology/
   house.py::whole_sign_house()`, the certified D1 rule) and Placidus cusp geometry
   (`engine/astronomy/house_positions.py`, via `swe.houses_ex(..., b"P", ...)`). An `equal_house_from_
   ascendant()` rule also exists, tested but uncertified and unused by any certified consumer.
2. **Whether any house system is already certified:** yes, both are, at different scopes - whole-sign D1
   assignment is fully certified; Placidus cusp geometry is *partially* certified, exercised only to
   64.1°N/S, with polar behaviour explicitly and repeatedly flagged as unverified and undefined across
   `README.md`, `docs/ENGINE_STATUS.md`, `docs/PROJECT_ROADMAP.md`, `ARCHITECTURE_STATUS.md`,
   `CURRENT_ENGINE_CERTIFICATION_STATUS.md`, `certification/ENGINE_CAPABILITY_INVENTORY.json`, and
   `docs/DECISION_LOG.md`'s own Tier-0 lock scope note.
3. **What Parashari requires:** whole-sign only, already certified, already the settled project decision
   (audit finding A-2, resolved by specification) - not an open methodology question. No Parashari
   document in this repository discusses or considers a cuspal (Placidus/Sripati) convention as an
   alternative for house-based work.
4. **What KP requires:** Placidus cusps specifically, with a full lordship chain attached to each cusp -
   already built and certified as part of `KP_CHAIN_V1` (`docs/KP_CHAIN_SPEC.md`: "attaches the chain to
   every planet, cusp, and the ascendant"; Gate 3 requires exact SL/NL/SB/SS match for every cusp, zero
   tolerance). The raw ingredient of a "cuspal sub lord" (the cusp's own SB field) already exists and is
   certified today; no significator logic is built on top of it yet.
5. **Whether Parashari and KP can legitimately share one implementation:** no, by explicit project
   decision, already implemented as two separate rules with a docstring stating they are "NOT
   interchangeable" and "never silently mixed." This is correct and should not be revisited.
6. **Whether they require separate system-specific implementations:** yes, already true today - whole-sign
   for Parashari's own certified D1, cuspal Placidus for KP's own certified chart. No change needed.
7. **Whether Placidus is required for any intended KP capability:** yes - KP astrology's own tradition
   requires Placidus cusps for cuspal sub-lord technique, and this project's own `KP_KRISHNAMURTI` profile
   already hardcodes `house_system=b"P"` for exactly this reason.
8. **What the previously identified polar-Placidus issue actually is:** Placidus house division becomes
   mathematically undefined at extreme latitude (the semicircle-of-diurnal-arc construction that defines
   Placidus cusps fails once a degree of the ecliptic no longer rises and sets locally - the general
   astronomical fact is not itself derived or cited anywhere in this repository, only its practical
   consequence is). This project's own documentation states the practical boundary as "above the polar
   circles" / "above 64.1°N," which is the *edge of the frozen holdout matrix's own highest-latitude case*
   (`H5_reykjavik_1992`, 64.15°N) rather than a derived theoretical threshold - i.e., "64.1°N" is where
   testing stopped, not necessarily where degeneracy begins. `scripts/profile.py`/`regression_report.json`
   assert, without in-repo verification, that Swiss Ephemeris's own internal behaviour falls back to
   Porphyry above the polar circle - this specific claim has never been tested against swetest in this
   repository.
9. **What latitude/domain boundaries matter:** the true astronomical polar circle (~66.5633°N/S) is the
   commonly-cited threshold beyond which Placidus becomes undefined for at least part of the ecliptic;
   this project's own current certification stops well short of that (64.1°N), leaving both the
   64.1°-to-66.5° band and the true polar zone unverified.
10. **What authoritative references are required:** a citable, precise mathematical definition of Placidus
    house division's own polar failure mode (a genuine gap - this repository does not currently cite one),
    plus a decision on what a certified system should *return* in the undefined zone (raise, refuse
    structurally, or fall back to a named alternative system) - none of these are decided yet.
11. **What oracle/reference implementation is available:** the bundled `swetest` 2.10.03 binary (already
    the Tier-0 oracle for non-polar Placidus, independently verified to ~0.0002 arcsec) is the natural
    first oracle to test against at high latitude, since it is already the authority for the non-polar
    case and its own polar behaviour (Porphyry fallback or otherwise) can be observed directly.
12. **Whether PyJHora is sufficient:** PyJHora has **never** been used as a house-cusp/bhava oracle
    anywhere in this repository (confirmed by direct search of every `scripts/certify_*.py` import) - it
    has only ever supplied panchanga, dasha, varga-chart, and aspect oracle data. Its own house-cusp
    capability, if any, is untested by this project and would need independent verification before use.
13. **What independent validator can be built:** following the established pattern (a from-scratch
    validator importing nothing from the production module), an independent Placidus-cusp re-derivation
    at high latitude, cross-checked against `swetest`'s own polar output and, ideally, a second
    independent library or a closed-form boundary analysis of where the diurnal-arc construction itself
    fails.
14. **What boundary tests are required:** cases bracketing 64.1°N/S (the current holdout edge), the true
    polar circle (~66.5633°N/S), and at least one case strictly inside the Arctic/Antarctic circle where
    Placidus is expected to be genuinely undefined for at least part of the ecliptic.
15. **What certification artifact should exist:** either an extension of the existing Tier-0 kernel
    certification's own holdout matrix (adding polar cases) or - given the established project convention
    of one artifact per capability - a small, dedicated `HOUSES_POLAR_V1`-style artifact recording exactly
    what was tested, what the defined behaviour is, and what remains genuinely unverifiable. **A directly
    applicable, already-certified precedent exists for exactly this shape of problem:** `RISE_SET_V1`'s
    own structured `NO_RISE`/`NO_SET` status pattern (never an exception, never a silently-wrong value,
    `certification/RISE_SET_V1_certification.json`: `"circumpolar_cases_checked": 2`) - no equivalent
    structured status exists yet for undefined house cusps; `house_positions()` today has no polar guard
    at all and will silently pass through whatever Swiss Ephemeris itself does.

**Section D conclusion:** the polar-Placidus gap is real, narrow, well-precedented (RISE_SET_V1's own
pattern applies directly), and closing it would be Tier-0/FOUNDATION-tier maintenance work, not a new
JATAKA capability in its own right - but it is a genuine, specific prerequisite for KP significators
specifically (via `D-008`'s own "cusp handling" requirement), not for Parashari yogas.

## E. System-boundary analysis

Every finding above was checked for accidental system-merging; none was found. Whole-sign (Parashari) and
cuspal Placidus (KP) houses remain two separate, non-interchangeable, already-certified rules with no
shared code. The word "karaka" names three unrelated things in this codebase (KP significator concept,
Jaimini Chara karaka, static natural-significator metadata) with zero shared code between any pair,
confirmed by direct search. "Yoga" names two unrelated things (the panchanga anga, already certified, vs.
Raja/Dhana-style combination yogas, not implemented) - do not conflate them. No evidence of any
Parashari/KP/Jaimini/BNN/Numerology cross-contamination was found anywhere in the current codebase; the
project's own school-isolation discipline (duplicated lord/year tables between `engine/dasha/` and
`engine/kp/`, cross-consistency tests rather than cross-imports) is consistently applied. **Recommendation
for any future capability: preserve this discipline exactly - a new capability must carry its own system
tag/provenance field (mirroring `Provenance.house_system`/`node_policy`/etc.) so results remain
attributable to their originating school, never silently merged.**

## F. Certification requirements (for whichever capability is eventually chosen)

Per the established, five-times-proven template (`docs/NEW_VARGA_IMPLEMENTATION_TEMPLATE.md`, the KP
chain build record, and this session's own six-ADR Dasha-roadmap pattern), any first JATAKA capability's
certification design should include, as applicable: an ADR drafted **before** any code (naming classical
source, school key, every non-claimed variant); a frozen rule/table module; an independent, from-scratch
oracle comparison (swetest and/or PyJHora, whichever is actually verified applicable - not assumed, per
§D.12); an independent validator importing nothing from the production module; positive, negative, and
boundary cases; a protected holdout never used for tuning; a machine-readable `certification/*.json`
artifact plus a human-readable `.report.md`; regression tests collected into the default gate; a genuine
negative control (this session's own established practice: actually break the guard, confirm the test
fails, restore, confirm byte-identical); artifact-drift protection (`check_artifact_drift.py`); CI
execution under the hash-pinned oracle environment; and explicit, itemized non-claims. **A gate that
cannot fail must not be proposed** - every comparison must be checked, before being trusted, to actually
be capable of catching a real, deliberately-injected defect (the H-03/B-03/M-03 "gate that cannot fail"
failure mode this project has already found and remediated elsewhere must not be repeated for a new
capability).

## G. Variant analysis

No implicit variant should be introduced for any future capability. Explicitly enumerated, current
production-variant status:

| Variant axis | Current certified state |
|---|---|
| House system | Two: whole-sign (Parashari D1, certified), Placidus (KP, certified non-polar) |
| Ayanamsa | Lahiri (`parashari_lahiri`), Krishnamurti (`kp_krishnamurti`) - both certified, both explicit `CalculationProfile` fields |
| Node policy | Mean node only; `find_crossings()` explicitly refuses true node for Rahu/Ketu (`UnsupportedNodePolicyError`, `ADR-0066`) |
| Boundary convention | Engine-wide 1e-10 tolerance-promoted (`longitude_utils.py`) vs. KP's own exact `[start,end)` rule - both certified, deliberately different, cross-referenced (`ADR-0071`) |
| School/tradition | Parashari, KP - both isolated by construction; Jaimini/BNN/Numerology not yet built |
| Orb | Not applicable to any currently certified capability (aspects are exact-angle Parashari drishti, not orb-based) |
| Calculation mode | Sidereal only, strict ephemeris mode |
| Chart type | D1 plus D2/D3/D7/D9/D10/D12/D30 vargas, all certified with individual scope |

Any new capability (a new varga, a house-system extension, a yoga rule, a significator methodology) must
declare its own variant scope explicitly in its own ADR and carry its own provenance field, per the
project's own established convention - this paper does not itself add or authorize any new variant.

## H. Risks and unresolved questions

1. **The governing-scope question (the single most consequential open item - see section M):**
   `Q8_CLOSURE_MATRIX.md` §5's own "Implementation scope" row names exactly four items - remaining
   vargas, Vimshottari depth/convention extensions, additional aspect coverage, planet strength - and
   states "each is a separate ADR." **None of Claude Web's proposed candidates (bhava, karakas, Parashari
   yogas, KP significators) appears in that list.** `specs/PROJECT_CHARTER.md`'s own "Analytical systems"
   text does separately name KP (with its "Four-Step refinement") as an in-scope system for the product
   overall, but the charter does not itself authorize *when* within JATAKA that work may begin. Whether
   Q8 §5's implementation-scope row is an illustrative starter list or an exhaustive boundary requiring
   its own amendment before anything outside it may be proposed is **not resolved by any document found
   in this investigation** - this paper does not resolve it either; it is presented as the first item in
   section M.
2. Risk of manufactured confidence, evaluated per candidate: highest for Shadbala (six classically-varying
   sub-components, real risk of picking one textual tradition's formula and presenting it as *the*
   answer) and for Parashari yogas (dozens to hundreds of named yogas across classical sources, with
   materially different qualifying conditions between texts) - lowest for a remaining varga (formulas are
   classically fixed and largely uncontested per division) and for Vimshottari depth extension (the
   proportional-subdivision rule is already certified and simply recurses).
3. Risk of methodology ambiguity: KP significators carries real ambiguity even with `D-008`'s own
   eleven-element checklist, since "four-step" interpretation itself has documented variant traditions;
   this is exactly why `D-008` requires a frozen, independently-audited spec before any code.
4. The M-04 finding (`DrishtiChart` provenance records `house_system == 'P'` while `aspected_houses` are
   computed whole-sign) was found by the deep bhava investigation to be still present in the codebase's
   own provenance-labelling pattern; whether it has been separately closed by a decision not surfaced in
   this investigation's own searches is not confirmed either way - flagged as a concrete, narrow,
   independently-verifiable item worth checking before or alongside any house-cusp-adjacent work.
5. The "risk order" for remaining vargas, referenced by `Q8_CLOSURE_MATRIX.md` §5's own text ("remaining
   production vargas in the roadmap's risk order"), was not found defined in any document searched - if
   vargas are chosen as the first capability, which one goes first is itself an open sub-question.
6. Whether closing the polar-Placidus gap belongs to JATAKA's own scope at all, versus being leftover
   FOUNDATION/Tier-0 certification debt (it lives inside `current_engine_certification.json`, the
   already-locked Tier-0 kernel artifact, not a JATAKA-scope certification) is itself worth the owner's
   explicit framing, since fixing it does not obviously require a JATAKA-phase ADR the way a new JATAKA
   capability would.

## I. Proposed sequencing

Two tracks are presented, since section H.1's governing-scope question determines which is even
available without a prior owner decision.

**Track 1 (textually authorized today, no scope question to resolve):**
Remaining varga (risk order TBD) **or** additional Parashari aspect coverage (sputa drishti / node
aspects, per Decisions AS-A/AS-B already on record as deferred-not-decided) **or** Vimshottari depth
extension **or** Shadbala - each independently authorizable via its own ADR, per `Q8_CLOSURE_MATRIX.md`
§5's own text, with no dependency between them.

**Track 2 (Claude Web's own proposed sequence, tested and reordered by evidence, contingent on section
H.1 being resolved in favour of a broader JATAKA scope):**
Close the polar-Placidus certification gap (Tier-0/FOUNDATION maintenance, cheap, precedented via
`RISE_SET_V1`'s own pattern) → resolve the M-04 provenance finding if still open → **only then** begin
`D-008`'s own KP-significator methodology-specification decision-readiness work (a dedicated, separate
paper, not implementation) → separately and independently, Parashari yoga-rule specification
decision-readiness work (its own dedicated paper - not gated by the polar-Placidus item at all, since
Parashari yogas do not depend on cusp geometry) → Jaimini Chara karakas, if the owner wants the cheapest
possible new *system*, gated only by its own required ADR and module, not by any of the above.

Both tracks explicitly do **not** touch EVIDENCE, INTERPRETATION, CONVERGENCE, historical
backtesting/BTR, Jaimini/BNN/Numerology beyond the narrow karaka item named above, Mundane, Prashna,
Varshaphal, or Muhurta - all remain separately governed and are not implied by JATAKA entry
(`Q8_CLOSURE_MATRIX.md` §6-§13).

## J. Options

- **Option 1:** Select a Track 1 capability now (varga / aspect coverage / dasha depth / Shadbala),
  staying strictly within `Q8_CLOSURE_MATRIX.md` §5's own literal implementation-scope text, no
  scope-interpretation decision required.
- **Option 2:** First resolve section H.1 (confirm Q8 §5's list is illustrative, or formally extend it),
  then select from the full candidate set including bhava-gap-closure, KP significators, Parashari yogas,
  or Jaimini karakas.
- **Option 3:** Authorize Track 2's own first step only (closing the polar-Placidus certification gap),
  treating it as FOUNDATION/Tier-0 maintenance rather than a JATAKA-scope choice, deferring the section
  H.1 question until a genuine JATAKA-labelled capability is actually proposed.
- **Option 4:** Defer capability selection entirely; request a narrower decision-readiness paper for one
  specific Track 1 item (e.g. "which varga, in what risk order") before committing to a first capability.

## K. Recommendation (NOT a decision)

**At medium confidence:** resolve section H.1 first (Option 2's own first half), since it is logically
prior to every other choice and costs nothing to answer. Independent of that answer, **Option 3 (closing
the polar-Placidus gap) is recommended as worth doing regardless of which capability is chosen next** -
it is cheap, narrowly scoped, already has a directly-applicable certified precedent (`RISE_SET_V1`), and
is a genuine prerequisite for KP significators specifically without being a large commitment in its own
right. For the actual "first JATAKA capability" question, **a Track 1 item - most likely a remaining
varga, once its own risk order is decided - is the lower-risk choice** or, if the owner's strategic
priority is what Claude Web's own analysis was gesturing toward (unlocking KP significators), the
correct next step is **not** "build bhava" but **`D-008`'s own methodology-specification decision-
readiness work**, which is a substantial undertaking in its own right and deserves its own dedicated
paper rather than being folded into this one. Confidence is medium rather than high because section H.1
is genuinely unresolved and materially changes which options are even available.

## L. Explicit non-claims

This paper does not choose a first capability. It does not authorize implementation of anything. It does
not resolve the D-008 KP-significator methodology question. It does not draft or authorize a Parashari
yoga specification. It does not authorize Jaimini, BNN, or Numerology work. It does not touch H-03, the
eight `H10`/`H11` cross-certifier findings from `ADR-0072`, or any closed Dasha/FOUNDATION item. It does
not modify any production code, test, or certified artifact. It does not determine whether the M-04
finding is still open - that is flagged as requiring independent verification, not resolved here. It does
not determine varga risk order. It does not derive the precise mathematical latitude threshold at which
Placidus becomes undefined - that remains an open technical item for whoever eventually does the
polar-Placidus work.

## M. Exact owner decisions required

1. **Governing-scope question (section H.1):** does `Q8_CLOSURE_MATRIX.md` §5's "Implementation scope"
   row (remaining vargas, Vimshottari extensions, aspect coverage, planet strength) name the exhaustive
   set of things JATAKA may build without a Q8-matrix amendment, or is it illustrative, with other
   JATAKA-appropriate capabilities (bhava-gap-closure, KP significators, Parashari yogas, Jaimini
   karakas) eligible for their own ADR without first amending Q8 §5 itself?
2. Which of Options 1-4 (section J) to pursue.
3. If Option 1 or a varga-first path is chosen: authorize a follow-up, narrower decision-readiness paper
   establishing varga risk order.
4. If the polar-Placidus gap is to be closed (Option 3, recommended regardless of the above): confirm
   whether this is authorized now as FOUNDATION/Tier-0 maintenance (no JATAKA ADR needed) or should itself
   go through a JATAKA-scoped decision.
5. Whether to authorize a dedicated, separate decision-readiness paper for `D-008`'s own KP-significator
   methodology specification, and/or a Parashari yoga-rule specification, as next steps after whichever
   near-term item is chosen above.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-24 | Created. First authorized JATAKA-phase decision-readiness paper. Full capability inventory (23 areas) independently verified against live code/tests/certification artifacts via three parallel research passes; dependency graph built with explicit rejection of the "shared math implies shared methodology" assumption; Claude Web's six independent claims tested individually against evidence (one confirmed strongly, several found overstated or mis-scoped); deep bhava/house-cusp investigation (15 sub-items) confirms both certified house rules already exist, with a narrow, well-precedented polar-Placidus certification gap as the genuine remaining item; identifies the governing-scope question (whether `Q8_CLOSURE_MATRIX.md` §5's implementation-scope row is exhaustive) as the single most consequential unresolved item; presents two sequencing tracks and four options; recommends resolving the scope question first and treating the polar-Placidus gap as worth closing regardless, at medium confidence. Options only; decides nothing; not implementation-authorized; no ADR drafted. |
