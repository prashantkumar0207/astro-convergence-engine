from pytest import approx

from engine.astrology.planet_mapper import map_planet


def test_planet_mapper():
    result = map_planet(
        longitude=125.5,
        ascendant=95.0,
    )

    assert result["longitude"] == approx(125.5)
    assert result["sign"] == 5
    assert result["degree"] == approx(5.5)
    assert result["house"] == 2