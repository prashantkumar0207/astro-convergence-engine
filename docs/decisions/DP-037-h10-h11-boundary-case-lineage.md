<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents evidence, a lineage reconstruction and a classification. **DECIDES NOTHING.** Requires owner approval. Renames nothing, corrects no label, changes no production code, regenerates no artifact, and does NOT close H10/H11. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-09-15 |
| Review cadence | TBD |

# DP-037. H10/H11 boundary-sensitive case lineage and surface classification

Written under the owner's "CEO AUTHORIZATION — PROCEED WITH DP-037 FULL LINEAGE
PAPER" instruction, after `DP-037` was registered before drafting per `ADR-0040`
(commit `d47ad63`). Reconstructed against `main` at
`7521a4e8976981f8fef0f5f87c05d499aef3d063`.

**In scope:** what each surface actually contains, actually asserts, and actually
depends on, reconstructed from the implementation rather than from prior summaries.

**Not in scope, and not done:** renaming any case, altering any holdout datum,
modifying certification logic, regenerating any artifact, changing any
certification status, editing `ADR-0072`, or closing H10/H11.

---

## 0. A withdrawn finding, recorded so it cannot re-enter the record

An earlier status report to the owner claimed the affected surfaces "do not share
identical case data", inferring it from a ~20.82 degree Moon discrepancy against
`ADR-0072`'s pinned values, characterised as about 37.8 hours of Moon motion.

**That finding is withdrawn in full. It was a harness error, not repository
evidence.** Two mistakes compounded in the measuring script: it used
`timezone="Asia/Kolkata"` where every time-bearing surface uses `"UTC"`, and it
read `snapshot.planets.planets` (tropical) where the reference implementation
reads `snapshot.sidereal_planets`. Correcting both reproduces `ADR-0072`'s pinned
value exactly:

```
tz="UTC",           sidereal_planets  -> Moon 339.791988042, nakshatra distance 6.458655
ADR-0072 pinned                       ->      339.791988042,                    6.458654709
tz="Asia/Kolkata",  planets.planets   -> Moon   0.607608975   <- the erroneous measurement
```

Nothing in this paper rests on the withdrawn result, and it must not be cited as
evidence of repository inconsistency. The surfaces that carry a time **do** share
identical inputs.

---

## 1. The surfaces, as the tree actually contains them

`ADR-0072` recorded the two cases as reused "in eight other certifiers/validators".
A repository-wide search finds the identifiers in **ten live surfaces** plus
`engine/tests/test_vimshottari_m02_boundary_holdout.py`, which is the already-
corrected surface and is therefore not a subject of this paper.

An eleventh surface, `scripts/certify_tier0.py`, carried the identifiers until it
was **retired under M-4** (`ADR-0097`, commit `3e1d199`, merged as `7521a4e8`). It
could never execute - it imported the `astro_kernel` package, which no longer
exists - so it never produced evidence about these cases at all. The live surface
count is therefore **ten**, not eleven, and was eleven only at the moment the
investigation was authorised.

| # | Surface | Case lines | `boundary_sensitive` set | Time basis | Basis provenance |
|---|---|---|---|---|---|
| 1 | `scripts/certify_current_engine.py` | L74, L75 | **YES** | UTC | L210 `timezone="UTC"` |
| 2 | `scripts/certify_kp_chain.py` | L48, L49 | no | UTC | L108 `..., "UTC")` |
| 3 | `scripts/certify_parashari_drishti.py` | L52, L53 | no | UTC | L92 `..., lat, lon, "UTC")` |
| 4 | `engine/tests/test_kp_chart.py` | L36, L37 | no | UTC | L49 `case["lat"], case["lon"], "UTC"` |
| 5 | `scripts/certify_panchanga.py` | L130, L131 | no | **12:00 UT** | L190 `swe.julday(*case["date"], 12.0, swe.GREG_CAL)` |
| 6 | `scripts/certify_trikalam.py` | L114, L115 | no | **12:00 UT** | L166 `swe.julday(*case["date"], 12.0, swe.GREG_CAL)` |
| 7 | `validate_panchanga_holdout.py` | L147, L148 | no | **12:00 UT** | L174 |
| 8 | `validate_trikalam_holdout.py` | L88, L89 | no | **12:00 UT** | L111 |
| 9 | `scripts/certify_rise_set.py` | L92, L93 | no | derived instant | rise/set solved from the date + coordinates |
| 10 | `validate_rise_set_holdout.py` | L43, L44 | no | derived instant | as above |

