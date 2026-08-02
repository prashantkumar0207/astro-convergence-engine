"""
Planet Gender
"""

PLANET_GENDER = {
    "Sun": "Male",
    "Moon": "Female",
    "Mars": "Male",
    "Mercury": "Neutral",
    "Jupiter": "Male",
    "Venus": "Female",
    "Saturn": "Neutral",
    "Rahu": "Neutral",
    "Ketu": "Neutral",
}


def planet_gender(name: str) -> str:
    return PLANET_GENDER[name]