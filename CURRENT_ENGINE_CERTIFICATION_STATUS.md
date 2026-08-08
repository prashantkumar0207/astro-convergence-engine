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
- Status after remediation: REFERENCE-VERIFIED, working toward full
  certification. Not yet claimed as LOCKED.
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

## Toward a LOCKED claim for the current engine

Remaining before a LOCK equivalent to the legacy one: a full multi-case
holdout run (the 11-case geography/epoch matrix of
scripts/certify_tier0.py) executed against engine/ with archived
machine-readable results, and a decision record for the per-system
ayanamsa profiles (A-1) signed off by the project owner.
