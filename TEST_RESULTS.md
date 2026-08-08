# TEST RESULTS - POST-REMEDIATION

Date: 2026-08-08. HEAD: see git log (remediation chain 5b77472..dfe1ca2 on top of 16ccea2).

## Exact runs executed at final verification

| Run | Result |
|---|---|
| `python -m pytest -q` (default gate) | 181 passed, 0 failed, 0 skipped |
| `python validate_d9_holdout.py` | ALL INDEPENDENT NAVAMSA CASES PASSED (108 midpoint + 312 boundary) |
| `python validate_d10_holdout.py` | ALL INDEPENDENT PARASHARI D10 CASES PASSED (462 cases incl. 12 classical anchors) |
| `python -m pytest test_tier0_certification.py test_official_swetest_reference.py` (legacy gates, explicit) | 5 passed |
| Clean-environment pipeline (fresh interpreter, cwd=/tmp) | OK; asc 239.0275, ephemeris_mode swieph |

Baseline before remediation: 99 passed (shape-level assertions only; zero astronomical reference values collected).

## Independent numerical verification (fresh, final pass)

| Check | Cases | Failures |
|---|---|---|
| D10 sign vs independent classical Parashari rule (dense sweep) | 51,429 | 0 |
| D9 longitude vs 9th-harmonic identity (off-boundary) | 51,429 sweep grid | 0 |
| D1 primitives range invariants over the same sweep | 51,429 | 0 |
| ULP-adversarial scans, D9+D10 sign/longitude agreement + range (final pass) | 8,560 | 0 |
| ULP scans at commit a0affad (larger battery) | 7,206 (D10) + 6,480 (D9, prior) | 0 |
| Nakshatra/pada/sign boundary matrix vs exact-arithmetic reference | 27, 108, and 12 boundaries x 11 offsets each (in suite) | 0 |
| pyjhora external oracle, D9 midpoints | 108 | 0 |
| pyjhora external oracle, D10 midpoints (Traditional Parasara) | 120 | 0 |
| D9 behavior vs certified 16ccea2 source (SHA-256 over 51,429 outputs) | 1 hash comparison | identical |
| Engine vs swetest binary (Sun, Moon, Asc, MC, cusps 2 and 9) | 6 values | all < 0.5 arcsec (asc/planets < 0.001 arcsec) |
| Engine vs certified legacy kernel, identical profile | 6 planets + asc | all < 0.001 arcsec |
| Astrodienst published 1946 fixture through engine profile | Sun, Moon | < 0.5 arcsec |
| J2000 Julian Day anchor | 1 | exact (2451545.0) |
| Ephemeris retflag SWIEPH | 10 bodies x 6 epochs | 60/60 |
| Frame consistency across epochs/locations (1900 London, 1992 Reykjavik 64.1N, 2000 Sydney, 2350 Paris) | 4 cases | 0 deviations (< 1e-6 arcsec vs direct sidereal houses) |

## New test files added by the remediation

test_ephemeris.py (8), test_reference_astronomy.py (9),
test_validation.py (17 incl. parametrized), test_time_service.py (5),
test_boundary_hardening.py (13, several exhaustive loops),
test_chart_integration.py (8), test_dignity.py (6), plus additions to
test_julian_day.py (3) and test_calculations.py (rewritten, 4), and
spec-correct replacements in test_divisional_chart.py,
test_chart_factory.py, test_chart*.py, test_planet_strength.py,
test_planet_collection.py, test_navamsa_chart.py.

## Tests replaced (mandate rule 4: incorrect behavior encoded)

- test_divisional_chart_preserves_unsupported_divisions: locked in the
  silent D1 passthrough; replaced by an UnsupportedVargaError test.
- test_chart_factory "D1 == snapshot": locked in the placeholder D1;
  replaced by real-Chart assertions.
- test_rashi_chart/test_chart identity tests: same reason.
- test_planet_strength "== 0.0": locked in a placeholder masquerading
  as a computed strength; replaced by NotImplementedError assertion.
- test_chart_lookup/sort/index tuple-based fixtures: violated the
  declared dict contract; replaced with contract-correct fixtures.
- 12-planet roster counts updated to 14 (canonical Rahu/Ketu added).
Each replacement is documented inline in the test file.

## Known behavior changes vs pre-remediation (all deliberate, documented)

1. Ascendant/cusps sidereal (was tropical): ~23.7 deg shift. THE fix.
2. Sidereal planets via FLG_SIDEREAL (was ayanamsa subtraction):
   9.57 arcsec shift to the certified/swetest convention.
3. Ephemeris SWIEPH (was silent Moshier): up to ~0.45 arcsec (Moon).
4. Exact nakshatra/pada boundaries classify into the next division.
5. D1 planet house numbers use whole sign (was equal house).
6. Unsupported vargas raise (was silent D1 passthrough).
7. calculate() takes BirthData (datetime variant retained as
   calculate_from_datetime).
