from engine.astrology.planet_gender import planet_gender


def test_planet_gender():
    assert planet_gender("Sun") == "Male"
    assert planet_gender("Venus") == "Female"
    assert planet_gender("Mercury") == "Neutral"