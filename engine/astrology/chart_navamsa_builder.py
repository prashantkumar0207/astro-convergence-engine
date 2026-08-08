"""
Navamsa Builder
"""

from engine.astrology.navamsa_chart import navamsa_sign
from engine.models.chart_navamsa import ChartNavamsa


def build_chart_navamsa(
    longitude: float,
    pada: int | None = None,
) -> ChartNavamsa:
    """
    Build the Navamsa model for a planetary longitude.
    """

    if pada is None:
        pada = int((longitude % (360 / 27)) // (360 / 108)) + 1

    return ChartNavamsa(
        pada=pada,
        sign=navamsa_sign(longitude),
    )