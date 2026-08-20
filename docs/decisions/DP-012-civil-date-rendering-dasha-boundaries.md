<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and recommends one. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-20 |
| Review cadence | TBD |

# DP-012. Civil-date rendering methodology for dasha boundaries

## 1. The question

`docs/Q8_CLOSURE_MATRIX.md` s4 lists "civil-date rendering for dasha boundaries" as FOUNDATION
implementation scope, separately from the dasha calculation itself (already certified,
`VIMSHOTTARI_V1`). `engine/models/dasha.py`'s `DashaPeriod` carries `start_jd`/`end_jd` as raw Julian
Day (UT) floats only - there is no certified path from a dasha boundary instant to the civil
(year-month-day, local time) date a person would actually be shown. This paper presents that
methodology's genuine open questions. It decides nothing.

## 2. What already exists, and what is missing

`engine/services/time_service.py` (remediating audit finding F-11) already converts `BirthData`'s own
local civil birth time to UTC via `zoneinfo`/`tzdata`, correctly handling DST and historical UTC-offset
changes, with ambiguous local times (DST fall-back) disambiguated by `BirthData.fold` (PEP 495) and
nonexistent local times (DST gap) rejected by `engine.core.validation` before that service runs. This is
the **reverse** direction of what dasha-boundary rendering needs: convert an arbitrary UT instant,
potentially decades after birth, back into a civil local date/time using the birth location's IANA
timezone identity (`BirthData.timezone`, e.g. `"Asia/Kolkata"`) - `zoneinfo` supports this directly
(`datetime.astimezone(ZoneInfo(tz))`), and reusing the birth location's timezone *identity* rather than
its instantaneous UTC offset is the only way to correctly follow that location's own historical
DST/offset rule changes over a dasha's multi-decade span, exactly as `time_service.py` already does for
the birth instant itself.

**What time_service.py's existing mechanism does not solve, because it only ever runs once, at the
birth instant, on user-validated input:**

1. **DST ambiguity/gaps at an arbitrary, computed later instant.** `BirthData.fold` disambiguates only
   the birth instant; a dasha boundary's `start_jd`/`end_jd` is a *derived* instant that can itself land
   inside a DST fall-back (ambiguous, two valid local times) or DST gap (no valid local time) window at
   the birth location, with no user-supplied `fold` to resolve it and no upstream validation step that
   could reject a derived instant the way `engine.core.validation` rejects invalid birth input.
2. **`tzdata` coverage at century-scale spans.** Dasha periods can run to 120 years (a full Vimshottari
   cycle); IANA timezone-rule data is reliably precise only from roughly the late 19th/early 20th century
   onward for most zones, and is explicitly approximate (`LMT`, Local Mean Time, or a fixed early
   estimate) further back. `RISE_SET_V1`'s own holdout already spans 1823-2350 for exactly this class of
   reason; a dasha boundary for a chart born in 1823 or projected to 2350 is not a hypothetical edge
   case in this repository, it is already inside the certified holdout's own range.
3. **Rendering granularity.** Whether a rendered dasha boundary needs full local time-of-day precision,
   or only a civil calendar date, and what happens to the tie-breaking convention if two representations
   are needed for different consumers (e.g. a report line vs. a machine-readable field).

## 3. Options

**Option A. Reuse `BirthData.timezone` identity via `zoneinfo`, `astimezone()`, fold resolved by a fixed,
declared convention (e.g. always the earlier of the two ambiguous instants), gaps reported as a
structured indeterminate result rather than silently shifted.** Directly extends `time_service.py`'s
already-working mechanism with the smallest new surface area. Mirrors this repository's established
"structured NO_RISE/NO_SET, never a silently-wrong timestamp" discipline (`ADR-0054`) for the DST-gap
case, and mirrors `ADR-0055`'s "engine-wide convention, not a silent per-instance choice" for the
fold-ambiguity case. Its cost: a declared fold convention is itself a choice affecting the rendered date
on the (rare) days it matters, and needs its own citation/justification the way every other convention
in this repository does.

**Option B. Render in a fixed reference timezone (e.g. UTC) instead of the birth location's local
civil time, leaving local-time rendering to a future presentation layer.** Avoids the ambiguity/gap
questions entirely for this work package - UTC has no DST. Its cost is that "civil date" for an
astrological report conventionally means the *subject's* local calendar date, not UTC's; deferring this
to a later "presentation layer" risks the same problem DP-009 warned against for panchanga - the eventual
implementer picks a convention under time pressure, silently, unless this paper's own analysis is
inherited by whichever later work package does the local-time conversion.

**Option C. Defer civil-date rendering entirely until a consuming feature (a report, Muhurta, or
similar) actually needs it, and let that feature's own decision paper settle the question in the context
of its actual requirements.** Costs nothing while no such feature exists yet, and `docs/Q8_CLOSURE_MATRIX.md`
s4 lists this as FOUNDATION scope but does not by itself make it FOUNDATION-exit-blocking the way H-01/
H-02 explicitly are (s4's exit-criteria row names H-01 and H-02 specifically as needing resolution or
deferral; it does not separately name civil-date rendering). Risk: FOUNDATION's own implementation-scope
list still names it, so treating it as silently out-of-scope without a recorded reason would itself be
the kind of silent narrowing `.claude/rules/certification.md` and `docs/PROJECT_CONSTITUTION.md` s3.2
warn against.

## 4. Recommendation

**Option A, with the fold convention and the DST-gap/pre-tzdata-coverage handling each explicitly
recorded as their own sub-decisions** (not left implicit), confidence: medium-high on the mechanism
(directly extends already-working, audit-remediated infrastructure), medium on the specific fold/gap
conventions (genuinely arbitrary choices, not derivable from first principles, so any reasonable choice
is defensible as long as it is recorded and applied uniformly).

I would accept Option C readily if the owner judges no near-term FOUNDATION or later-phase work actually
consumes rendered dasha boundaries yet - the same "defer costs nothing while unauthorized" reasoning
`DP-009`'s own Option D used, and Option A's analysis above is what that later decision would need
regardless, so nothing is lost by waiting.

## 5. What the decision must also settle, whichever option is chosen

The exact fold-ambiguity convention (earlier instant, later instant, or report both). Whether a DST-gap
landing produces a structured indeterminate result (mirroring `RiseSetStatus`/`TrikalamStatus`) or some
other explicit, non-silent handling. Whether pre-tzdata-reliable-coverage instants (roughly pre-1900,
zone-dependent) get a documented, honest scope limitation (mirroring `panchanga.vara`'s own "UT calendar
date of the anchoring sunrise, not necessarily the observer's local civil date" disclosed limitation)
rather than a silently-approximate `LMT`-based answer presented as exact. Rendering granularity (date
only vs. date-and-time) and whether both are needed for different consumers. Whether implementation is
authorized to begin immediately on ratification, or requires its own FOUNDATION per-capability CEO
checkpoint on completion, consistent with how Panchanga, rise/set, and `TRIKALAM_V1` each received one.

## 6. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-20 | Drafted per the owner's "if a decision paper is required before implementation, draft that decision paper and register it" instruction. Presents options; decides nothing. |
