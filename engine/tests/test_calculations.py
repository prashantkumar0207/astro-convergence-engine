import pytest

from engine.calculations.calculations import calculate
from engine.core.validation import ValidationError
from engine.models.astronomy_result import AstronomyResult
from engine.models.birth_data import BirthData


PATNA_BIRTH = BirthData(
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


def test_calculate_returns_astronomy_result():
    result = calculate(PATNA_BIRTH)

    assert isinstance(result, AstronomyResult)


def test_calculate_pipeline_produces_expected_julian_day():
    # 1989-07-12 16:44 IST == 11:14 UT == JD 2447719.9680555556.
    result = calculate(PATNA_BIRTH)

    assert abs(result.snapshot.julian_day - 2447719.9680555556) < 1e-9


def test_calculate_snapshot_is_sidereal_with_provenance():
    result = calculate(PATNA_BIRTH)

    snapshot = result.snapshot

    assert snapshot.houses.frame == "sidereal"
    assert snapshot.provenance is not None
    assert snapshot.provenance.profile_name == "parashari_lahiri"
    assert snapshot.provenance.ephemeris_mode == "swieph"


def test_calculate_rejects_invalid_input():
    bad = BirthData(
        year=1989,
        month=7,
        day=12,
        hour=16,
        minute=44,
        second=0.0,
        latitude=95.0,  # out of range
        longitude=85.1376,
        timezone="Asia/Kolkata",
    )

    with pytest.raises(ValidationError):
        calculate(bad)
