<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and recommends one. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-11 |
| Review cadence | TBD |

# DP-009. Tier classification for panchanga and astronomical rise/set

## 1. The question

ADR-0020 D2 decided that panchanga and rise/set are **Tier-0 foundational capabilities requiring
independent certification before any dependent production module relies on them**. That substance is
settled and is not reopened here.

What remains open is whether the two carry the **same tier classification**, given that they are
different kinds of computation. ADR-0020 recorded the nuance and deliberately left it undecided.

**This paper decides nothing**, and it must not be resolved by implementation convenience.

## 2. The distinction, stated explicitly as required

**Rise and set is astronomical calculation.** It computes an event instant from ephemeris positions
plus horizon geometry. It is not one calculation but a **family parameterised by declared
conventions**, and this is the crux of the argument. Every one of the following changes the answer,
and traditions differ on each: whether the reference is the disc centre or the upper limb; the
refraction model and the standard altitude adopted, commonly around 34 arcminutes but not
universally; whether the observer's elevation is accounted for; and how the calculation behaves at
latitudes where the body does not rise or set at all. These are conventions of the same class as
ayanamsha and node policy, which the project already handles through explicit calculation profiles,
and they belong in the same mechanism.

**Panchanga is deterministic classification over astronomical outputs.** Tithi is a function of the
Sun-Moon elongation. Nakshatra is a function of Moon longitude. Yoga is a function of their sum.
Karana is a function of half a tithi. Each is exact-arithmetic-representable, each has boundaries and
therefore a boundary convention, and each is structurally a **varga-shaped problem**: a frozen rule
over a continuous input, certifiable by dense sweep, ULP battery and independent reference.

## 3. The fact that spoils the clean split

**Vara is not classification over longitudes.** The Jyotisha weekday runs sunrise to sunrise, so vara
depends on rise/set and inherits every convention and every high-latitude failure mode listed above.

Panchanga is therefore four elements of pure classification plus one element with an astronomical
dependency. Any option that puts panchanga wholly on one side of the line is inaccurate about vara.

A second consequence follows and is worth stating: Rahu Kalam, Yamaganda and Gulika are eighth-part
divisions of the day and night, so they depend on rise/set too, and they additionally carry variant
assignment tables that differ across traditions. Each variant is a decision to record, never a silent
choice, exactly as varga variants are.

## 4. Options

**Option A. Both Tier-0, one classification.** Simple, matches ADR-0020 D2's wording most directly, and
correctly signals that both must be certified before dependants rely on them. Its cost is precision:
it groups a convention-parameterised astronomical calculation with deterministic table classification,
and the project's own charter principle separates astronomy from astrological rule interpretation.
Grouping them invites the assumption that one certification methodology fits both, which it does not:
rise/set needs an external astronomical reference and profile declarations, panchanga needs dense
sweeps and ULP batteries.

**Option B. Rise/set Tier-0, panchanga Tier-1.** Most technically accurate for four of the five
panchanga elements. It places rise/set with the ephemeris kernel, where its conventions can join the
existing calculation-profile mechanism, and places panchanga with the vargas, where its certification
template already exists and is proven. Its cost is that vara straddles the boundary and needs an
explicit note, and that two tiers must both be certified before Muhurta, so the split buys precision
rather than sequencing freedom.

**Option C. A new label, for example Tier-0b or Tier-1a.** Avoids overloading either existing tier.
Its cost is a third vocabulary term for a project that already carries two overlapping certification
vocabularies, the LOCKED and CERTIFIED language and the charter's C0 to C5 levels, with the mapping
between them still unresolved. Adding a third before reconciling the two would compound an existing
problem.

**Option D. Defer until the C0 to C5 taxonomy lands.** The taxonomy work is already planned as ADR-0017
and will have to state what each tier means anyway. Deferring costs nothing while no implementation is
authorised, and it avoids deciding twice. Its risk is that the first implementer needs an answer, and
the answer then gets chosen by whoever is closest to the code.

## 5. Recommendation

**Option B, with vara explicitly noted as straddling the boundary.** Confidence: medium.

The reason is methodological rather than taxonomic. The two need **different certification
methodologies**, and a tier classification that hides that difference will produce a certification
plan that is wrong for one of them. Rise/set needs declared conventions in a calculation profile and
an independent astronomical reference. Panchanga needs the varga template: frozen rule, second
transcription, dense sweep, ULP battery, external oracle, independent validator. Putting them in
separate tiers makes that difference structural rather than something a reader has to notice.

I would accept Option D readily if the taxonomy work is imminent, since deciding once is better than
deciding twice, and this paper's analysis is what the taxonomy work would need regardless.

## 6. What the decision must also settle, whichever option is chosen

The rise/set convention set to be declared: disc centre or upper limb, refraction model and standard
altitude, observer elevation, and behaviour where the body does not rise or set. Whether these become
fields on the existing `CalculationProfile` or a separate profile type. Which tithi, yoga and karana
boundary convention applies, and whether it is the engine-wide promote-up convention or the KP-style
exact interval convention, since the repository already carries both. Which Rahu Kalam, Yamaganda and
Gulika variant tables are certified. And whether vara is computed inside panchanga or consumed from
the rise/set layer.

## 7. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Drafted on CEO direction. Presents options; decides nothing. |
