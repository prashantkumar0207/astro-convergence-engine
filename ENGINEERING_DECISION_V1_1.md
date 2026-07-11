# ASTRO KERNEL V1.1 — ENGINEERING DECISION

## Status
**NOT FULLY LOCKED.** The package now distinguishes canonical Swiss-Ephemeris accuracy from Brihat compatibility.

## Executed evidence
- 7 pytest tests pass.
- KP interval engine: 200/200 SL/NL/SB/SS fields exact on the 50 available transcribed planet+cusp fixture items from Cases C and D.
- Independent Astrodienst `swetest` 2.10.03 published fixture (28 Dec 1946 09:33 UT, sid0): local Moshier calculation differs by **0.0106 arcsec for Sun** and **0.1699 arcsec for Moon**; maximum **0.1699 arcsec**, passing the 0.5 arcsec target for this independent fixture.
- Brihat compatibility still fails: Case C maximum planet residual 166.4 arcsec; Case D 703.9 arcsec. This is not a permissible accuracy reference for the canonical Swiss profile.

## Code corrections made
1. Removed `Fraction(float)` binary-expansion path; KP now converts ephemeris floats via `Decimal(str(x))` before exact rational interval ownership.
2. Removed meaningless `or True` test assertion.
3. Added actual ephemeris-mode reporting.
4. Added strict SWIEPH mode that raises if Swiss data files are missing and Swiss silently falls back.
5. Added an independent official Astrodienst swetest regression test.

## Exact blocker to full ±0.5 arcsecond lock
A full lock needs a **larger independent reference set for all required planets and Placidus cusps under an identical calculation profile**. The current environment does not contain `sepl_18.se1` and `semo_18.se1`; therefore production SWIEPH cannot be certified here. For cusps, exact reference latitude/longitude and identical sidereal-house settings are mandatory.

## Required production validation
Pin Swiss Ephemeris 2.10.03-compatible data files `sepl_18.se1` and `semo_18.se1`, record SHA-256, run strict SWIEPH, and compare against official Astrodienst swetest/JPL holdout outputs generated with identical flags. Accept only if max absolute planetary and cusp residual is <=0.5 arcsec and all KP categorical fields have zero mismatches.

## Decision
Do **not** regenerate the engine from scratch. Continue from this codebase. KP hierarchy is solved at rule level on available fixtures. The remaining foundation work is independent all-body/cusp numerical certification, not more Brihat screenshot fitting.
