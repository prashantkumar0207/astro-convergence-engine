"""
Modality Utilities
"""

MODALITIES = {
    1: "Cardinal",
    2: "Fixed",
    3: "Dual",
    4: "Cardinal",
    5: "Fixed",
    6: "Dual",
    7: "Cardinal",
    8: "Fixed",
    9: "Dual",
    10: "Cardinal",
    11: "Fixed",
    12: "Dual",
}


def modality(sign: int) -> str:
    return MODALITIES[sign]