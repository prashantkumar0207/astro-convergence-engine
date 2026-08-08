# CURRENT ENGINE CERTIFICATION STATUS

Date: 2026-08-08
Scope: this document describes the CURRENT modular engine under `engine/`.
It supersedes NOTHING: `LOCK_MANIFEST.json`, `reports/`, `DECISION_LOG.md`
and `v1_1_engineering_decision.json` are historical evidence about the
LEGACY kernel and remain unmodified (audit finding F-17).

## The two kernels, clearly distinguished

LEGACY CERTIFIED (historical):
- Code: `legacy/engine.py` + `legacy/kp.py` (formerly packaged as `astro_kernel`).
- Status: Tier-0 certified at <= 0.5 arcsec against the swetest reference
  binary under the KRISHNAMURTI / mean node / Placidus / strict SWIEPH
  profile, per `LOCK_MANIFEST.json` and `reports/CERTIFICATION_REPORT.md`.
- Gate: `python -m pytest test_tier0_certification.py` (repaired in this
  remediation to point at the actual artifact locations; 4/4 passing).
- The LOCKED badge in LOCK_MANIFEST.json applies ONLY to this kernel.

CURRENT ENGINE (this codebase's future):
- Code: `engine/` (astronomy, astrology, models, calculations).
- Status after remediation: HOLDOUT-CERTIFIED (see below). LOCK
  recommended pending one human decision (per-system ayanamsa
  sign-off, A-1).
- Gate: the default `pytest` run (engine/tests) plus the two independent
  holdout validators. Everything below is collected by a bare `pytest`.

## What the current engine's gate verifies

Astronomy:
- Ephemeris: strict SWIEPH with return-flag inspection; silent Moshier
  fallback raises; bundled files verified present and actually used
  across 10 bodies and 6 epochs (engine/tests/test_ephemeris.py).
- Frame: planets, ascendant, and cusps all sidereal; verified against
  swetest-generated reference values (Sun/Moon/Asc/MC/cusps at the
  canonical epoch, <= 0.5 arcsec), the published Astrodienst 1946
  fixture through an explicit Fagan-Bradley profile, and the certified
  legacy kernel under an identical profile at sub-milliarcsecond
  agreement (engine/tests/test_reference_astronomy.py).
- Time: J2000 JD anchor exact; GREG_CAL explicit; IANA timezone
  conversion with DST, historical offsets (Asia/Kolkata 1944 +06:30),
  fold disambiguation, DST-gap rejection.

Astrology:
- D9 Navamsa and D10 Dashamsa: independently certified (dense sweeps vs
  first-principles classical rules, exact-arithmetic references,
  ULP-adversarial scans, pyjhora external oracle 108/108 and 120/120,
  classical anchors, holdout validators). D9 behavior bit-identical to
  the certified 16ccea2 implementation.
- D1: real chart builder wired end to end; whole-sign house rule
  (documented decision); nakshatra/pada hardened to the single
  project-wide boundary convention; real-birth integration tests with
  independently derived expectations.
- Dignity/friendship data: BPHS tables with citations in
  engine/knowledge/data/, verified by hand-entered classical anchors;
  Rahu/Ketu tradition variants recorded, never silently chosen.

## Explicit non-claims

- No dasha, transit, KP (in engine/), Jaimini, BNN/Nadi, numerology,
  or convergence functionality exists yet; nothing here certifies them.
- Vargas other than D1/D9/D10 raise UnsupportedVargaError by design.
- Planet strength (Shadbala) raises NotImplementedError by design.
- UTC is treated as UT1 (|dUT1| <= 0.9 s), recorded in Provenance.
- Polar-latitude house behavior is exercised only at 64.1 N; Placidus
  behavior above the polar circles remains NOT YET VERIFIED.

## Holdout certification (Phase 1 gate) - EXECUTED AND PASSED

Date: 2026-08-08. Runner: scripts/certify_current_engine.py. Archive:
certification/current_engine_certification.json (machine-readable,
regenerated from scratch on every run; stored JSON is never accepted
as proof). Collected gate: engine/tests/test_current_engine_certification.py.

- Matrix: the frozen 11-case holdout (1823 London through 2350 Paris,
  latitudes -33.9 to +64.1, plus two Moon nakshatra-boundary cases),
  identical to the legacy Tier-0 matrix and never used for tuning.
- Profiles: BOTH parashari_lahiri (SIDM 1) and kp_krishnamurti
  (SIDM 5), 264 planet comparisons and 264 cusp comparisons total
  against the independent swetest 2.10.03 C binary.
- Results: max planet error 0.000179 arcsec, max ascendant error
  0.000176 arcsec, max cusp error 0.000180 arcsec; zero Moshier
  fallbacks (strict mode); all four boundary-sensitive Moon
  classifications agree with exact rational arithmetic; the two
  profiles differ by the expected 5.811 arcmin, proving the profile
  system drives the computation (A-1 verified mechanically).
- These figures match the legacy kernel's archived certification
  precision (0.000179 arcsec), on the current engine's own code path.

## LOCK determination

STATUS: LOCKED / TIER-0 CERTIFIED (current engine).

Human sign-off recorded 2026-08-08 (project owner, verbatim):
"I confirm the intended per-system ayanamsa assignments for the
astrology engine: Parashari = Lahiri ayanamsa; KP = Krishnamurti
ayanamsa. These are intentional system-specific CalculationProfiles
and must remain isolated by methodology. Do not introduce a hidden
global/default ayanamsa that overrides the profile."

Binding consequences of the sign-off:
- engine/astronomy/profile.py: PARASHARI_LAHIRI (SIDM 1) and
  KP_KRISHNAMURTI (SIDM 5) are the ratified system profiles.
- The profile parameter is the ONLY path to an ayanamsa; no code may
  introduce a hidden global default that overrides it. (The
  DEFAULT_PROFILE constant exists solely as the parameter default of
  astronomy_snapshot/calculate and equals PARASHARI_LAHIRI; every
  snapshot records its actual profile in Provenance, so no output is
  ever ambiguous about which ayanamsa produced it.)
- Methodology isolation: KP-layer code must request KP_KRISHNAMURTI
  explicitly; Parashari-layer code PARASHARI_LAHIRI. Cross-system
  reuse of a snapshot computed under the other profile is forbidden.

Lock scope: the astronomical calculation kernel (ephemeris handling,
frame, profiles, houses, sidereal positions, JD/time pipeline) and the
certified D9/D10 divisional mathematics, as evidenced by
certification/current_engine_certification.json (max error 0.000180
arcsec across 528 comparisons, both profiles, 11 holdout cases) plus
the 186-test default gate. Changes inside the lock scope require the
same certification discipline used to establish it (re-run
scripts/certify_current_engine.py and the full gate; document the
diff).

The machine-readable lock record is
certification/CURRENT_ENGINE_LOCK.json. Historical legacy
certification artifacts (LOCK_MANIFEST.json, reports/) remain
untouched and continue to describe the legacy kernel only.
