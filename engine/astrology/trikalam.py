"""
Rahu Kalam, Yamaganda, Gulika (ADR-0060): the PYJHORA_TRIKALAM_V1 variant.

Scope: DP-011 s2/ADR-0060 established that the weekday-to-eighth-part
assignment table for these three "tri kaalam" periods genuinely varies by
tradition, so it is a named, profile-selectable variant, never a silent
default - exactly the discipline already applied to ayanamsa and node
policy. Exactly one variant exists as of ADR-0060: `PYJHORA_TRIKALAM_V1`,
transcribed verbatim from PyJHora 4.8.7's `jhora.panchanga.drik.trikalam()`
(ADR-0060 Decision item 1). A second variant is explicitly NOT authorized
here (ADR-0060 Consequences) and would be additive, not a rewrite of this
one, since every table below is already keyed by variant identity.

Frozen rule (identical in kind for all three elements, this variant):
each period spans exactly 1/8 of the sunrise-to-sunset interval on the
calendar day containing the query instant, starting at
`sunrise + offset[element][weekday] * (sunset - sunrise)`, where `weekday`
is 0 (Sunday) through 6 (Saturday). Both the day's sunrise/sunset and the
weekday are consumed from already-certified primitives, never
reimplemented: `engine.astronomy.rise_set.sunrise`/`sunset` for the
window, `engine.astrology.panchanga.vara` for the weekday index (whose
own 0=Sunday..6=Saturday convention already matches PyJHora's `vaara()`
exactly, confirmed by direct comparison during ADR-0060's drafting).

Two representational differences from PyJHora, honestly recorded rather
than silently resolved (ADR-0060 Decision item 7), not defects:

  - PyJHora expresses the window in local decimal hours (subject to its
    `place.timezone` field); this module computes in Julian Day (UT),
    consistent with how `vara` already consumes `rise_set` in JD-UT
    rather than reimplementing PyJHora's local-hour pipeline. The
    transcribed rule is the *proportional offset arithmetic*, which is
    representation-independent; only the units differ.
  - PyJHora's `trikalam` computes the window from the sunrise of the
    query instant's own calendar day (via `sunrise(jd, place)` called
    directly), but selects the offset using `vaara`'s sunrise-anchored,
    possibly rolled-back weekday (`vedic_weekday`). For an instant before
    that calendar day's own sunrise, the window's calendar day and the
    weekday used to select its offset can therefore differ. This module
    mirrors that mixed behaviour exactly: `sunrise`/`sunset` are queried
    for the UT midnight of `julian_day_ut` (never rolled back), while the
    weekday comes from `panchanga.vara` (which does roll back) - it is
    not "improved" into a more internally-consistent rule PyJHora itself
    does not implement.

NOT computed here: any Muhurta-specific consumption of these periods
(search, ranking, or otherwise) - ADR-0060 does not authorize it.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from engine.astrology.panchanga import VaraStatus, _midnight_ut, vara
from engine.astronomy.profile import CalculationProfile, DEFAULT_PROFILE
from engine.astronomy.rise_set import RiseSetStatus, sunrise, sunset


class TrikalamElement(str, Enum):
    """The three periods `trikalam()` in PyJHora governs together."""

    RAHU_KALAM = "rahu_kalam"
    YAMAGANDA = "yamaganda"
    GULIKA = "gulika"


#: Variant identity (ADR-0060). A future alternate source table is a NEW
#: identity, never a silent edit to this one (DP-009: "a variant is a
#: decision to record, never a silent choice").
PYJHORA_TRIKALAM_V1 = "PYJHORA_TRIKALAM_V1"

#: Each period spans this fraction of the sunrise-to-sunset span, every
#: weekday, this variant (PyJHora 4.8.7: `end_time = start_time + 0.125 *
#: day_dur`, unconditionally).
PERIOD_FRACTION = 0.125

#: offsets[variant][element][weekday], weekday 0=Sunday..6=Saturday.
#: Transcribed verbatim from PyJHora 4.8.7 `jhora/panchanga/drik.py`,
#: `trikalam()`'s `offsets` dict (ADR-0060 Decision item 1). Frozen: do
#: not edit these numbers to "fix" or "improve" them - a changed source
#: is a new variant identity.
_OFFSETS: dict[str, dict[TrikalamElement, tuple[float, float, float, float, float, float, float]]] = {
    PYJHORA_TRIKALAM_V1: {
        TrikalamElement.RAHU_KALAM: (0.875, 0.125, 0.75, 0.5, 0.625, 0.375, 0.25),
        TrikalamElement.GULIKA: (0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0.0),
        TrikalamElement.YAMAGANDA: (0.5, 0.375, 0.25, 0.125, 0.0, 0.75, 0.625),
    }
}


class TrikalamStatus(str, Enum):
    """Outcome of a `trikalam_period` query."""

    OK = "ok"
    #: No ordinary sunrise/sunset on the query instant's UT calendar day,
    #: or the weekday itself is INDETERMINATE (circumpolar) - the window
    #: is not defined here, exactly as rise/set reports NO_RISE/NO_SET
    #: rather than guessing.
    INDETERMINATE = "indeterminate"


@dataclass(frozen=True)
class TrikalamResult:
    """
    Outcome of a `trikalam_period` query.

    Attributes
    ----------
    status
        `OK` with the remaining fields populated, or `INDETERMINATE`.
    variant
        The variant identity that produced this result (system/profile
        provenance, carried explicitly per ADR-0060 Consequences).
    element
        The requested period, or `None` if `INDETERMINATE`.
    start_julian_day_ut, end_julian_day_ut
        The period's window, Julian Day (UT), or `None`.
    weekday_index
        The weekday (0=Sunday..6=Saturday) used to select the offset, or
        `None`. Sourced from `engine.astrology.panchanga.vara`.
    """

    status: TrikalamStatus
    variant: str
    element: TrikalamElement | None
    start_julian_day_ut: float | None
    end_julian_day_ut: float | None
    weekday_index: int | None


def trikalam_period(
    element: TrikalamElement,
    julian_day_ut: float,
    latitude: float,
    longitude: float,
    elevation_m: float = 0.0,
    profile: CalculationProfile = DEFAULT_PROFILE,
    strict: bool = True,
    variant: str = PYJHORA_TRIKALAM_V1,
) -> TrikalamResult:
    """Compute `element`'s window at `julian_day_ut`'s calendar day and
    location, under `variant`'s frozen offset table."""

    if variant not in _OFFSETS:
        raise ValueError(f"unknown trikalam variant: {variant!r}")

    midnight = _midnight_ut(julian_day_ut)
    today_sunrise = sunrise(midnight, latitude, longitude, elevation_m, profile, strict)
    today_sunset = sunset(midnight, latitude, longitude, elevation_m, profile, strict)
    weekday = vara(julian_day_ut, latitude, longitude, elevation_m, profile, strict)

    if (
        today_sunrise.status != RiseSetStatus.OK
        or today_sunset.status != RiseSetStatus.OK
        or weekday.status != VaraStatus.OK
    ):
        return TrikalamResult(
            status=TrikalamStatus.INDETERMINATE,
            variant=variant,
            element=None,
            start_julian_day_ut=None,
            end_julian_day_ut=None,
            weekday_index=None,
        )

    day_duration = today_sunset.julian_day_ut - today_sunrise.julian_day_ut
    offset = _OFFSETS[variant][element][weekday.index]
    start = today_sunrise.julian_day_ut + day_duration * offset
    end = start + PERIOD_FRACTION * day_duration

    return TrikalamResult(
        status=TrikalamStatus.OK,
        variant=variant,
        element=element,
        start_julian_day_ut=start,
        end_julian_day_ut=end,
        weekday_index=weekday.index,
    )
