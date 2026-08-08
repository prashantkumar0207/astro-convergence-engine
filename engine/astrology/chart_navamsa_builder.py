"""
Navamsa Builder

Builds the D9 summary embedded in a D1 ChartPlanet. Audit finding
F-09: this previously stored the 1-4 NAKSHATRA pada in a field
named `pada` on a Navamsa model, colliding with the 1-9 navamsa
number used by the standalone D9 chart. It now stores the actual
navamsa number so the embedded summary always agrees with
engine.astrology.navamsa_chart.
"""

from engine.astrology.navamsa_chart import navamsa_number, navamsa_sign
from engine.models.chart_navamsa import ChartNavamsa


def build_chart_navamsa(longitude: float) -> ChartNavamsa:
    """
    Build the Navamsa summary for a planetary longitude.
    """

    return ChartNavamsa(
        navamsa_number=navamsa_number(longitude),
        sign=navamsa_sign(longitude),
    )
