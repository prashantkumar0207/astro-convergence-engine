# REMEDIATION SUMMARY

Mandate: full remediation of the MASTER audit findings at HEAD 16ccea2.
Result: every actionable finding is FIXED or RESOLVED BY SPECIFICATION;
one item (F-22, the Flutter stub) is DEFERRED with justification
required by the mandate's own safety rules. Nothing was pushed.

## Commit chain (each independently verified before the next began)

1. 5b77472  F-02: deterministic ephemeris initialization, strict mode,
   return-flag inspection, out-of-range policy. 8 tests.
2. 8c143c7  F-01/A-1/F-14/F-20: sidereal houses (FLG_SIDEREAL, the
   certified convention), sidereal planets computed directly (swetest
   proved subtraction 9.57 arcsec off), CalculationProfile system,
   canonical Rahu/Ketu roster, Provenance on every snapshot. 9
   reference tests incl. legacy-kernel cross-check at <0.001 arcsec.
3. 5ff57ca  F-10/F-11/F-12/F-21: GREG_CAL policy, IANA timezone live
   path (DST, fold, 1944 Kolkata +06:30), input validation wired,
   single version source. 29 tests.
4. 4e9830d  F-04/F-05/A-2/A-3/F-13: one project-wide boundary
   convention with mathematical rationale, hardened nakshatra/pada/
   sign/house primitives, explicit whole-sign vs equal-house rules,
   normalized aspect primitive. 21 tests incl. exact-arithmetic
   reference and ULP scans.
5. 36c9d6f  F-03/F-08/F-09/A-6: real D1 pipeline on the factory path,
   nakshatra map fixed, chart utilities honor the dict contract,
   canonical terminology (nakshatra_pada / navamsa_number), embedded
   D9 summary now agrees with the standalone D9 chart. 8 integration
   tests against independently derived values.
6. a0affad  F-15/F-18/F-19: UnsupportedVargaError instead of silent D1
   passthrough, D10 normalization guard, unified boundary convention,
   full D9/D10 recertification (D9 bit-identical to 16ccea2; D10
   0/51,429 sweep mismatches; pyjhora 228/228).
7. dfe1ca2  F-07/F-16/F-17 + metadata: BPHS dignity and friendship
   data with citations behind a single accessor, honest
   NotImplementedError strength, pytest collection repair, legacy
   certification gate repaired (4/4), unified dependencies, pyproject,
   CI workflow, CURRENT_ENGINE_CERTIFICATION_STATUS.md.
8. (this commit) Final adversarial audit + the six deliverable
   documents.

## Headline numbers

- Suite: 99 shape-level tests before; 181 tests after, including
  astronomical reference values, boundary matrices, integration, and
  provenance checks. 0 failures, 0 skips.
- The two BLOCKER defects are fixed and regression-locked: ascendant
  now 239.0275081 (was 262.7410, a 23.71 deg frame error) and
  ephemeris mode swieph with strict guard (was silent Moshier).
- Independent verification: 51,429-point sweeps (0 mismatches),
  8,560-point final ULP battery (0 violations), pyjhora oracle 228/228,
  swetest reference <0.5 arcsec, legacy kernel <0.001 arcsec, exact
  J2000 anchor.
- Readiness: 34/100 (audited) -> 61/100 (assessed post-remediation;
  scorecard in FINAL_CERTIFICATION_REPORT.md). The gap to higher
  scores is unbuilt functionality (dasha, transits, KP, aspects,
  convergence), not defects in what exists.

## Deferred (explicit)

- F-22 Flutter stub replacement: forbidden by mandate rule 11 until
  the API layer exists; release-blocking, tracked.
- scripts/ legacy pipeline repair beyond the root gate: the new engine
  gate supersedes it for current code; the scripts document the
  historical astro_kernel packaging.
- Phases 13-19 (dasha, transits, KP, Jaimini, BNN, numerology,
  evidence): gated by the mandate itself on a certified fact layer;
  the fact layer is now ready for them. Recommended order in
  ARCHITECTURE_STATUS.md.
- Polar-circle house behavior: needs a specification decision before a
  test can assert anything; flagged NOT YET VERIFIED.
