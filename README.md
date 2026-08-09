# Astro Convergence Engine

Private source-of-truth repository for a deterministic, independently verifiable, multi-system astrology calculation platform.

## Current state

CURRENT ENGINE (`engine/`): LOCKED / TIER-0 CERTIFIED per `certification/CURRENT_ENGINE_LOCK.json` and `CURRENT_ENGINE_CERTIFICATION_STATUS.md`. The astronomical kernel (strict SWIEPH ephemeris, sidereal frame, calculation profiles, IANA time pipeline, Placidus cusp data, provenance on every snapshot) and the certified D1/D9/D10 calculations passed an 11-case holdout matrix against the bundled swetest 2.10.03 reference binary under both ratified profiles (Parashari = Lahiri, KP = Krishnamurti), max error 0.000180 arcsec across 528 comparisons.

LEGACY KERNEL (`legacy/`): historical Tier-0 certification evidence, described by `LOCK_MANIFEST.json` and `reports/`. Unmodified, and verified so by diff at every phase. It served as the equivalence oracle for the KP chain migration (ADR-0006) and is retained per `docs/LEGACY_KERNEL_MIGRATION.md`, which forbids retiring it before all certified functionality has been migrated.

GENERIC VARGA FRAMEWORK: in certified production use. The certified D9/D10 production modules remain authoritative and are never routed through the registry, which refuses those divisions by contract. The sanctioned registry contents are the single constant `engine.astrology.CERTIFIED_PRODUCTION_VARGAS`; every division outside the certified eight raises UnsupportedVargaError.

KP LAYER (`engine/kp/`): KP_CHAIN_V1 CERTIFIED per `certification/KP_CHAIN_V1_certification.json` (ADR-0006). Exact-rational KP lordship chains (SL/NL/SB/SS) and KP fact charts under the kp_krishnamurti profile, proven equivalent to the certified legacy kernel with zero categorical mismatches (51,429-point sweep, 19,679 boundary points, 11-case chart holdout, 200/200 transcribed fixture fields, independent validator). KP scope covers chains and fact charts ONLY.

DASHA LAYER (`engine/dasha/`): VIMSHOTTARI_V1 CERTIFIED per `certification/VIMSHOTTARI_V1_certification.json` (ADR-0007). Exact-rational Vimshottari maha/antar/pratyantar timelines, school-explicit seeding (parashari_lahiri or kp_krishnamurti Moon), year length pinned as an explicit DashaProfile (mean sidereal year, exactly 91314091/250000 days). Certified against the PyJHora external oracle by injecting the oracle's own Moon into this engine's timeline (D-007 methodology): 1,782 bhukti rows, zero lord mismatches, max start delta 1.4e-9 days; plus an independent closed-form validator (1,081 moon cases, exact arithmetic, zero failures). Other dasha systems and deeper levels are non-claims.

VARGA REGISTRY, FIRST PRODUCTION ENTRY: D3 Drekkana (Parashara variant) CERTIFIED per `certification/VARGA_D3_V1_certification.json` (ADR-0009), served through the generic framework under (3, "parashara"). Rule expressed as frozen SegmentVargaRule literals verified cell by cell against a second transcription and a trine re-derivation; 51,429-point sweep and full ULP boundary battery under the locked convention; PyJHora pure-math oracle 3,600/3,600; registration proven non-invasive (D1/D9/D10 dispatch bit-identical across registration by SHA-256 sweep, refusals intact). Other drekkana variants and all other vargas remain non-claims.

VARGA REGISTRY, SECOND PRODUCTION ENTRY: D12 Dwadasamsa (Parashara variant) CERTIFIED per `certification/VARGA_D12_V1_certification.json` (ADR-0010), the first production use of the CyclicVargaRule path; with it both certified rule contracts carry production traffic. Same six-gate discipline as D3: cell-verified literals, 51,429-point sweep, full ULP battery at all 144 boundaries, PyJHora oracle 3,600/3,600, registration proven non-invasive (D9/D10 bit-identical, refusals intact), independent validator. The sanctioned registry state is the single constant engine.astrology.CERTIFIED_PRODUCTION_VARGAS.

