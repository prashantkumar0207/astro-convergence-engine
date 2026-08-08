# FINAL CERTIFICATION REPORT - ASTRO-CONVERGENCE-ENGINE

Date: 2026-08-08. Remediation base: audited HEAD 16ccea2 (readiness
34/100). This report follows the mandate's Phase 26 requirements: it is
a fresh adversarial audit of the remediated state, not a rerun of the
remediation's own claims.

## 1. Fresh verification performed (independent of repository tests)

A. Repository inspection: working tree clean at every checkpoint; 8
   logical commits; no changes to legacy/, reports/, LOCK_MANIFEST.json,
   v1_1_engineering_decision.json, DECISION_LOG.md, swetest, *.se1,
   CHECKSUMS.sha256 (verified by git diff --name-only against 16ccea2).
B. Architecture inspection: layering intact; calculation still fully
   separated from interpretation; new modules documented.
C. Mathematical verification: D10 vs an independently coded classical
   Parashari rule, 51,429 points, 0 mismatches; D9 9th-harmonic
   identity, 0 mismatches; D9 output bit-identical (SHA-256 over
   51,429 outputs) to the certified 16ccea2 implementation.
D. Numerical boundary verification: 8,560-point final ULP battery
   across all division boundaries plus tiny negatives and 360
   multiples: 0 range violations, 0 sign/longitude disagreements.
E. Independent reference comparison: pyjhora oracle 108/108 (D9) and
   120/120 (D10); swetest binary values for Sun, Moon, Ascendant, MC,
   cusps 2 and 9 all within 0.5 arcsec (planets and ascendant within
   0.001 arcsec); certified legacy kernel agreement < 0.001 arcsec
   under an identical profile; Astrodienst published 1946 fixture
   through an explicit engine profile within 0.5 arcsec; J2000 exact.
F. Real-chart end-to-end: 1989-07-12 16:44 IST Patna through
   BirthData -> validation -> zoneinfo -> JD -> snapshot -> D1:
   Scorpio lagna, Sun Gemini/house 8/Punarvasu pada 2/D9 Taurus 8,
   Moon Libra/house 12/Swati pada 2/D9 Capricorn 4, Rahu/Ketu exactly
   opposed, provenance complete. ALL PASS.
G. Dependency/environment: fresh interpreter with cwd outside the
   repository runs the full pipeline (no cwd-dependent behavior);
   canonical pinned requirements; installable pyproject; CI defined.
H. API/app boundary: the demo endpoint now works (asdict); the app
   remains disconnected and its stub is release-blocking (F-22,
   deferred by mandate rule).
I. Original findings review: complete per-finding table in
   FINDINGS_MATRIX.md. Summary: F-01..F-21, F-24 FIXED or RESOLVED BY
   SPECIFICATION with evidence; F-22 DEFERRED (mandate rule 11);
   F-23 INFO consumed. A-1..A-7 all RESOLVED. T-1..T-14 all FIXED.

## 2. Certification statements (measurable form)

PASS: retflag contains FLG_SWIEPH for 60/60 body-epoch combinations;
      strict mode raises on all tested fallback paths.
PASS: 0 frame mismatches; ascendant within 0.001 arcsec of two
      independent references at 5 epochs/locations including 64.1 N.
PASS: 0/51,429 D10 classical-rule mismatches; 228/228 external oracle
      agreements; D9 bit-identical to its certified baseline.
PASS: 0 boundary violations across every sign, nakshatra, pada, D9,
      and D10 boundary at 11 offsets plus 20-25 ulps both directions.
PASS: real chart independently matches swetest within 0.5 arcsec and
      hand-derived classical classifications exactly.
PASS: 181/181 default-gate tests; 462 + 420 holdout validator cases;
      legacy gate 4/4 when invoked.
FAIL conditions checked and absent: no silent fallback, no frame
      mixing, no undocumented convention, no varga disguised as
      another, no contradictory identifier semantics in models
      (one residual convention note: D1 signs 1-based vs varga signs
      0-based, documented and flagged for unification before the
      convergence layer).

## 3. Readiness scorecard (0-100)

| Component | Audited | Now | Basis |
|---|---|---|---|
| Astronomical kernel | 25 | 82 | strict SWIEPH, sidereal frame, profiles, provenance, reference tests; UT1 caveat and polar gap remain |
| D1 / Rashi | 30 | 80 | real pipeline, hardened primitives, integration-tested; sign-index convention note |
| Nakshatra | 45 | 90 | exact boundaries verified against exact arithmetic; names complete |
| D9 | 95 | 95 | unchanged behavior, terminology clarified |
| D10 | 92 | 94 | guard added, convention unified, recertified |
| Divisional framework | 35 | 55 | dispatcher honest; generic contract still to design before D2..D60 |
| House system | 20 | 68 | three roles separated and documented; polar behavior unverified |
| Planetary metadata | 25 | 60 | dignity/friendship data with citations; combustion/temporary/compound computation pending |
| Aspects | 10 | 30 | primitive correct and normalized; no systems yet (by design) |
| Dasha | 0 | 0 | not built (gated, correctly) |
| Transits | 0 | 0 | not built (gated, correctly) |
| Parashari architecture | 30 | 55 | primitives now trustworthy; bhava/yoga/karaka layers pending |
| KP architecture | 25 | 40 | kp_krishnamurti profile ready; legacy Fraction math awaiting migration |
| Jaimini architecture | 10 | 15 | whole-sign now exists correctly; nothing else |
| BNN/Nadi architecture | 10 | 15 | trustworthy nakshatra facts now exist |
| Numerology isolation | 50 | 55 | still nothing to violate the boundary |
| Evidence engine | 15 | 30 | provenance-stamped facts exist; identifier unification pending |
| Testing | 25 | 78 | reference-anchored, boundary-exhaustive, integrated; property-based suite optional |
| API/data model | 30 | 65 | provenance, docs, honest endpoint; validation at model layer still shallow |
| Performance | 60 | 62 | unchanged; global swe state documented |
| Documentation | 30 | 62 | status docs now authoritative and non-contradictory |
| Maintainability | 45 | 65 | dead code documented (not yet removed by design; post-stability task) |

CURRENT READINESS: 61/100 (was 34/100). The remaining 39 points are
almost entirely unbuilt layers (dasha, transits, KP, aspects systems,
convergence), not defects in built code.

## 4. Remaining risks

Listed with honesty in ARCHITECTURE_STATUS.md: polar-latitude houses
(NOT YET VERIFIED), UTC-as-UT1 (documented, bounded), scripts/ legacy
pipeline (superseded, unrepaired beyond the root gate), sidereal speed
semantics (documented), Rahu/Ketu tradition variants awaiting profile
selection, Flutter stub (release-blocking), 1-based/0-based sign
convention split (documented; unify before convergence).

## 5. Recommended next development phase

Run the 11-case holdout matrix against engine/ and archive the results
(the last step to a current-engine LOCK), then design the generic
divisional framework, then migrate KP from legacy/, then Vimshottari.

## 6. Verdict

The engine is now a deterministic, independently verified,
provenance-aware calculation foundation. Its outputs at the verified
epochs and locations match two independent oracles and the certified
legacy kernel to within the project's frozen tolerance, and its failure
modes are loud instead of silent. It is fit to serve as the foundation
for the interpretation layers, which should be built in the order above.
