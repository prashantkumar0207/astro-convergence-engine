"""
Panchanga classification: tithi, nakshatra, yoga, karana, vara (ADR-0055).

Scope (ADR-0055 item 3): classification of the five panchanga elements at
a given instant, reusing already-certified primitives. Element start/end
transition timing (when today's tithi ends, etc.) needs new certified
event-finding infrastructure and is explicitly deferred to a later
FOUNDATION checkpoint - it is NOT computed here.

Rahu Kalam, Yamaganda and Gulika are explicitly NOT computed here. Their
weekday-segment assignment tables genuinely vary by tradition (DP-009 s3),
and no source table is ratified yet (ADR-0055 item 2); implementing them
without one would be exactly the "silent choice" DP-009 warns against.

Boundary convention (ADR-0055 item 1): the existing engine-wide 1e-10
promote-up, `[start, end)` convention (engine.astrology.longitude_utils),
already used by nakshatra/vargas/signs, applies uniformly to tithi, yoga
and karana under both certified profiles. Unlike rise/set, there is
exactly one ratified convention here, so it is not a CalculationProfile
field with alternatives to declare and validate.

Frozen rules:
  - Tithi: floor(elongation / 12 deg) + 1, 1-30, where elongation is
    sidereal Moon longitude minus sidereal Sun longitude (mod 360). The
    ayanamsa cancels exactly in this subtraction (same mode, same
    instant), so the result is ayanamsa-independent; sidereal inputs are
    used throughout only for implementation uniformity with yoga/nakshatra.
  - Nakshatra: reuses the already Tier-0-certified
    `engine.astrology.nakshatra.nakshatra` on sidereal Moon longitude -
    not reimplemented here.
  - Yoga: floor((sidereal Sun + sidereal Moon longitude) / (360/27)) + 1,
    1-27. Unlike tithi, this genuinely depends on the profile's ayanamsa
    mode (the ayanamsa does not cancel in a sum).
  - Karana: floor(elongation / 6 deg) + 1, 1-60 (a half-tithi). Naming
    (engine.astrology.panchanga_names.karana_name) follows the universal
    classical scheme: index 1 fixed (Kimstughna), indices 2-57 cycle
    seven movable karanas eight times, indices 58-60 fixed (Shakuni,
    Chatushpada, Naga). This is not a regional variant, unlike Rahu
    Kalam/Yamaganda/Gulika.
  - Vara: the Jyotisha weekday, sunrise to sunrise (DP-009 s3), found by
    consuming the certified Tier-0 `engine.astronomy.rise_set.sunrise`
    (ADR-0055 item 4) - never reimplementing sunrise. See `vara`'s own
    docstring for a stated scope limitation on civil-date labelling.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date
from enum import Enum

import swisseph as swe

from engine.astrology.longitude_utils import division_index, normalize_longitude
from engine.astrology.nakshatra import nakshatra as _nakshatra_classify
from engine.astronomy.profile import CalculationProfile, DEFAULT_PROFILE
from engine.astronomy.rise_set import RiseSetStatus, sunrise
from engine.astronomy.sidereal_planets import sidereal_planet_position

TITHI_SPAN_DEGREES = 12.0
YOGA_SPAN_DEGREES = 360.0 / 27.0
KARANA_SPAN_DEGREES = 6.0

TITHI_COUNT = 30
YOGA_COUNT = 27
KARANA_COUNT = 60


def _sun_moon_sidereal_longitudes(
    julian_day_ut: float, profile: CalculationProfile, strict: bool
) -> tuple[float, float]:
    sun = sidereal_planet_position(
        julian_day_ut, swe.SUN, profile.ayanamsa_mode, strict
    )
    moon = sidereal_planet_position(
        julian_day_ut, swe.MOON, profile.ayanamsa_mode, strict
    )
    return sun.longitude, moon.longitude


def _elongation(sun_longitude: float, moon_longitude: float) -> float:
    return normalize_longitude(moon_longitude - sun_longitude)


def tithi_index(sun_longitude: float, moon_longitude: float) -> int:
    """Tithi number, 1-30, from sidereal Sun/Moon longitudes."""

    elongation = _elongation(sun_longitude, moon_longitude)
    return division_index(elongation, TITHI_SPAN_DEGREES, TITHI_COUNT) + 1


def yoga_index(sun_longitude: float, moon_longitude: float) -> int:
    """Yoga number, 1-27, from sidereal Sun/Moon longitudes."""

    total = normalize_longitude(sun_longitude + moon_longitude)
    return division_index(total, YOGA_SPAN_DEGREES, YOGA_COUNT) + 1


def karana_index(sun_longitude: float, moon_longitude: float) -> int:
    """Karana number, 1-60 (half-tithi), from sidereal Sun/Moon longitudes."""

    elongation = _elongation(sun_longitude, moon_longitude)
    return division_index(elongation, KARANA_SPAN_DEGREES, KARANA_COUNT) + 1


def nakshatra_index(moon_longitude: float) -> int:
    """Nakshatra number, 1-27. Thin re-export: the certified primitive
    lives in engine.astrology.nakshatra and is not reimplemented here."""

    return _nakshatra_classify(moon_longitude)


class VaraStatus(str, Enum):
    """Outcome of a `vara` query."""

    OK = "ok"
    #: No ordinary sunrise on the anchoring UT calendar day (circumpolar):
    #: the sunrise-to-sunrise vara boundary is not defined here, exactly
    #: as rise/set itself reports NO_RISE rather than guessing.
    INDETERMINATE = "indeterminate"


@dataclass(frozen=True)
class VaraResult:
    """
    Outcome of a `vara` query.

    Attributes
    ----------
    status
        `OK` with `index` populated, or `INDETERMINATE` (`index` `None`)
        when the anchoring UT day has no ordinary sunrise.
    index
        0 (Sunday / Ravivara) through 6 (Saturday / Shanivara), or `None`.
    anchor_sunrise_julian_day_ut
        The sunrise (Julian Day, UT) that opened the panchanga day the
        query instant falls in, or `None` if `status` is `INDETERMINATE`,
        or if the anchor was the *previous* UT day's sunrise (not
        separately re-queried; see `vara`'s docstring).
    """

    status: VaraStatus
    index: int | None
    anchor_sunrise_julian_day_ut: float | None


def _midnight_ut(julian_day_ut: float) -> float:
    """Julian Day (UT) of the most recent UT midnight at or before
    `julian_day_ut`. JD X.5 is midnight UT (JD X.0 is the preceding
    noon), per the Julian Day convention this project already uses
    (engine.core.julian_day)."""

    return math.floor(julian_day_ut - 0.5) + 0.5


def _weekday_index_of_civil_date(year: int, month: int, day: int) -> int:
    python_weekday = date(year, month, day).weekday()  # Monday=0 .. Sunday=6
    return (python_weekday + 1) % 7  # Sunday=0 .. Saturday=6


def vara(
    julian_day_ut: float,
    latitude: float,
    longitude: float,
    elevation_m: float = 0.0,
    profile: CalculationProfile = DEFAULT_PROFILE,
    strict: bool = True,
) -> VaraResult:
    """
    The Jyotisha weekday at `julian_day_ut`: sunrise to sunrise, per
    DP-009 s3, consuming the certified Tier-0 `rise_set.sunrise`.

    Algorithm: find the sunrise on `julian_day_ut`'s own UT calendar day.
    If `julian_day_ut` is at or after it, the vara is that UT day's
    weekday; otherwise (the instant precedes its own day's sunrise) the
    vara is the *previous* UT day's weekday - the panchanga day has not
    yet rolled over.

    Scope limitation, stated rather than silently assumed: the weekday
    label is derived from the UT calendar date of the anchoring sunrise,
    not the observer's local civil date. For most longitudes local
    sunrise and its UT calendar date agree, but for locations where local
    sunrise falls in the UT day adjacent to the local calendar date
    (broadly, longitudes far enough east that local morning is still the
    previous UT day, e.g. East Asia/Australia), the returned index can be
    one weekday off from the traditionally-expected local-date label.
    Precise per-location civil-date labelling requires threading the
    observer's IANA timezone through (the same discipline
    `engine.models.birth_data.BirthData` already requires and this
    module does not yet have wired to it) and is deferred, not silently
    assumed correct, consistent with rise/set's own "never a
    silently-wrong timestamp" discipline (ADR-0054).
    """

    midnight = _midnight_ut(julian_day_ut)
    today_sunrise = sunrise(midnight, latitude, longitude, elevation_m, profile, strict)

    if today_sunrise.status != RiseSetStatus.OK:
        return VaraResult(status=VaraStatus.INDETERMINATE, index=None, anchor_sunrise_julian_day_ut=None)

    if julian_day_ut >= today_sunrise.julian_day_ut:
        year, month, day, _hour = swe.revjul(midnight, swe.GREG_CAL)
        return VaraResult(
            status=VaraStatus.OK,
            index=_weekday_index_of_civil_date(year, month, day),
            anchor_sunrise_julian_day_ut=today_sunrise.julian_day_ut,
        )

    prior_midnight = midnight - 1.0
    year, month, day, _hour = swe.revjul(prior_midnight, swe.GREG_CAL)
    return VaraResult(
        status=VaraStatus.OK,
        index=_weekday_index_of_civil_date(year, month, day),
        anchor_sunrise_julian_day_ut=None,
    )


@dataclass(frozen=True)
class Panchanga:
    """The five panchanga elements at a given instant and location."""

    julian_day_ut: float
    sun_longitude: float
    moon_longitude: float
    tithi: int
    nakshatra: int
    yoga: int
    karana: int
    vara: VaraResult


def panchanga(
    julian_day_ut: float,
    latitude: float,
    longitude: float,
    elevation_m: float = 0.0,
    profile: CalculationProfile = DEFAULT_PROFILE,
    strict: bool = True,
) -> Panchanga:
    """Compute all five panchanga elements at one instant and location."""

    sun_longitude, moon_longitude = _sun_moon_sidereal_longitudes(
        julian_day_ut, profile, strict
    )

    return Panchanga(
        julian_day_ut=julian_day_ut,
        sun_longitude=sun_longitude,
        moon_longitude=moon_longitude,
        tithi=tithi_index(sun_longitude, moon_longitude),
        nakshatra=nakshatra_index(moon_longitude),
        yoga=yoga_index(sun_longitude, moon_longitude),
        karana=karana_index(sun_longitude, moon_longitude),
        vara=vara(julian_day_ut, latitude, longitude, elevation_m, profile, strict),
    )
