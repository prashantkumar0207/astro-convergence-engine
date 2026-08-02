from engine.models.planet import Planet
from engine.models.planet_metadata import PlanetMetadata


def test_planet_metadata():
    metadata = PlanetMetadata(
        planet=Planet.SUN,
        english_name="Sun",
        sanskrit_name="Surya",
        unicode_symbol="☉",
        category="luminary",
        gender="Male",
        nature="Cruel",
        element="Fire",
        guna="Sattva",
        caste="Kshatriya",
        direction="East",
        weekday="Sunday",
        karakas=(
            "Soul",
            "Father",
            "Government",
            "Authority",
            "Vitality",
            "Power",
        ),
    )

    assert metadata.planet == Planet.SUN
    assert metadata.english_name == "Sun"
    assert metadata.sanskrit_name == "Surya"
    assert metadata.unicode_symbol == "☉"
    assert metadata.category == "luminary"
    assert metadata.gender == "Male"
    assert metadata.nature == "Cruel"
    assert metadata.element == "Fire"
    assert metadata.guna == "Sattva"
    assert metadata.caste == "Kshatriya"
    assert metadata.direction == "East"
    assert metadata.weekday == "Sunday"
    assert metadata.karakas == (
        "Soul",
        "Father",
        "Government",
        "Authority",
        "Vitality",
        "Power",
    )