# ARCHITECTURE STATUS - POST-REMEDIATION

## Layering (current, verified)

    BirthData
      -> validation (core/validation)
      -> IANA time (services/time_service)  -> JD UT (core/julian_day)
      -> AstronomySnapshot under explicit CalculationProfile
         [sidereal frame, strict SWIEPH, provenance-stamped]
      -> D1 chart (whole-sign; real builder on the factory path)
      -> D9 / D10 (certified) via dispatcher (errors on others)

Calculation remains fully separated from interpretation; no
interpretation layer exists yet, and the fact layer is now
trustworthy enough to build one on.

## What is production-grade now

engine/astronomy (ephemeris guard, sidereal frame, profiles),
engine/core (julian_day, timezone_engine, validation),
engine/services/time_service (live), engine/calculations,
engine/astrology: longitude_utils, signs, nakshatra, pada, house,
navamsa_chart, dashamsa_chart, divisional_chart, chart builders,
dignity accessors, engine/models (with provenance), the test suite.

## Deliberately unimplemented (explicit, error-raising or absent)

Vargas other than D1/D9/D10 (UnsupportedVargaError), planet strength
(NotImplementedError), aspect SYSTEMS (only the normalized separation
primitive exists), dasha, transits, KP in engine/ (legacy/kp.py is the
reference for migration), Jaimini, BNN/Nadi, numerology, evidence/
convergence, API routes beyond the demo endpoint.

## Remaining architectural work, in recommended order

1. Engine holdout matrix: run the 11-case geography/epoch matrix from
   scripts/certify_tier0.py against engine/ and archive machine-readable
   results; then declare the current-engine LOCK.
2. Generic divisional framework before any D2..D60: shared models
   (varga number + school on the chart), per-varga rule functions,
   D9/D10 migrated only with bit-identical output proof.
3. KP migration from legacy/kp.py (Fraction math preserved) under the
   kp_krishnamurti profile; then Vimshottari dasha (seeded by the now
   boundary-hardened Moon nakshatra); then transits with root-finding.
4. Aspect systems as separate modules per school; never one conflated
   engine.
5. Evidence layer consuming provenance-stamped facts; canonical
   identifier note: D1 signs are 1-based, varga signs 0-based; unify
   before the convergence layer joins facts across systems.
6. API layer serializing fact bundles; THEN replace the Flutter stub
   (F-22, deferred by mandate rule 11).

## Known open risks (honest list)

- Polar-latitude Placidus behavior: NOT YET VERIFIED (exercised to
  64.1 N only); define expected behavior before testing above the
  polar circles.
- scripts/ certification pipeline still targets the old astro_kernel
  packaging; the root gate (test_tier0_certification.py) was repaired,
  the pipeline scripts were not (deferred; the new engine gate is the
  default pytest run).
- UTC treated as UT1 (bounded 0.9 s, documented in Provenance);
  delta-T-aware UT1 handling would remove the caveat.
- Sidereal speeds are Swiss FLG_SIDEREAL outputs; fine for retrograde
  flags, review before high-precision speed work.
- Rahu/Ketu dignity/friendship variants recorded but no tradition
  profile selects them yet.
- app/ still contains the labeled-temporary fake horoscope stub
  (release-blocking; see F-22).
