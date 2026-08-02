from engine.astrology.planet_names import PLANET_NAMES


def test_planet_names():
    assert len(PLANET_NAMES) == 9
    assert PLANET_NAMES[0] == "Sun"
    assert PLANET_NAMES[-1] == "Ketu"