<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | PROPOSED - research and planning only. Authorises no change to certified Dasha mathematics. Pending owner ratification (docs/OPEN_QUESTIONS.md Q1). |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-11 |
| Review cadence | TBD |

# Dasha Certification Roadmap

## 1. Why Dashas need Tier-1 treatment

Dashas are the timing spine of every downstream product layer. Historical validation asks whether a
confirmed event fell in the period the system says it should have. BTR asks whether a candidate
birth time moves those periods into better agreement with confirmed events. Convergence asks whether
independent systems agree about when. All three consume dasha boundaries as if they were facts.

The sensitivity is severe and worth stating numerically, because it drives every requirement below.
Moon longitude error propagates to dasha dates by `lord_years * 365.256364 / (40/3)` days per degree:
164 days per degree for a Sun-lord seed, 192 for Ketu or Mars, and **548 days per degree for Venus**.
A one-hour ambiguity in birth time, for example an unresolved daylight-saving fold, was measured to
move the first mahadasha boundary by **101 days**.

That is the whole argument for depth. A layer this sensitive cannot rest on plausible-looking dates.

## 2. Current state, from the repository rather than from documents

Certified: Vimshottari mahadasha and antardasha, exact rational arithmetic throughout, year length
an explicit profile field rather than a hidden default, school-explicit seeding with profile
enforcement, and exact hierarchical sums where child periods close on the parent bit-exactly.

Partially certified: pratyantardasha. The oracle gate compares antardasha rows only; depth three
rests on the in-repository closed-form validator. Two documents state otherwise. Recorded as audit
finding H-04, and the audit confirmed by execution that the missing comparison would pass with zero
lord mismatches and a maximum start delta of 1.86e-09 days. The gate is absent, not failing.

Absent: every other dasha system, every depth beyond pratyantar, every alternative year convention,
and any conversion from Julian Day to civil date. That last absence is structural and matters more
than it looks: leap years, month boundaries, midnight behaviour and calendar transitions are
currently untestable because no code performs that conversion. Whatever code eventually does is
where those defects will live.

## 3. Findings that must be resolved before deeper Dasha work

From `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`, each recorded and none fixed:

**H-04** the depth-three oracle gate does not exist despite two documents citing it.
**H-05** the hermetic tier cannot detect a wrong anchor: a sign flip injecting a 4,748-day error
passes every network-free gate, because the consistency test is relative to the mutated anchor, the
boundary test is insensitive when elapsed is zero, and the independent validator never inspects a
Julian Day. No committed baseline of dasha calendar dates exists anywhere.
**H-06** no allow-list for dasha profiles, so an uncertified year convention flows through the
production entry points, and a float year length silently destroys the exactness guarantee.
**H-08** the KP boundary convention is exported into the Parashari-labelled dasha seed, so at six
float spellings of nakshatra boundaries a Parashari timeline disagrees with the engine's own
Parashari classifier about the seed nakshatra and therefore about the whole mahadasha sequence.
**M-02** the certification's two named boundary cases sit five to six degrees from any boundary, so
the oracle gate contains no near-boundary Moon case at all.

## 4. What deep certification must eventually cover

Grouped by what each group would actually falsify.

**Seeding.** Starting mahadasha lord, exact birth balance, behaviour exactly at a nakshatra boundary
and one ULP either side, and agreement between the seed classifier and the school the timeline
claims to belong to.

**Hierarchy.** Antardasha and pratyantardasha structure, deeper levels if ever claimed, exact
proportional duration arithmetic, and the invariant that child periods sum to the parent within the
declared precision. This group is currently the strongest: the sums are exact, not approximate.

**Boundaries in time.** Exact before, at, and after behaviour at every period transition, and an
explicit interval-membership convention. There is currently no membership function at all: successive
periods share a boundary value exactly, and nothing decides which period owns an instant equal to it.
The KP layer solves the same problem explicitly and is a working precedent.

**Calendar.** Leap years, month and year transitions, midnight behaviour, and the proleptic Gregorian
policy. Untestable until civil-date rendering exists, and therefore a prerequisite for it.

**Time zone.** DST transitions, ambiguous and non-existent local times, historical offsets, and
non-integer offsets. The Tier-0 pipeline handles these and is tested. The dasha layer's own tests and
certification never exercise a single one, despite the measured 101-day effect.

**Boundary sensitivity as an output.** The KP layer exposes a boundary-proximity indicator precisely
so consumers can flag critical classifications. The dasha layer, where the amplification is hundreds
of days per degree, exposes nothing equivalent. This is arguably the single most valuable addition
for BTR.

**Independence.** A mathematical reference built by a different construction, an external oracle where
one exists, and a genuinely protected holdout. The current validator is an algebraic re-derivation
rather than protected data, and no frozen expected dasha dates exist in the repository.

**Range.** The bundled ephemeris floors at 1800 and ceilings at 2399, verified to raise rather than
degrade. Charts before 1800 are impossible, which directly caps how far back historical validation
can reach and should be stated as a product constraint rather than discovered later.

## 5. Recommended sequence

1. Close H-04 by running the depth-three comparison and correcting whichever statement remains
   inaccurate. Cheapest and closes a documentation-versus-evidence defect.
2. Close H-05 with a committed frozen baseline of dasha instants, which also gives the layer its
   first genuine protected holdout.
3. Close H-06 with a certified-profile allow-list mirroring the varga pattern.
4. Decide H-08, which is an owner decision about which convention a Parashari-seeded dasha follows,
   not a builder choice.
5. Add near-boundary Moon cases to the oracle gate, closing M-02.
6. Add a boundary-proximity indicator to the timeline.
7. Specify and then implement civil-date rendering, which unlocks the entire calendar group.
8. Only then consider deeper levels or a second dasha system.

Steps 1 through 6 change no calculated value. Step 7 introduces a new surface and needs its own
specification and gates. Step 8 is new capability and needs its own ADR.

## 6. Other dasha systems

Not planned, not specified, not authorised. When one is proposed it inherits this entire framework
plus its own classical source, its own school key, and its own isolation from Vimshottari. Nothing in
the current architecture assumes Vimshottari is the only system, but nothing generalises to a second
one either, and the shared lord and year tables are already duplicated three times as a deliberate
school-isolation choice recorded as an open standards conflict.

## 7. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Created in the G1 work package from the 2026-08-11 architecture audit. |
