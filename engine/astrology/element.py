"""
Element Utilities
"""

ELEMENTS = {
    1: "Fire",
    2: "Earth",
    3: "Air",
    4: "Water",
    5: "Fire",
    6: "Earth",
    7: "Air",
    8: "Water",
    9: "Fire",
    10: "Earth",
    11: "Air",
    12: "Water",
}


def element(sign: int) -> str:
    return ELEMENTS[sign]