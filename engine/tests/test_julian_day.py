from datetime import datetime, timezone

from engine.core.julian_day import julian_day


def test_julian_day_returns_float():
    dt = datetime(
        1989,
        7,
        12,
        11,
        14,
        tzinfo=timezone.utc,
    )

    jd = julian_day(dt)

    assert isinstance(jd, float)