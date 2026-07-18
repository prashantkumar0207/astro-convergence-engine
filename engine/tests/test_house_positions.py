import pytest

from engine.astronomy.house_positions import house_positions


def test_house_positions_returns_model():
    result = house_positions(
        julian_day=2447719.968055556,
        latitude=25.5941,
        longitude=85.1376,
    )

    assert result.ascendant >= 0
    assert result.ascendant <= 360

    assert result.mc >= 0
    assert result.mc <= 360

    assert len(result.houses) == 12