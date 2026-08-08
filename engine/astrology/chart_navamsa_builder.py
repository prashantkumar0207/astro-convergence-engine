"""
Navamsa Builder
"""

from engine.astrology.navamsa_chart import navamsa_sign


def build_chart_navamsa(
    longitude: float,
    pada: int | None = None,
) -> int:
    """
    Return the Navamsa (D9) sign for a longitude.
    """
    return navamsa_sign(longitude)