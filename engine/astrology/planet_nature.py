"""
Planet Nature
"""

PLANET_NATURE = {
    "Sun": "Cruel",
    "Moon": "Benefic",
    "Mars": "Cruel",
    "Mercury": "Neutral",
    "Jupiter": "Benefic",
    "Venus": "Benefic",
    "Saturn": "Cruel",
    "Rahu": "Cruel",
    "Ketu": "Cruel",
}


def planet_nature(name: str) -> str:
    return PLANET_NATURE[name]