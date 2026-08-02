from engine.models.planet import Planet


def test_planet_values():
    assert Planet.SUN.value == "Sun"
    assert Planet.MOON.value == "Moon"
    assert Planet.MARS.value == "Mars"
    assert Planet.MERCURY.value == "Mercury"
    assert Planet.JUPITER.value == "Jupiter"
    assert Planet.VENUS.value == "Venus"
    assert Planet.SATURN.value == "Saturn"
    assert Planet.RAHU.value == "Rahu"
    assert Planet.KETU.value == "Ketu"


def test_planet_str():
    assert str(Planet.SUN) == "Sun"
    assert str(Planet.KETU) == "Ketu"


def test_planet_order():
    assert Planet.ordered() == (
        Planet.SUN,
        Planet.MOON,
        Planet.MARS,
        Planet.MERCURY,
        Planet.JUPITER,
        Planet.VENUS,
        Planet.SATURN,
        Planet.RAHU,
        Planet.KETU,
    )