**Confirmed: exactly one of the ten carries `boundary_sensitive`.** The owner's
stated 1-of-11 finding is verified against the tree, with the refinement that the
denominator is now ten live surfaces.

**Case inputs.** The four time-bearing surfaces use identical inputs:
`H10_boundary_moon_a` = 2025-03-01 16:21:00, `H11_boundary_moon_b` =
2025-03-02 11:38:00, latitude 28.6667, longitude 77.2167, timezone UTC. The six
date-only surfaces carry the dates `(2025, 3, 1)` and `(2025, 3, 2)` and the same
coordinates, with **no time field**. No instant is manufactured for them in this
paper: four of the six evaluate at **12:00 UT by their own implementation**, and
the two rise/set surfaces derive their instant by solving for the event.

**Artifact reach.** Only `certification/current_engine_certification.json` contains
either identifier. `KP_CHAIN_V1`, `PANCHANGA_V1`, `RISE_SET_V1`, `TRIKALAM_V1` and
`PARASHARI_DRISHTI_V1` do not emit the case ids at all, so they publish no claim -
boundary or otherwise - attached to these names.

**Boundary prose.** `certify_panchanga.py` and `certify_trikalam.py` contain
substantial "boundary" prose (20 and 16 occurrences). Inspected in the six lines
surrounding each case entry, **none of it attaches to H10/H11**: it concerns those
surfaces' own quantities - tithi/yoga/karana transitions and the sunrise weekday
rollover. A boundary claim must not be inferred from co-occurrence in a file.

---

## 2. What `boundary_sensitive` actually does

`scripts/certify_current_engine.py` L345:

```python
if case.get("boundary_sensitive"):
    exact = exact_nakshatra_reference(ref["planets"]["Moon"])
    entry["moon_boundary_check"] = {
        "engine": got["moon_nakshatra"],
        "exact_reference_on_swetest_moon": exact,
        "agrees": (... nakshatra and nakshatra_pada both equal ...),
    }
    if not entry["moon_boundary_check"]["agrees"]:
        failures.append(...)
```

**The flag is a check selector, not a proximity assertion.** It does not claim the
Moon is near a nakshatra edge. It selects an additional cross-implementation
check: the engine's own Moon nakshatra and pada classification is compared against
an exact reference computed on **swetest's** Moon - the independent D-001
authority - and disagreement fails certification.
`engine/tests/test_current_engine_certification.py` L68 asserts exactly four such
checks (two cases x two profiles), and all four record `agrees: true` in the
committed artifact.

That check is **sound for any Moon longitude**. It verifies that two
implementations classify the same position identically. Its diagnostic power would
be greater near a cell edge, but nothing about it is falsified by the cases being
far from one. **The check is not defective.**

Corrected sidereal distances, recorded as context and not as the check's purpose:
`H10` Moon 339.791988, **6.4587 deg** from the nearest nakshatra edge; `H11` Moon
351.686403, **5.0197 deg**. Both reproduce `ADR-0072` exactly.

---

## 3. Per-surface boundary quantity, evaluated independently

No quantity is generalised across methodologies. For each surface the question is
what that surface's check could actually be made to fail by, and how much margin
the cases leave.

