# Astro Convergence Engine

Private source-of-truth repository for a deterministic, independently verifiable, multi-system astrology calculation platform.

## Current state

CURRENT ENGINE (`engine/`): LOCKED / TIER-0 CERTIFIED per `certification/CURRENT_ENGINE_LOCK.json` and `CURRENT_ENGINE_CERTIFICATION_STATUS.md`. The astronomical kernel (strict SWIEPH ephemeris, sidereal frame, calculation profiles, IANA time pipeline, Placidus cusp data, provenance on every snapshot) and the certified D1/D9/D10 calculations passed an 11-case holdout matrix against the bundled swetest 2.10.03 reference binary under both ratified profiles (Parashari = Lahiri, KP = Krishnamurti), max error 0.000180 arcsec across 528 comparisons.

LEGACY KERNEL (`legacy/`): historical Tier-0 certification evidence, described by `LOCK_MANIFEST.json` and `reports/`. Unmodified. It remains the migration reference for the future KP layer.

GENERIC VARGA FRAMEWORK: infrastructure only. The registry is empty by design; the certified D9/D10 production modules remain authoritative. Vargas other than D1/D9/D10 raise UnsupportedVargaError.

KP LAYER (`engine/kp/`): KP_CHAIN_V1 CERTIFIED per `certification/KP_CHAIN_V1_certification.json` (ADR-KP-001). Exact-rational KP lordship chains (SL/NL/SB/SS) and KP fact charts under the kp_krishnamurti profile, proven equivalent to the certified legacy kernel with zero categorical mismatches (51,429-point sweep, 19,679 boundary points, 11-case chart holdout, 200/200 transcribed fixture fields, independent validator). KP scope covers chains and fact charts ONLY.

DASHA LAYER (`engine/dasha/`): VIMSHOTTARI_V1 CERTIFIED per `certification/VIMSHOTTARI_V1_certification.json` (ADR-DASHA-001). Exact-rational Vimshottari maha/antar/pratyantar timelines, school-explicit seeding (parashari_lahiri or kp_krishnamurti Moon), year length pinned as an explicit DashaProfile (mean sidereal year, exactly 91314091/250000 days). Certified against the PyJHora external oracle by injecting the oracle's own Moon into this engine's timeline (D-007 methodology): 1,782 bhukti rows, zero lord mismatches, max start delta 1.4e-9 days; plus an independent closed-form validator (1,081 moon cases, exact arithmetic, zero failures). Other dasha systems and deeper levels are non-claims.

TRANSIT LAYER (`engine/transits/`): TRANSIT_V1 CERTIFIED per `certification/TRANSIT_V1_certification.json` (ADR-TRANSIT-001). Longitude-crossing events by station-aware bisection on the certified position pipeline (event residual bound 1e-4 arcsec, event-time guarantee 1e-6 day): sign and nakshatra ingresses, returns, natal conjunctions (retrograde multiplicity handled, directions flagged), and the profile-guarded natal-relative TransitView. Verified by a residual battery, an independent scan-plus-interpolation validator, and 24 PyJHora sankranti anchors under per-event derived tolerances (D-007). Aspect-system events, dasha-transit convergence, and interpretation are non-claims.

Explicit non-claims: no KP significators, four-step, ruling planets, or horary (Tier-1 KP_SIGNIFICATOR_V1 requires a frozen spec first, per D-008); no dasha systems beyond Vimshottari V1; no aspect-system transit events; no Jaimini, BNN/Nadi, numerology, or convergence functionality exists yet. Placidus behavior above the polar circles is NOT YET VERIFIED. UTC is treated as UT1 (bounded 0.9 s, recorded in Provenance).

## Verification gates

```bash
python -m pytest                                   # default gate (engine/tests)
python validate_d9_holdout.py                      # independent D9 holdout
python validate_d10_holdout.py                     # independent D10 holdout
python -m pytest test_tier0_certification.py test_official_swetest_reference.py   # legacy gate
python scripts/certify_current_engine.py           # regenerate 11-case holdout matrix
python validate_kp_holdout.py                      # independent KP chain holdout
python scripts/certify_kp_chain.py                 # regenerate KP_CHAIN_V1 certification
python validate_vimshottari_holdout.py             # independent Vimshottari holdout
python scripts/certify_vimshottari.py              # regenerate VIMSHOTTARI_V1 certification (needs PyJHora)
python validate_transits_holdout.py                # independent transit-event holdout
python scripts/certify_transits.py                 # regenerate TRANSIT_V1 certification (needs PyJHora)
```

The stored `certification/current_engine_certification.json` is never accepted as proof; the certifier regenerates it from scratch on every run. Do not commit an audit-run regeneration.

## Non-negotiable engineering rules

No component may be called certified without executable evidence, a frozen profile, independent references, and a reproducible report. Locked components (see `CURRENT_ENGINE_CERTIFICATION_STATUS.md` lock scope and `LOCK_MANIFEST.json` for the legacy kernel) must not change without a formal change request and full recertification. Astrology schools remain isolated; per-system ayanamsa profiles must never be overridden by a hidden default.

## Roadmap

See `ARCHITECTURE_STATUS.md` for the recommended order: KP migration from `legacy/kp.py` under the kp_krishnamurti profile, then Vimshottari dasha, transits, additional vargas through the generic registry (one at a time, each with classical source, rule table, independent reference, and certification artifact), aspect systems per school, evidence layer, API, and only then a production application.
