from engine.astronomy.planet_collection import planet_collection


def test_planet_collection_returns_model():
    result = planet_collection(2447719.968055556)

    assert len(result.planets) == 12

    assert "Sun" in result.planets
    assert "Moon" in result.planets
    assert "Mars" in result.planets
    assert "Saturn" in result.planets