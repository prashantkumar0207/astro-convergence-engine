from engine.models import Planet


def test_planet_enum():
    assert Planet.SUN.value == "Sun"
    assert Planet.MOON.value == "Moon"
    assert Planet.MARS.value == "Mars"
    assert Planet.MERCURY.value == "Mercury"
    assert Planet.JUPITER.value == "Jupiter"
    assert Planet.VENUS.value == "Venus"
    assert Planet.SATURN.value == "Saturn"
    assert Planet.RAHU.value == "Rahu"
    assert Planet.KETU.value == "Ketu"