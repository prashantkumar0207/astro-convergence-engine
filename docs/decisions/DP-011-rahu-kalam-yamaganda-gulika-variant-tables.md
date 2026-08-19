<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and recommends one. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-19 |
| Review cadence | TBD |

# DP-011. Rahu Kalam / Yamaganda / Gulika variant-table source

## 1. The question

`ADR-0055` item 2 left Rahu Kalam, Yamaganda and Gulika explicitly unauthorized: "No source was named
by the owner; per DP-009's own warning that 'each variant is a decision to record, never a silent
choice,' this entry authorizes drafting a short `DP-NNN` options paper naming candidate source tables
for [these] for separate, later owner ratification." This paper is that paper. It decides nothing;
implementation of any of the three remains unauthorized until the owner ratifies a specific source.

## 2. What is common ground, and what is not

**Common ground across traditions:** all three periods are computed by dividing the interval from
sunrise to sunset into eight equal parts ("eighth-parts" of the day), and assigning one eighth-part to
each period for each weekday. All three therefore depend on the certified `engine.astronomy.rise_set`
layer for the day's sunrise/sunset instants, exactly as `vara` already does (`ADR-0055` item 4) - this
paper does not reopen that dependency.

**What is not common ground, and is exactly the gap `DP-009` s6 flagged:**

1. **Which eighth-part each weekday maps to, for each of the three periods.** Widely-circulated
   Panchanga references and software (including popular sources such as Drik Panchang) commonly use one
   specific weekday-to-eighth-part table for each of Rahu Kalam, Yamaganda and Gulika, but this
   repository has not independently verified any specific table against a citable classical or
   documented source, and general astrological convention is not, on its own, the kind of independent
   reference this repository's certification discipline requires (`.claude/rules/validation.md`:
   "prefer an external reference... wherever one exists"; `docs/DECISION_LOG.md`'s own anti-fitting
   rules apply equally to a table adopted without a named source). **No table is asserted as fact by
   this paper** - the mechanism (eight equal day-parts, one part per weekday) is well-attested; the
   specific weekday-to-part assignment is not yet a verified, citable fact in this repository.
2. **Day-only vs. day-and-night division.** Some traditions compute Gulika (and, less commonly,
   Yamaganda) separately for daytime and night-time births, using the night interval (sunset to next
   sunrise) divided into its own eight parts, rather than only ever using the day's eighth-parts. Others
   use only the day-time table regardless of birth time. This is a second, independent variant axis, not
   merely a detail of the first.
3. **Regional/lineage variation.** Some Tamil- and Telugu-tradition sources report different
   weekday-to-part tables for Yamaganda and Gulika from the more commonly circulated one; this
   repository has not surveyed which lineage(s) it intends to support.

## 3. Why this cannot be resolved by implementation convenience

The three periods are pure lookup tables over an already-certified astronomical primitive (rise/set) -
there is no dense-sweep or ULP-boundary question here the way there is for tithi/yoga/karana. The
entire certification risk is **which table**, not **how to compute given a table**. Silently picking
the first source found (as `certify_rise_set.py`'s own predecessor mistake with an unverified `swetest`
call illustrates, and as this repository's own `PANCHANGA_V1` Gate F checkpoint just demonstrated for a
structurally identical "which external reference" question) is exactly the failure mode `ADR-0055` item
2 was written to prevent.

## 4. Options

**Option A. Adopt the single most commonly circulated weekday-to-eighth-part table (day-only), for all
three periods, sourced and cited explicitly before implementation.** Simplest to implement and certify -
one static table per period, no profile branching. Its cost is that it silently favors one lineage over
others some users may expect, and it does not address the day/night variant axis (item 2 above) at all;
night-time Gulika would be either unimplemented or (worse) silently computed with the day table, which
would be a real defect, not a convention choice, if presented as if it were general.