| Surface | Does it assert boundary sensitivity? | Quantity actually relevant | Boundary definition | Relevance | Distance | Classification |
|---|---|---|---|---|---|---|
| `certify_current_engine` | **No** - the flag selects a check | Moon nakshatra / pada classification | 27 cells of 13 deg 20 min; pada = quarter cell | A classification can only differ between implementations near a cell edge | 6.4587 / 5.0197 deg | **Ordinary case, sound check, misleading identifier** |
| `certify_kp_chain` | No | Full lordship chain for every body, ascendant and 12 cusps | sign / star / sub / sub-sub cells, Vimshottari proportions | A chain mismatch requires disagreement exceeding the distance to a cell edge | Moon sub-lord 0.9031 / 0.2420 deg; but the gate compares **275 chains**, not the Moon alone | **Ordinary case; not Moon-specific** |
| `test_kp_chart` | No | as above, in test form | as above | as above | as above | **Ordinary case** |
| `certify_parashari_drishti` | No | Graha drishti angular relationships | aspect ranges from the certified drishti tables | Unrelated to lunar cell edges | not meaningful | **No boundary quantity involved** |
| `certify_panchanga` | No | tithi / karana / yoga / nakshatra at 12:00 UT | 12 deg / 6 deg elongation, 13 deg 20 min sum, 13 deg 20 min | Element transitions are this surface's own edges | tithi and karana 1.3313 / 2.2433 deg; yoga 3.5820 / 2.9495 deg | **Ordinary case for its own quantities** |
| `validate_panchanga_holdout` | No | as above | as above | as above | as above | **Ordinary case** |
| `certify_trikalam` | No | Rahu Kalam / Yamaganda / Gulika segments | day divided into eight parts between sunrise and sunset; weekday rollover at sunrise | Segment edges and the sunrise rollover are its own edges | Delhi, ordinary mid-latitude day; no rollover stress | **Ordinary case** |
| `validate_trikalam_holdout` | No | as above | as above | as above | as above | **Ordinary case** |
| `certify_rise_set` | No | Sunrise / sunset existence and instant | the no-rise / no-set polar condition | Its genuine edge cases are `P1_svalbard_midnight_sun` and `P2_svalbard_polar_night`, which exist separately | Delhi 2025, unremarkable | **Ordinary case; real edge cases exist elsewhere in the same holdout** |
| `validate_rise_set_holdout` | No | as above | as above | as above | as above | **Ordinary case** |

### 3.1 Whether the KP sub-lord distances matter

The owner directed that the KP sub-lord distances be evaluated independently of
nakshatra proximity rather than assumed relevant. They are **not** relevant, and
the reason is quantitative rather than a matter of judgement.

`gate_b_holdout_chart_equivalence` (`scripts/certify_kp_chain.py` L100-130) fails
if any longitude diverges from the legacy kernel by more than **0.001 arcsec**, or
if any chain tuple differs. The committed artifact records
`max_longitude_delta_arcsec: 0.0` across **275 chain comparisons** over 11 cases -
exact agreement.

A chain mismatch therefore requires the two implementations to disagree by more
than the distance from the position to its cell edge. The Moon's sub-lord margins
here are 0.9031 and 0.2420 degrees, which are **3.25e6 and 8.71e5 times** the
gate's own longitude tolerance. At measured divergence of zero, the margin is not
merely large but unreachable.

The same arithmetic disposes of the nakshatra question for `certify_current_engine`:
margins of 6.4587 and 5.0197 degrees against an engine-versus-swetest agreement of
~1.6e-4 arcsec are ratios of about **1.3e8 and 1.0e8**.

**Conclusion: no surface's check is boundary-stressed by these cases, in any
quantity.** The identifiers promise a stress that the data does not deliver, and no
check is made wrong by that.

---

## 4. Append-only correction of the historical record

`ADR-0072` is **not edited**. The following correction is recorded here, per the
owner's explicit authorization, and distinguishes two things that entry conflated.

`ADR-0072` states the cases are *"reused as a 'boundary_sensitive' holdout case in
eight other certifiers/validators"*. Reconstructed from the tree:

- **True:** the case identifiers are present, and the cases reused, in additional
  holdout arrays - ten live surfaces at the time of this reconstruction.
