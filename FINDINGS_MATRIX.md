# FINDINGS MATRIX - REMEDIATION STATUS

> **SUPERSEDING NOTE (2026-08-09).** Two dispositions in this matrix have since changed and
> are recorded in `docs/DECISION_LOG.md` ADR-0003 and ADR-0012. **F-13**: aspect SYSTEMS,
> recorded here as intentionally not claimed, were built and certified as Parashari graha
> drishti (ADR-0012). **F-22**: recorded here as DEFERRED WITH JUSTIFICATION pending the API
> layer, resolved instead by DELETION of `app/` in commit 5ae8ee7, because the stub displayed
> values not produced by the engine; a frontend is rebuilt at PROJECT_BACKLOG.md Phase 5
> (ADR-0003). The table below is otherwise preserved unmodified as dated evidence.

Base audit: MASTER_AUDIT_REPORT (audited HEAD 16ccea2). Every finding
carries one of: FIXED, RESOLVED BY SPECIFICATION, NOT APPLICABLE WITH
EVIDENCE, DEFERRED WITH EXPLICIT JUSTIFICATION.

| ID | Status | Fix location | Evidence |
|---|---|---|---|
| F-01 tropical houses vs sidereal planets | FIXED | astronomy_snapshot.py, house_positions.py (FLG_SIDEREAL) | Asc 239.0275081 matches swetest to <0.5 arcsec and legacy kernel to 0.0005 arcsec; frame test asserts >1 deg from tropical; commit 8c143c7 |
| F-02 silent Moshier fallback | FIXED | engine/astronomy/ephemeris.py; planet_positions.py | retflag 258 (SWIEPH) asserted for 10 bodies x 6 epochs; strict mode raises on fallback and out-of-range; commit 5b77472 |
| F-03 nakshatra_map index-as-longitude | FIXED | chart_nakshatra_builder.py, chart_builder.py | Map holds numbers 1..27, Rohini at 4, Revati at 27; integration test; commit 36c9d6f |
| F-04 nakshatra/pada boundary misclassification | FIXED | longitude_utils.py; nakshatra.py; pada.py; signs.py | 40.0 -> nakshatra 4 pada 1; all 27+108+12 boundaries x 11 offsets vs exact-arithmetic reference; 0 ULP violations; commit 4e9830d |
| F-05 equal-house documented as whole-sign | FIXED | house.py (both rules explicit); chart_planet_builder.py | Divergence case tested (asc 100/planet 95: whole=1, equal=12); D1 uses whole sign per documented decision; commit 4e9830d |
| F-06 ayanamsa Lahiri vs Krishnamurti contradiction | RESOLVED BY SPECIFICATION | astronomy/profile.py | Named profiles (parashari_lahiri, kp_krishnamurti); mode recorded in Provenance; no hidden default determines interpretation; commit 8c143c7 |
| F-07 collection gaps, broken cert harness | FIXED | pytest.ini, conftest.py, engine/tests/test_reference_astronomy.py, test_tier0_certification.py | Default pytest = 181 tests incl. reference values; legacy gate repaired, 4/4 when invoked; commit dfe1ca2 |
| F-08 chart utils crash on real charts | FIXED | chart_index/lookup/sort/mapper | Exercised against a real built chart in integration tests; commit 36c9d6f |
| F-09 pada semantic collision | FIXED | models + builders + navamsa_chart | nakshatra_pada (1-4) vs navamsa_number (1-9); embedded D9 summary equals standalone D9 for every planet (tested); commit 36c9d6f |
| F-10 calendar flag omitted | FIXED | core/julian_day.py | GREG_CAL explicit; policy documented; 1500 CE anchor test; commit 5ff57ca |
| F-11 fixed-offset live path, dead zoneinfo | FIXED | calculations.py, services/time_service.py | BirthData pipeline; DST, fold, 1944 Kolkata +06:30 tests; commit 5ff57ca |
| F-12 broken validation module | FIXED | core/validation.py + test_validation.py (17 tests) | lat/lon/tz/date/fold/DST-gap validation wired into calculate(); commit 5ff57ca |
| F-13 aspect primitive unnormalized | FIXED (primitive level) | astronomy/aspects.py | aspect(730,10)=0.0; range property test. Aspect SYSTEMS (Parashari 4/8, 5/9, 3/10 etc.) intentionally not claimed; deferred to the aspect-systems phase by design |
| F-14 roster inconsistency, no Rahu/Ketu | FIXED | planet_collection.py, sidereal_planets.py | Canonical 9 grahas + nodes + outers; Ketu = Rahu+180 with real node speed; opposition preserved end-to-end (tested); commit 8c143c7 |
| F-15 silent varga passthrough | FIXED | divisional_chart.py | UnsupportedVargaError for 13 recognized unimplemented vargas; D1 dispatch returns real chart; old passthrough test replaced with documented rationale; commit a0affad |
| F-16 dependency chaos | FIXED | requirements*, pyproject.toml, CI | pyswisseph name corrected everywhere; UTF-8 lock; installable package; CI runs gate on 3.11/3.12; commit dfe1ca2 |
| F-17 certification claims contradiction | FIXED | CURRENT_ENGINE_CERTIFICATION_STATUS.md | LEGACY CERTIFIED vs CURRENT ENGINE explicitly separated; historical files untouched; commit dfe1ca2 |
| F-18 D10 normalize guard missing | FIXED | dashamsa_chart.py | Explicit >=360 guard; -1e-16 -> 0.0/Aries by design, not parity accident; commit a0affad |
| F-19 boundary convention divergence | FIXED | dashamsa_chart.py + longitude_utils.py | One convention everywhere (1e-10 promote-up, top clamp); full D10 recertification after change (51,429-pt sweep 0 mismatches, pyjhora 120/120); commit a0affad |
| F-20 no provenance/frame metadata | FIXED | models/provenance.py, house_position.py, astronomy_snapshot.py | Frame, ayanamsa mode, house system, node policy, ephemeris mode, time basis on every snapshot; commit 8c143c7 |
| F-21 three version constants | FIXED | engine/version.py | Single source 0.3.0; all others derive; commit 5ff57ca |
| F-22 Flutter fake horoscope math | DEFERRED WITH JUSTIFICATION | - | Mandate rule 11 forbids modifying the app to compensate for engine defects; replacement requires the API layer (Phase 20), which is gated on engine certification. The stub remains clearly labeled temporary; blocking any release, tracked in ARCHITECTURE_STATUS.md |
| F-23 legacy kernel value | NOT APPLICABLE (INFO) | - | Mined as intended: FLG_SIDEREAL mechanism, strict-mode guard, GREG_CAL, Ketu derivation, cusp-tuple defense, and the cross-check oracle test all came from legacy/ |
| F-24 empty knowledge payloads | FIXED | engine/knowledge/data/*.json, astrology/dignity.py | BPHS dignity + naisargika tables with citations; Rahu/Ketu variants recorded, never silently chosen; classical anchor tests incl. Moon/Mercury asymmetry; commit dfe1ca2 |

## Ambiguities

| ID | Status | Resolution |
|---|---|---|
| A-1 ayanamsa | RESOLVED BY SPECIFICATION | Per-system CalculationProfile; Lahiri and Krishnamurti verified to differ by the expected 5-6 arcmin in tests; final per-system sign-off flagged for project owner in CURRENT_ENGINE_CERTIFICATION_STATUS.md |
| A-2 house semantics | RESOLVED BY SPECIFICATION | Three roles separated: Placidus cusps (data, labeled), whole-sign planet assignment (D1 decision, documented), equal-house available explicitly |
| A-3 boundary convention | RESOLVED BY SPECIFICATION | Single documented convention in longitude_utils.py with mathematical rationale; applied to signs, nakshatra, pada, houses, D9, D10 |
| A-4 certification status | RESOLVED BY SPECIFICATION | CURRENT_ENGINE_CERTIFICATION_STATUS.md; historical files unmodified |
| A-5 node/Ketu policy | RESOLVED BY SPECIFICATION | Rahu = policy node (mean default, true available), Ketu always derived +180; raw nodes still exposed; documented in planet_collection.py |
| A-6 pada terminology | RESOLVED BY SPECIFICATION | nakshatra_pada (1-4), navamsa_number (1-9), ChartPada documented as global 1-108 index; navamsa_pada kept as documented alias |
| A-7 version identity | RESOLVED BY SPECIFICATION | engine/version.py single source |

## Missing-test items (audit section 22 CRITICAL/HIGH lists)

T-1 ephemeris mode guard: FIXED (test_ephemeris.py, 8 tests).
T-2 sidereal ascendant reference: FIXED (test_reference_astronomy.py).
T-3 astronomy reference values in default run: FIXED (swetest values, Astrodienst fixture, J2000).
T-4 end-to-end D1 with real astronomy: FIXED (test_chart_integration.py, 8 tests).
T-5 validation module import/tests: FIXED (17 tests).
T-6 container-contract with non-empty planets: FIXED (integration + utils tests on real charts).
T-7 root tests collected: FIXED (reference tests live in engine/tests; legacy gate documented and runnable).
T-8 nakshatra/pada exact boundaries: FIXED (all boundaries x 11 offsets + ULP).
T-9 cross-varga D9 consistency: FIXED (embedded-vs-standalone agreement test).
T-10 house rule divergence case: FIXED.
T-11 negative/360 normalization sweeps for all modules: FIXED.
T-12 dispatcher coverage for all 16 advertised vargas: FIXED (explicit errors + tests).
T-13 timezone DST/fold/historical: FIXED.
T-14 roster consistency: FIXED (Rahu/Ketu tests; metadata keyed names now producible).
Deferred test items: polar-circle house behavior (needs a specified expected behavior first; flagged NOT YET VERIFIED), property-based hypothesis suite (nice-to-have; ULP + dense sweeps currently cover the same ground), multi-case holdout matrix vs engine/ (listed as the remaining step toward LOCK).
