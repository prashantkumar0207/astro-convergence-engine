# Decision Log

> **CLASSIFICATION NOTE (added 2026-08-11 by ADR-0022, PROPOSED, pending owner ratification).**
>
> This file is the **ROOT TECHNICAL DECISIONS** register (D-001 through D-008). Its status under
> the governance hierarchy recorded in `docs/DECISION_LOG.md` ADR-0022 is:
>
> **OPERATIVE, SUBORDINATE, AND CLOSED TO NEW ENTRIES.**
>
> *Operative* means these decisions still bind. They are not historical. D-001 fixes swetest
> 2.10.03 as the numerical authority, D-002 the 0.5 arcsecond tolerance, D-003 zero categorical
> tolerance for the KP hierarchy, D-004 the anti-fitting rule, and D-007 the handling of external
> oracle divergence. All of these are cited live by the certification scripts and by ADR-0006,
> ADR-0007 and ADR-0008. Labelling them historical would imply they no longer bind, which would be
> a substantive weakening that no decision authorises.
>
> *Subordinate* means that where a D-00x entry and an ADR-000x entry conflict, **the ADR governs**,
> and the conflict is recorded rather than resolved silently.
>
> *Closed* means all future decisions are issued as ADR-000x in `docs/DECISION_LOG.md` only. No
> entry in this file is deleted, renumbered or rewritten; provenance is preserved intact.
>
> D-008 is the one entry carrying a sequencing claim rather than a technical constraint. Its
> methodology requirement stands and is generalised; its sequencing claim is superseded. See
> ADR-0027. D-008 is **clarified, not superseded**, and nothing in it authorises implementation.

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
