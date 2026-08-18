"""
Sunrise and sunset (ADR-0054, FOUNDATION rise/set capability).

Owner-ratified conventions (ADR-0054), all binding, none inferred:

  - Upper-limb solar disc. Swiss Ephemeris's default `rsmi` behaviour
    (no `SE_BIT_DISC_CENTER`, no `SE_BIT_DISC_BOTTOM`) already is
    upper-limb; no extra flag is needed to obtain it.
  - Standard atmospheric refraction, the classical -50' standard
    altitude (34' refraction + 16' solar semi-diameter). Swiss
    Ephemeris's default `rsmi` behaviour (no `SE_BIT_NO_REFRACTION`)
    already applies standard refraction; combined with the upper-limb
    default above, this reproduces -50' without any extra flag.
  - Observer elevation is fully accounted for, both effects:
      (a) atmospheric pressure/refraction - Swiss Ephemeris derives
          standard pressure from the observer's altitude when
          `atpress`/`attemp` are 0.0 (its own documented default);
      (b) geometric dip of the horizon - NOT automatic in plain
          `swe.rise_trans`, verified empirically before this module
          was written (a 4000m-elevation case computed with (a) alone
          gave a LATER sunrise than sea level, the wrong direction).
          `swe.rise_trans_true_hor`'s explicit `horhgt` parameter is
          used instead, set to the standard nautical/astronomical dip
          approximation (Meeus, "Astronomical Algorithms" ch. 15;
          equivalent to arccos(R_earth/(R_earth+h)) for small h/R):
          dip_degrees = 0.0293 * sqrt(elevation_m). Re-verified after
          the fix: 4000m then rises ~487 seconds EARLIER than sea
          level, the physically correct direction.
  - A day on which the event does not occur (circumpolar) returns a
    structured NO_RISE / NO_SET result: never an exception, never a
    silently-wrong timestamp.

Only these ratified values are implemented. A `CalculationProfile`
carrying any other `rise_set_disc_reference` / `rise_set_refraction`
is rejected rather than silently guessed at.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum

import swisseph as swe

from engine.astronomy.ephemeris import calc_ut_checked, initialize_ephemeris
from engine.astronomy.profile import (
    RISE_SET_DISC_UPPER_LIMB,
    RISE_SET_REFRACTION_STANDARD,
    CalculationProfile,
    DEFAULT_PROFILE,
)

#: Nautical/astronomical dip-of-horizon coefficient (degrees per
#: sqrt(metre)). Meeus, "Astronomical Algorithms" ch. 15.
_DIP_COEFFICIENT_DEG_PER_SQRT_M = 0.0293


class RiseSetStatus(str, Enum):
    """Outcome of a rise/set query."""

    OK = "ok"
    NO_RISE = "no_rise"
    NO_SET = "no_set"


class UnsupportedRiseSetConventionError(ValueError):
    """
    Raised when a `CalculationProfile` declares a rise/set convention
    other than the one ADR-0054 ratified. Never silently substituted.
    """


@dataclass(frozen=True)
class RiseSetResult:
    """
    Outcome of a `sunrise`/`sunset` query.

    Attributes
    ----------
    status
        `OK` with `julian_day_ut` populated, or `NO_RISE`/`NO_SET`
        with `julian_day_ut` `None` (circumpolar day).
    julian_day_ut
        Julian day (Universal Time) of the event, or `None`.
    event
        `"rise"` or `"set"`, the query that produced this result.
    """

    status: RiseSetStatus
    julian_day_ut: float | None
    event: str


def horizon_dip_degrees(elevation_m: float) -> float:
    """
    Geometric dip of the horizon seen from `elevation_m` above it.

    Zero for sea level or below (a negative elevation does not raise
    the horizon; the standard formula is undefined there and this
    module does not extrapolate it).
    """

    if elevation_m <= 0.0:
        return 0.0
    return _DIP_COEFFICIENT_DEG_PER_SQRT_M * math.sqrt(elevation_m)


def _check_profile_convention(profile: CalculationProfile) -> None:
    if profile.rise_set_disc_reference != RISE_SET_DISC_UPPER_LIMB:
        raise UnsupportedRiseSetConventionError(
            "rise_set_disc_reference "
            f"{profile.rise_set_disc_reference!r} is not implemented; "
            f"only {RISE_SET_DISC_UPPER_LIMB!r} is ratified (ADR-0054)"
        )
    if profile.rise_set_refraction != RISE_SET_REFRACTION_STANDARD:
        raise UnsupportedRiseSetConventionError(
            f"rise_set_refraction {profile.rise_set_refraction!r} is "
            f"not implemented; only {RISE_SET_REFRACTION_STANDARD!r} "
            "is ratified (ADR-0054)"
        )


def _rise_or_set(
    event: str,
    julian_day_ut: float,
    latitude: float,
    longitude: float,
    elevation_m: float = 0.0,
    profile: CalculationProfile = DEFAULT_PROFILE,
    strict: bool = True,
) -> RiseSetResult:
    if event not in ("rise", "set"):
        raise ValueError(f"event must be 'rise' or 'set', got {event!r}")
    if not math.isfinite(elevation_m):
        raise ValueError(f"elevation_m must be finite, got {elevation_m}")
    if not (-90.0 <= latitude <= 90.0):
        raise ValueError(f"latitude out of range: {latitude}")
    if not (-180.0 <= longitude <= 180.0):
        raise ValueError(f"longitude out of range: {longitude}")

    _check_profile_convention(profile)

    initialize_ephemeris()

    if strict:
        # Reuses the existing, already-certified Tier-0 fallback guard
        # rather than re-deriving BUNDLED_RANGE_YEARS here: calc_ut_checked
        # raises EphemerisFallbackError itself when Swiss Ephemeris data
        # was requested but the Moshier fallback was actually used.
        # `swe.rise_trans_true_hor` exposes no equivalent flag of its
        # own, so this is the only way to detect the same silent
        # degradation for a rise/set query.
        calc_ut_checked(julian_day_ut, swe.SUN, swe.FLG_SWIEPH, strict=True)

    rsmi = swe.CALC_RISE if event == "rise" else swe.CALC_SET
    horhgt = -horizon_dip_degrees(elevation_m)
    geopos = (longitude, latitude, elevation_m)

    res, tret = swe.rise_trans_true_hor(
        julian_day_ut, swe.SUN, rsmi, geopos, 0.0, 0.0, horhgt, swe.FLG_SWIEPH,
    )

    if res == -2:
        status = RiseSetStatus.NO_RISE if event == "rise" else RiseSetStatus.NO_SET
        return RiseSetResult(status=status, julian_day_ut=None, event=event)
    if res != 0:
        raise RuntimeError(
            f"unexpected swe.rise_trans_true_hor result code {res} for "
            f"event={event!r} jd={julian_day_ut} lat={latitude} lon={longitude}"
        )

    return RiseSetResult(status=RiseSetStatus.OK, julian_day_ut=tret[0], event=event)


def sunrise(
    julian_day_ut: float,
    latitude: float,
    longitude: float,
    elevation_m: float = 0.0,
    profile: CalculationProfile = DEFAULT_PROFILE,
    strict: bool = True,
) -> RiseSetResult:
    """
    Sunrise at or after `julian_day_ut` (Universal Time), under the
    ADR-0054 conventions. Returns `NO_RISE` rather than raising when
    the sun does not rise that day (circumpolar).
    """

    return _rise_or_set(
        "rise", julian_day_ut, latitude, longitude, elevation_m, profile, strict
    )


def sunset(
    julian_day_ut: float,
    latitude: float,
    longitude: float,
    elevation_m: float = 0.0,
    profile: CalculationProfile = DEFAULT_PROFILE,
    strict: bool = True,
) -> RiseSetResult:
    """
    Sunset at or after `julian_day_ut` (Universal Time), under the
    ADR-0054 conventions. Returns `NO_SET` rather than raising when
    the sun does not set that day (circumpolar).
    """

    return _rise_or_set(
        "set", julian_day_ut, latitude, longitude, elevation_m, profile, strict
    )
