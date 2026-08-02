from __future__ import annotations

"""
Calculation Engine

Runs the complete deterministic astronomy calculation pipeline.
"""

from datetime import datetime

from engine.core.timezone_engine import to_utc
from engine.core.julian_day import julian_day

from engine.astronomy.astronomy_snapshot import astronomy_snapshot

from engine.models.astronomy_result import AstronomyResult


def calculate(
    birth_datetime: datetime,
    latitude: float,
    longitude: float,
) -> AstronomyResult:
    utc_datetime = to_utc(birth_datetime)

    jd = julian_day(utc_datetime)

    snapshot = astronomy_snapshot(
        julian_day=jd,
        latitude=latitude,
        longitude=longitude,
    )

    return AstronomyResult(
        snapshot=snapshot,
        aspects=(),
    )