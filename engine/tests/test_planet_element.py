from engine.astrology.planet_element import planet_element


def test_planet_element():
    assert planet_element("Sun") == "Fire"
    assert planet_element("Moon") == "Water"