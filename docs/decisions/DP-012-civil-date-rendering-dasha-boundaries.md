<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and recommends one. DECIDES NOTHING. Requires owner approval. |
| Version | 1.2.0 |
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

1. **DST fold/gap ambiguity - empirically checked and found NOT to apply to this direction.** An
   earlier draft of this paper (v1.0.0) assumed dasha-boundary rendering would face the same fold/gap
   ambiguity `BirthData`/`time_service.py` resolve for the birth instant. Direct testing (`zoneinfo`,
   `America/New_York`, swept minute-by-minute across both the 2024-03-10 spring-forward gap and the
   2024-11-03 fall-back fold) shows this does **not** apply: fold/gap ambiguity is a property of
   *interpreting a naive local wall-clock reading as an instant* (which UTC instant did the human mean?)
   - exactly `BirthData`'s own situation, which is why it needs `fold` as an input and why
   `engine.core.validation` rejects gap-landing birth input. Dasha-boundary rendering runs in the
   **opposite** direction: `start_jd`/`end_jd` are already exact, unambiguous UTC instants (computed,
   never human-entered), and `datetime.astimezone(ZoneInfo(tz))` on an already-aware UTC datetime is
   **fully deterministic in this direction** - every UTC instant maps to exactly one local datetime, the
   spring-forward gap is simply never an output (local time jumps 01:59->03:00 with no instant landing
   in between), and the fall-back fold is resolved automatically and correctly by `astimezone()` itself
   (confirmed: instants an hour apart in wall-clock-adjacent UTC minutes are correctly tagged `fold=0`
   then `fold=1` without any caller-supplied disambiguation). **No convention decision is needed for this
   sub-question** - it is resolved by the language/library's own well-defined semantics, not a policy
   choice this repository must record.
2. **`tzdata` coverage at century-scale spans - empirically checked, not assumed.** Dasha periods can
   run to 120 years (a full Vimshottari cycle). Probing this repository's own installed `tzdata` against
   `RISE_SET_V1`'s own H1-H5 holdout dates confirms `zoneinfo` resolves every one of them, but the
   *meaning* of the result changes silently at the pre-standardization boundary: `Europe/London` on
   1823-04-17 (H1) resolves to a `-00:01:15` offset - not a rounded zone offset, but the great city's
   **Local Mean Time** (solar time at that exact longitude), because standardized civil time zones did
   not exist there yet; `Asia/Kolkata` on 1979-11-11 (H4, well after standardization) resolves to the
   expected `+05:30`. Both are genuine, deliberately-encoded `tzdata` answers, not silent approximation -
   but "LMT at the birth longitude" and "the modern civil zone's standard offset" are two different KINDS
   of answer, and a rendered date that switches between them at an unstated historical boundary, with no
   flag distinguishing which kind produced it, would be exactly the "silently-wrong timestamp"
   `RISE_SET_V1`/`ADR-0054` already refuses to produce for sunrise/sunset. `RISE_SET_V1`'s own holdout
   already spans 1823-2350 for exactly this class of reason; a dasha boundary for a chart born in 1823 or
   projected to 2350 is not a hypothetical edge
   case in this repository, it is already inside the certified holdout's own range.
3. **Rendering granularity.** Whether a rendered dasha boundary needs full local time-of-day precision,
   or only a civil calendar date, and what happens to the tie-breaking convention if two representations
   are needed for different consumers (e.g. a report line vs. a machine-readable field).

## 3. Options

**Option A. Reuse `BirthData.timezone` identity via `zoneinfo`, `astimezone()` directly on the already-
unambiguous UTC instant, with the rendered result explicitly labelled `civil_time_basis: "LMT" |
"standardized_zone"` per s2 item 2's finding.** Directly extends `time_service.py`'s already-working
mechanism with minimal new surface area - s2 item 1's finding removes what looked like the largest open
sub-question (fold/gap handling turns out to need no policy at all, only correct use of `astimezone()`).
Its remaining, genuine cost is solely the LMT-vs-standardized-zone labelling s2 item 2 identifies, plus
the ordinary implementation/certification effort any new FOUNDATION capability carries.

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

**Option A, with the LMT-vs-standardized-zone labelling explicitly recorded as its one remaining
sub-decision** (not left implicit), confidence: **high** on the mechanism (directly extends
already-working, audit-remediated infrastructure, and s2 item 1's empirical finding removes the
fold/gap sub-question entirely - it was never a real choice, only a misapplied analogy to
`BirthData`'s different, opposite-direction problem), medium-high on the labelling sub-decision (a real
but narrow choice: which field name/values to use, not whether the distinction exists - s2 item 2
already establishes that empirically).

I would accept Option C readily if the owner judges no near-term FOUNDATION or later-phase work actually
consumes rendered dasha boundaries yet - the same "defer costs nothing while unauthorized" reasoning
`DP-009`'s own Option D used, and Option A's analysis above is what that later decision would need
regardless, so nothing is lost by waiting.

## 5. What the decision must also settle, whichever option is chosen

Whether a rendered boundary in the empirically-confirmed LMT-era range carries an explicit marker (e.g.
a `civil_time_basis: "LMT" | "standardized_zone"` field, or a specific alternative name/values) rather
than presenting an LMT-derived answer as if it were an ordinary standardized-zone civil time - the s2
item 2 probe confirms both kinds of answer are real, `zoneinfo`-encoded outputs, not something to
silently paper over. (Fold/gap handling, this paper's v1.0.0 draft's other named sub-question, is
resolved by s2 item 1's finding and needs no further decision.) Rendering granularity (date only vs.
date-and-time) and whether both are needed for different consumers. Whether implementation is authorized
to begin immediately on ratification, or requires its own FOUNDATION per-capability CEO checkpoint on
completion, consistent with how Panchanga, rise/set, and `TRIKALAM_V1` each received one.

## 6. Change history

| Version | Date | Change |
|---|---|---|
| 1.2.0 | 2026-08-20 | Decision-readiness audit: empirically tested (`zoneinfo`, `America/New_York`, both 2024 DST transitions) whether fold/gap ambiguity actually applies to UTC-instant-to-local rendering (the direction dasha-boundary rendering needs) - confirmed it does NOT: `astimezone()` on an already-unambiguous UTC instant is fully deterministic, no policy decision needed. Removed this sub-question from s5 and lowered Option A's cost/raised its confidence accordingly. Research only; still presents options (now two genuine sub-decisions instead of three) and decides nothing. |
| 1.1.0 | 2026-08-20 | Strengthened s2 item 2 and s5 with an empirical `zoneinfo`/`tzdata` probe against `RISE_SET_V1`'s own holdout dates: confirmed pre-standardization instants (e.g. `Europe/London` 1823) resolve to genuine Local Mean Time, not an approximation - a real, labelled-vs-unlabelled distinction the ratified option must address. Research only; still presents options and decides nothing. |
| 1.0.0 | 2026-08-20 | Drafted per the owner's "if a decision paper is required before implementation, draft that decision paper and register it" instruction. Presents options; decides nothing. |