**Option B. Adopt whatever table `PyJHora`'s `jhora.panchanga.drik` module already implements for these
three periods, reusing it as this repository's designated Panchanga oracle already does for tithi/yoga/
karana (`ADR-0059`).** Consistency argument: this repository already treats PyJHora as its external
oracle of record for Panchanga classification, so reusing its rahu-kalam/yamaganda/gulika convention
avoids introducing a second, unrelated source of truth. Its cost is that **this repository has not yet
inspected PyJHora's actual source for these three functions in this session** (PyJHora is not installed
on this Windows host; the isolated exploration venv used for `ADR-0059` inspected only
`tithi`/`yogam`/`karana`) - adopting this option is not yet backed by a verified citation and would
need that inspection done first, in the CI oracle environment or an equivalent isolated venv, before
ratification, not after.

**Option C. Support multiple named variant tables, selectable via `CalculationProfile`, mirroring how
ayanamsha and node policy are already handled.** Most flexible and most honest about the fact that this
is a genuine, named tradition-dependent variant, not a single correct answer - matches this
repository's own established pattern for exactly this class of problem. Its cost is materially higher:
each named variant needs its own cited source and its own certification evidence (dense sweep is not
needed, but a protected holdout and an independent cross-check against that variant's own source table
is), multiplying the certification burden by the number of variants supported, for a capability with
comparatively low downstream demand until Muhurta (Phase 10) actually needs it.

**Option D. Defer Rahu Kalam/Yamaganda/Gulika entirely until closer to Muhurta phase entry.**
`Q8_CLOSURE_MATRIX.md` s4 lists these under FOUNDATION's implementation scope, but `Q8_CLOSURE_MATRIX.md`
s10 (MUHURTA) is the first phase that actually consumes them ("Tara Bala and Chandra Bala specified" as
a MUHURTA prerequisite; Rahu Kalam/Yamaganda/Gulika are not named as consumed by JATAKA or EVIDENCE).
Costs nothing while no implementation is authorized regardless, and avoids picking a table under time
pressure; risk is the same as `DP-009`'s own Option D risk - the decision eventually has to be made by
someone, and deferring only delays who.

## 5. Recommendation

**Option C (named, profile-selectable variant tables), with Option B's PyJHora-convention inspection
done first as the initial variant to verify and register**, and Option A's single-table approach
explicitly rejected as a starting point. Confidence: medium.

The reasoning: this repository has already established, twice (ayanamsha, node policy), that a
tradition-dependent astronomical/astrological convention gets a named field on `CalculationProfile`
rather than a silently-picked default - Option A would be the first place this repository quietly
abandoned that pattern for convenience, and `ADR-0055` item 2 was written specifically to prevent that.
Starting the first registered variant from PyJHora's own convention (Option B) is efficient because the
verification work (reading `jhora.panchanga.drik`'s source in an isolated venv, exactly as `ADR-0059`
already did for tithi/yoga/karana) is a small, bounded task using infrastructure this repository already
has, and it keeps this repository's designated oracle internally consistent with itself. Additional
named variants (Option C's generality) can be added later, each on its own citation and its own
ratification, without re-opening this decision.

I would accept Option D if the owner judges Muhurta is far enough off that this effort is better spent
elsewhere first; it is a legitimate sequencing call the analysis above does not by itself settle.

## 6. What the decision must also settle, whichever option is chosen

Which specific source(s) are cited for the weekday-to-eighth-part table(s), by name and by variant if
more than one is ratified. Whether Gulika (and/or Yamaganda) needs a separate night-time division, and
if so, which source governs the night table. Whether these three periods produce a structured
NO_RESULT-style output when rise/set itself returns `NO_RISE`/`NO_SET` (the same circumpolar edge case
`RISE_SET_V1`/`PANCHANGA_V1`'s `vara` already had to handle), consistent with the existing convention
rather than inventing a new one. Whether implementation is authorized to begin immediately on
ratification, or requires its own separate FOUNDATION per-capability CEO checkpoint on completion
(`Q8_CLOSURE_MATRIX.md` s4's own "per-capability" language suggests the latter, consistent with how
Panchanga classification and rise/set each received their own checkpoint).

## 7. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-19 | Drafted per `ADR-0055` item 2's authorization. Presents options; decides nothing. |
