# TIER-0 ASTRONOMICAL CORE - CERTIFICATION REPORT (v1.3, portable)
Generated during the certification run itself: 2026-07-10 22:46:00 UTC

Frozen profile: KRISHNAMURTI ayanamsha (SIDM 5) - MEAN node - Placidus - geocentric apparent -
sidereal - strict SWIEPH (silent Moshier fallback impossible; raises and fails the run).

Independent reference: Astrodienst swetest v2.10.03 (independent C binary, package-relative, version-verified at runtime).
Ephemeris files SHA-256 verified BEFORE certification:
- seas_18.se1  a2cd8fc33807c78ca9a700c91c2e042258b12fc4796519e00781440b5ad8b2e2
- semo_18.se1  1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7
- sepl_18.se1  ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66

Holdout: 11 cases, epochs 1823-2350, latitudes -33.9 to +64.1, second-level UT timestamps,
including two boundary-sensitive KP cases (Moon < 0.3 arcsec from a sub-sub boundary).
Holdout cases were never used to tune or debug the engine. Stored JSON from previous runs is
retained only in reports_historical/ and is never read by the certification pipeline.

## REQUIRED FINAL RESULT BLOCK
```
TEST SUITE: 11/11 PASS
SKIPPED TESTS: 0
PLANETARY HOLDOUT COUNT: 132
MAX PLANETARY ERROR: 0.000179 arcsec (H5_reykjavik_1992, Mercury)
MAX ASCENDANT ERROR: 0.000168 arcsec
MAX CUSP ERROR: 0.000176 arcsec (H9_paris_2350, house 6)
SIGN LORD MISMATCHES: 0
NAKSHATRA LORD MISMATCHES: 0
SUB LORD MISMATCHES: 0
SUB-SUB LORD MISMATCHES: 0
MOSHIER FALLBACK EVENTS: 0
HARDCODED CORRECTION/FITTING FOUND: NO
ENVIRONMENT-SPECIFIC ABSOLUTE PATH DEPENDENCIES: 0
FRESH EXTRACTION ONE-COMMAND REPRODUCTION: PASS

FINAL STATUS: TIER-0 NUMERICAL CORE - PORTABLY CERTIFIED <=0.5 ARCSECOND
```

Machine-readable results: reports/tier0_certification.json, reports/swetest_raw_outputs.json,
reports/pytest_results.xml, reports/regression_report.json (Brihat categorical regression,
regenerated this run: see structural check inside - comparison fixtures only, never fitted).
