"""
Navamsa (D9) Chart
"""

from engine.models.astronomy_snapshot import AstronomySnapshot


def navamsa_sign(longitude: float) -> int:
    """
    Return Navamsa sign index (0-11).
    """

    sign = int(longitude // 30)
    degree = longitude % 30

    navamsa = int(degree // (30 / 9))

    movable = {0, 3, 6, 9}
    fixed = {1, 4, 7, 10}
    dual = {2, 5, 8, 11}

    if sign in movable:
        start = sign
    elif sign in fixed:
        start = (sign + 8) % 12
    else:
        start = (sign + 4) % 12

    return (start + navamsa) % 12


def navamsa_chart(snapshot: AstronomySnapshot) -> AstronomySnapshot:
    """
    Build the Navamsa (D9) chart.

    Placeholder implementation.
    """
    return snapshot