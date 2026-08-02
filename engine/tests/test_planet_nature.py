from engine.astrology.planet_nature import planet_nature


def test_planet_nature():
    assert planet_nature("Jupiter") == "Benefic"
    assert planet_nature("Mars") == "Cruel"