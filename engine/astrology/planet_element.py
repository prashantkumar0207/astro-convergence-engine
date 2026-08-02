"""
Planet Element
"""

PLANET_ELEMENT = {
    "Sun": "Fire",
    "Moon": "Water",
    "Mars": "Fire",
    "Mercury": "Earth",
    "Jupiter": "Ether",
    "Venus": "Water",
    "Saturn": "Air",
    "Rahu": "Air",
    "Ketu": "Fire",
}


def planet_element(name: str) -> str:
    return PLANET_ELEMENT[name]