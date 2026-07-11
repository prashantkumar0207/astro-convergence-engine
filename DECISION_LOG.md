# Decision Log

## D-001 — Canonical numerical authority

Tier 0 is certified against Astrodienst swetest 2.10.03 under an identical frozen calculation profile. Proprietary astrology applications are comparison fixtures, not automatic astronomical ground truth.

## D-002 — Numerical tolerance

Maximum absolute numerical error for identical calculation profiles is <= 0.5 arc-second. Percentage tolerance is prohibited.

## D-003 — KP hierarchy tolerance

SL/NL/SB/SS categorical mismatch tolerance is zero.

## D-004 — Anti-fitting

No arbitrary body-specific corrections, reverse-solved coordinates/times, or fitting to rounded screenshot DMS values.

## D-005 — Tier 0 portability correction

An earlier package had environment-specific `/home/claude/...` certification paths and produced a skipped test on fresh extraction. Version 1.3 portable removed executable absolute-path dependencies, resolves bundled resources package-relatively, verifies ephemeris checksums, fails on missing certification dependencies/fallback, and reproduces the full certification with one command.

## D-006 — Tier 0 final evidence

Fresh execution of `tier0_numerical_core/run_all.sh` reproduced 11/11 PASS, 0 skipped, 132 planetary holdout comparisons, maximum planetary error 0.000179 arcsec, maximum Ascendant error 0.000168 arcsec, maximum cusp error 0.000176 arcsec, zero SL/NL/SB/SS mismatches, zero Moshier fallback events, zero hard-coded fitting findings, and zero environment-specific absolute-path dependencies.

## D-007 — External app differences

AstroSage, Brihat, KundliStar, or another proprietary application's numerical DMS difference does not automatically reopen Tier 0. First compare exact calculation profiles, place coordinates, timezone handling, ayanamsha variant, node mode, ephemeris flags, and house procedure.

## D-008 — Next engineering tier

The next tier is KP_SIGNIFICATOR_V1. Its methodology specification must be frozen before implementation. Claude may be used as an implementation engineer, but implementation is accepted only after independent spec audit and adversarial/holdout validation.
