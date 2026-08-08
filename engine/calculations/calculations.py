from __future__ import annotations

"""
Calculation Engine

Runs the complete deterministic astronomy calculation pipeline:

    BirthData
      -> validation (engine.core.validation)
      -> IANA timezone conversion (engine.services.time_service)
      -> Julian Day in UT (engine.core.julian_day)
      -> AstronomySnapshot under an explicit CalculationProfile

Remediates audit findings F-11/F-12: input is validated and the
timezone conversion uses the IANA database (DST and historical
offsets), instead of accepting unvalidated fixed offsets.
"""

from datetime import datetime

from engine.astronomy.astronomy_snapshot import astronomy_snapshot
from engine.astronomy.profile import DEFAULT_PROFILE, CalculationProfile
from engine.core.julian_day import julian_day
from engine.core.timezone_engine import to_utc
from engine.core.validation import validate_birth_data
from engine.models.astronomy_result import AstronomyResult
from engine.models.birth_data import BirthData
from engine.services.time_service import utc_datetime


def calculate(
    birth_data: BirthData,
    profile: CalculationProfile = DEFAULT_PROFILE,
) -> AstronomyResult:
    """
    Run the full validated pipeline from BirthData to an
    AstronomyResult carrying a provenance-stamped snapshot.
    """

    validate_birth_data(birth_data)

    utc = utc_datetime(birth_data)

    jd = julian_day(utc)

    snapshot = astronomy_snapshot(
        julian_day=jd,
        latitude=birth_data.latitude,
        longitude=birth_data.longitude,
        profile=profile,
    )

    return AstronomyResult(
        snapshot=snapshot,
        aspects=(),
    )


def calculate_from_datetime(
    birth_datetime: datetime,
    latitude: float,
    longitude: float,
    profile: CalculationProfile = DEFAULT_PROFILE,
) -> AstronomyResult:
    """
    Compatibility entry point for callers that already hold an
    aware datetime. CAUTION: a fixed-offset tzinfo bypasses DST
    and historical offset handling; prefer calculate(BirthData).
    """

    utc = to_utc(birth_datetime)

    jd = julian_day(utc)

    snapshot = astronomy_snapshot(
        julian_day=jd,
        latitude=latitude,
        longitude=longitude,
        profile=profile,
    )

    return AstronomyResult(
        snapshot=snapshot,
        aspects=(),
    )
