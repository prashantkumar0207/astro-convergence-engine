from datetime import datetime, timedelta, timezone

from engine.calculations.calculations import calculate
from engine.models.astronomy_result import AstronomyResult


def test_calculate_returns_astronomy_result():
    birth_datetime = datetime(
        1989,
        7,
        12,
        16,
        44,
        tzinfo=timezone(timedelta(hours=5, minutes=30)),
    )

    result = calculate(
        birth_datetime=birth_datetime,
        latitude=25.5941,
        longitude=85.1376,
    )

    assert isinstance(result, AstronomyResult)