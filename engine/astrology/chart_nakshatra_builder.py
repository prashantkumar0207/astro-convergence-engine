"""
Nakshatra Builder
"""

from engine.astrology.nakshatra import nakshatra
from engine.astrology.nakshatra_names import nakshatra_name
from engine.models.chart_nakshatra import ChartNakshatra


def build_chart_nakshatra(longitude: float) -> ChartNakshatra:
    """
    Build ChartNakshatra from ecliptic longitude.
    """

    number = nakshatra(longitude)

    return ChartNakshatra(
        number=number,
        name=nakshatra_name(number),
        start=(number - 1) * (360 / 27),
        end=number * (360 / 27),
    )