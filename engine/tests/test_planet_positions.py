import swisseph as swe

from engine.astronomy.planet_positions import planet_position


def test_planet_position_returns_model():
    result = planet_position(
        2447719.968055556,
        swe.SUN,
    )

    assert result.longitude >= 0
    assert result.longitude <= 360