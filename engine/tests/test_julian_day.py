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

def test_julian_day_j2000_reference_value():
    dt = datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc)

    assert julian_day(dt) == 2451545.0


def test_julian_day_canonical_epoch_reference_value():
    dt = datetime(1989, 7, 12, 11, 14, tzinfo=timezone.utc)

    assert abs(julian_day(dt) - 2447719.9680555556) < 1e-9


def test_julian_day_uses_proleptic_gregorian_calendar():
    """
    Python datetimes are proleptic Gregorian; the engine passes
    GREG_CAL explicitly (audit finding F-10). Reference: proleptic
    Gregorian 1500-01-01 12:00 UT is JD 2268933.0 (the Julian
    calendar date of the same nominal day differs by 9 days).
    """
    dt = datetime(1500, 1, 1, 12, 0, tzinfo=timezone.utc)

    import swisseph as swe

    expected = swe.julday(1500, 1, 1, 12.0, swe.GREG_CAL)
    julian_cal = swe.julday(1500, 1, 1, 12.0, swe.JUL_CAL)

    assert julian_day(dt) == expected
    assert abs(expected - julian_cal) == 9.0
