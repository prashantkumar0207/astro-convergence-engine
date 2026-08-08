from engine.astronomy.planet_collection import planet_collection


def test_planet_collection_returns_model():
    result = planet_collection(2447719.968055556)

    # 12 direct Swiss bodies + canonical Rahu/Ketu (audit F-14).
    assert len(result.planets) == 14

    assert "Sun" in result.planets
    assert "Moon" in result.planets
    assert "Mars" in result.planets
    assert "Saturn" in result.planets
    assert "Rahu" in result.planets
    assert "Ketu" in result.planets

    rahu = result.planets["Rahu"]
    ketu = result.planets["Ketu"]

    # Rahu follows the mean node by default; Ketu is opposite.
    assert rahu == result.planets["MeanNode"]
    assert abs((ketu.longitude - rahu.longitude) % 360.0 - 180.0) < 1e-12
    assert ketu.speed_longitude == rahu.speed_longitude