- **Not established by the tree:** that they are reused *as `boundary_sensitive`
  holdout cases*. Exactly one surface sets that flag, and there it selects a check
  rather than asserting proximity. The remaining surfaces carry the cases as
  ordinary holdout entries, and five of the six certification artifacts examined do
  not emit the identifiers at all.

This is a correction of **characterisation**, not of any calculation. `ADR-0072`'s
own measured finding - that the cases sit 6.46 and 5.02 degrees from the nearest
nakshatra boundary - is reproduced exactly by this reconstruction and stands. Its
decision to rename the cases *within the Vimshottari oracle gate*, where the label
had been relied on for boundary coverage, also stands. What does not survive is the
implication that ten other surfaces were relying on a boundary claim.

**No calculation inconsistency is asserted or found.** Every surface examined
agrees with its own reference: `max_longitude_delta_arcsec: 0.0` for KP,
`agrees: true` on all four Tier-0 boundary checks, and PASS verdicts throughout.

---

## 5. The decision question

**Does H10/H11 represent an actual engineering or governance defect, or was the
original concern primarily a mischaracterisation of case reuse and of the meaning
of `boundary_sensitive`?**

The reconstruction supports the second reading, with one residual worth the owner's
attention.

**Not defects.** No calculation is wrong. No check is unsound. No certification
verdict is affected. No artifact overstates its evidence: the only artifact that
records anything tied to these identifiers records a classification agreement,
which is exactly what was verified. The `boundary_sensitive` flag does what its
code says, and its test asserts the right number of checks.

**The residual.** Two identifiers assert, by name, a property their data does not
have, across ten surfaces. That is a provenance and communication defect rather
than a calculation one: a reader encountering `H10_boundary_moon_a` in
`certify_rise_set.py` will reasonably infer boundary coverage that surface does not
have and does not claim. `ADR-0072` already judged this worth correcting where the
label was load-bearing. Whether it is worth correcting where it is merely
misleading is a matter for the owner, not for this paper.

**A genuinely open question, stated rather than answered.** `certify_current_engine`
is the one surface whose check would gain diagnostic power from a near-boundary
case, and it currently has none: its two `boundary_sensitive` cases are 6.46 and
5.02 degrees from an edge. Whether that gate should acquire a genuinely
near-boundary Moon case - as `ADR-0072` did for the Vimshottari gate - is a
test-design question requiring its own authorization. This paper does not propose
it, implement it, or treat its absence as a defect in what is currently certified.

---

## 6. Options, for the owner. This paper selects none.

**Option A - no defect, record and close.** Accept that the concern was a
mischaracterisation; keep every identifier and every check exactly as implemented;
record this reconstruction as the standing answer.

**Option B - documentation and provenance correction only.** Option A plus an ADR
recording the append-only correction in section 4, so a future reader of `ADR-0072`
finds the narrowing. No code, no test, no artifact touched.

**Option C - Option B plus a separately authorized test-design change.** Additionally
authorize, as its own work item, either renaming the identifiers where they mislead,
or adding a genuinely near-boundary Moon case to `certify_current_engine`'s
`boundary_sensitive` set, or both. Each would change certification evidence and
requires its own authorization, its own negative control and its own regeneration.

**Option D - another evidence-supported disposition** the owner identifies.

---

## 7. What this paper does not do

It does not decide. It renames nothing, alters no holdout datum, modifies no
certification logic, regenerates no artifact, changes no certification status, does
not edit `ADR-0072`, and does not close H10/H11. It authorizes no implementation of
any kind.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-09-15 | Created under the owner's "CEO AUTHORIZATION — PROCEED WITH DP-037 FULL LINEAGE PAPER" instruction. Full lineage reconstruction of all ten live surfaces (eleven at authorization, one retired under M-4) from their actual repository inputs, with the withdrawn harness-error finding recorded in section 0, the `boundary_sensitive` check-selector determination in section 2, per-surface boundary quantities in section 3, the quantitative disposal of the KP sub-lord question in section 3.1, and the append-only correction of `ADR-0072`'s characterisation in section 4. |
