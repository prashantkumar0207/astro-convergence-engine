# Astro Convergence Engine

Private source-of-truth repository for a deterministic multi-system astrology calculation, methodology, validation, and convergence engine.

## Current project state

- Tier 0 Numerical Core: PORTABLY CERTIFIED and LOCKED against the frozen canonical Swiss Ephemeris profile.
- Tier 1 KP Significator: SPECIFICATION PENDING.
- Tier 2 Four-Step: NOT STARTED.
- Tier 3 CIL: NOT STARTED.

## Non-negotiable engineering rule

No tier may be marked LOCKED without executable evidence, automated regression tests, a frozen specification/profile, and a reproducible certification report.

## Tier 0 quick verification

```bash
cd tier0_numerical_core
./run_all.sh
```

Expected final status:

`TIER-0 NUMERICAL CORE - PORTABLY CERTIFIED <=0.5 ARCSECOND`

See `LOCK_MANIFEST.json` and `docs/DECISION_LOG.md` before changing a locked tier.