VARGA REGISTRY, BATCH THREE THROUGH FIVE: D7 Saptamsa, D30 Trimsamsa, and D2 Hora (Parashara variants) CERTIFIED per `certification/VARGA_D7_V1_certification.json`, `VARGA_D30_V1_certification.json`, and `VARGA_D2_V1_certification.json` (ADR-0011, ADR-0011, ADR-0011). Same six-gate discipline per varga: dual-transcribed literals (D7's parity start table, D30's tara-graha unequal segments with a rulership re-derivation, D2's pinned two-sign Leo/Cancer output space), 51,429-point sweeps, ULP batteries, PyJHora Parasara oracles 3,600/3,600 each, non-invasive registration (D9/D10 bit-identical), independent by-name validators. The registry now serves D2, D3, D7, D12, D30 under parashara.

PARASHARI SCHOOL LAYER (`engine/parashari/`): PARASHARI_DRISHTI_V1 CERTIFIED per `certification/PARASHARI_DRISHTI_V1_certification.json` (ADR-0012), the first module of the school-separated aspect-systems architecture. Full (purna) graha drishti facts (aspected signs, whole-sign houses, planets) from certified Parashari placements: dual-transcribed offset table, exhaustive 84-pair combinatorics, PyJHora oracle over the 11-case holdout (154 comparisons, zero mismatches), independent name-counting validator. Node-cast aspects are excluded by approved decision AS-B (recorded variant); sputa drishti, Jaimini rashi drishti, Western aspects, yogas, and interpretation are non-claims.

TRANSIT LAYER (`engine/transits/`): TRANSIT_V1 CERTIFIED per `certification/TRANSIT_V1_certification.json` (ADR-0008). Longitude-crossing events by station-aware bisection on the certified position pipeline (event residual bound 1e-4 arcsec, event-time guarantee 1e-6 day): sign and nakshatra ingresses, returns, natal conjunctions (retrograde multiplicity handled, directions flagged), and the profile-guarded natal-relative TransitView. Verified by a residual battery, an independent scan-plus-interpolation validator, and 24 PyJHora sankranti anchors under per-event derived tolerances (D-007). Aspect-system events, dasha-transit convergence, and interpretation are non-claims.

SIGN CONVENTIONS (`engine/astrology/sign.py`, `sign_conventions.py`): SIGN_CONVENTION_V1 CERTIFIED per `certification/SIGN_CONVENTION_V1_certification.json` (ADR-0012). The repository carries two certified, locked sign-index conventions by history: every VARGA sign output is 0-based (including certified D9/D10 and all registry vargas) and every RASHI-level output is 1-based (D1 fields, KP chains, drishti). Neither is renumbered. Instead an inert `Sign` value type carries the convention explicitly, additive accessors expose the opposite view on every sign-carrying model, and `SIGN_FIELD_CONVENTIONS` is the single declared source of truth, enforced by a collected gate that FAILS when a new sign-typed field is added without a declaration. Each declaration is proven by a discriminating witness (a value impossible under the other convention) observed on real charts. This is the documented prerequisite for the future convergence layer.

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
python validate_d3_holdout.py                      # independent D3 drekkana holdout
python scripts/certify_d3.py                       # regenerate VARGA_D3_V1 certification (needs PyJHora)
python validate_d12_holdout.py                     # independent D12 dwadasamsa holdout
python scripts/certify_d12.py                      # regenerate VARGA_D12_V1 certification (needs PyJHora)
python validate_d7_holdout.py                      # independent D7 saptamsa holdout
python scripts/certify_d7.py                       # regenerate VARGA_D7_V1 certification (needs PyJHora)
python validate_d30_holdout.py                     # independent D30 trimsamsa holdout
python scripts/certify_d30.py                      # regenerate VARGA_D30_V1 certification (needs PyJHora)
python validate_d2_holdout.py                      # independent D2 hora holdout
python scripts/certify_d2.py                       # regenerate VARGA_D2_V1 certification (needs PyJHora)
python validate_parashari_drishti_holdout.py       # independent graha drishti holdout
python scripts/certify_parashari_drishti.py        # regenerate PARASHARI_DRISHTI_V1 certification (needs PyJHora)
python scripts/certify_sign_convention.py          # regenerate SIGN_CONVENTION_V1 certification
```

The stored `certification/current_engine_certification.json` is never accepted as proof; the certifier regenerates it from scratch on every run. Do not commit an audit-run regeneration.

## Non-negotiable engineering rules

No component may be called certified without executable evidence, a frozen profile, independent references, and a reproducible report. Locked components (see `CURRENT_ENGINE_CERTIFICATION_STATUS.md` lock scope and `LOCK_MANIFEST.json` for the legacy kernel) must not change without a formal change request and full recertification. Astrology schools remain isolated; per-system ayanamsa profiles must never be overridden by a hidden default.

## Roadmap

The ratified roadmap is still OPEN (`docs/OPEN_QUESTIONS.md` Q8). `docs/PROJECT_BACKLOG.md` is the enumerated plan of record: Phase 1 Core Intelligence (Question, Knowledge, Inference and Prediction engines) precedes Phase 2 Astrology Systems, then Phase 3 validation against historical cases, Phase 4 API, Phase 5 frontend, Phase 6 production. The astrology layers certified so far are Phase 2 content built ahead of Phase 1; that divergence is recorded in `docs/DECISION_LOG.md` ADR-0013. `ARCHITECTURE_STATUS.md` carries the remediation-era engineering order for reference, not as a ratified sequence.
