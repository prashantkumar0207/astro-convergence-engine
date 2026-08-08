"""
Birth data validation tests (audit finding F-12: this file was
previously 0 bytes while the validation module itself was broken
and dead).
"""

import pytest

from engine.core.validation import ValidationError, validate_birth_data
from engine.models.birth_data import BirthData


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


def test_valid_birth_data_passes():
    validate_birth_data(make())


@pytest.mark.parametrize(
    "overrides",
    [
        {"latitude": 95.0},
        {"latitude": -90.001},
        {"longitude": 180.5},
        {"longitude": -181.0},
        {"month": 13},
        {"day": 32},
        {"hour": 24},
        {"second": 60.0},
        {"second": -1.0},
        {"timezone": "Not/AZone"},
        {"timezone": "UTC+05:30"},
        {"fold": 2},
    ],
)
def test_invalid_birth_data_rejected(overrides):
    with pytest.raises(ValidationError):
        validate_birth_data(make(**overrides))


def test_boundary_coordinates_accepted():
    validate_birth_data(make(latitude=90.0, longitude=180.0))
    validate_birth_data(make(latitude=-90.0, longitude=-180.0))


def test_nonexistent_dst_gap_time_rejected():
    # 2021-03-14 02:30 does not exist in America/New_York
    # (clocks jump 02:00 -> 03:00).
    with pytest.raises(ValidationError):
        validate_birth_data(
            make(
                year=2021,
                month=3,
                day=14,
                hour=2,
                minute=30,
                timezone="America/New_York",
            )
        )


def test_ambiguous_dst_time_accepted_with_both_folds():
    # 2021-11-07 01:30 occurs twice in America/New_York.
    validate_birth_data(
        make(
            year=2021,
            month=11,
            day=7,
            hour=1,
            minute=30,
            timezone="America/New_York",
            fold=0,
        )
    )
    validate_birth_data(
        make(
            year=2021,
            month=11,
            day=7,
            hour=1,
            minute=30,
            timezone="America/New_York",
            fold=1,
        )
    )
