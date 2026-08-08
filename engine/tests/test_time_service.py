"""
Time service tests (audit finding F-11): the IANA-database
conversion is now the live path, and must handle DST transitions,
ambiguous times via fold, and historical offset changes.
"""

from datetime import timedelta, timezone

from engine.models.birth_data import BirthData
from engine.services.time_service import local_datetime, utc_datetime


def make(**overrides) -> BirthData:
    base = dict(
        year=1989,
        month=7,
        day=12,
        hour=16,
        minute=44,
        second=0.0,
        latitude=25.5941,
        longitude=85.1376,
        timezone="Asia/Kolkata",
    )
    base.update(overrides)
    return BirthData(**base)


def test_ist_conversion():
    utc = utc_datetime(make())

    assert (utc.hour, utc.minute) == (11, 14)
    assert utc.tzinfo == timezone.utc


def test_us_dst_summer_vs_winter_offsets_differ():
    summer = local_datetime(
        make(year=2021, month=7, day=1, hour=12, minute=0,
             timezone="America/New_York")
    )
    winter = local_datetime(
        make(year=2021, month=1, day=1, hour=12, minute=0,
             timezone="America/New_York")
    )

    assert summer.utcoffset() == timedelta(hours=-4)  # EDT
    assert winter.utcoffset() == timedelta(hours=-5)  # EST


def test_ambiguous_fall_back_time_fold_disambiguation():
    # 2021-11-07 01:30 America/New_York occurs twice.
    first = utc_datetime(
        make(year=2021, month=11, day=7, hour=1, minute=30,
             timezone="America/New_York", fold=0)
    )
    second = utc_datetime(
        make(year=2021, month=11, day=7, hour=1, minute=30,
             timezone="America/New_York", fold=1)
    )

    assert second - first == timedelta(hours=1)


def test_historical_offset_change_is_honored():
    """
    India used +06:30 (WWII 'war time') from 1942-09-01 to
    1945-10-15. A fixed +05:30 offset, the pre-remediation live
    path, would be one hour wrong here (about 15 degrees of
    ascendant motion).
    """
    wartime = local_datetime(
        make(year=1944, month=6, day=15, hour=12, minute=0,
             timezone="Asia/Kolkata")
    )

    assert wartime.utcoffset() == timedelta(hours=6, minutes=30)


def test_fractional_seconds_preserved():
    dt = local_datetime(make(second=30.25))

    assert dt.second == 30
    assert dt.microsecond == 250000
