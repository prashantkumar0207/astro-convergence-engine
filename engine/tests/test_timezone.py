from datetime import datetime, timezone, timedelta

import pytest

from engine.core.timezone_engine import to_utc


def test_to_utc():
    local = datetime(
        2025,
        1,
        1,
        17,
        30,
        tzinfo=timezone(timedelta(hours=5, minutes=30)),
    )

    utc = to_utc(local)

    assert utc == datetime(
        2025,
        1,
        1,
        12,
        0,
        tzinfo=timezone.utc,
    )


def test_naive_datetime():
    with pytest.raises(ValueError):
        to_utc(datetime(2025, 1, 1, 12, 0))


def test_invalid_input():
    with pytest.raises(TypeError):
        to_utc("2025-01-01")