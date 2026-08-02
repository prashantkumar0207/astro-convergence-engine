from engine.astrology.element import element


def test_element():
    assert element(1) == "Fire"
    assert element(2) == "Earth"
    assert element(3) == "Air"
    assert element(4) == "Water"