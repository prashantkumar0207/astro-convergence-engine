"""
Nakshatra Builder

Builds the static ChartNakshatra span record for a nakshatra
NUMBER (1-27). Audit finding F-03: the previous signature took a
longitude but was called with the index, which collapsed all 27
map entries onto nakshatras 1-3.
"""

from engine.astrology.nakshatra import NAKSHATRA_SPAN
from engine.astrology.nakshatra_names import nakshatra_name
from engine.models.chart_nakshatra import ChartNakshatra


def build_chart_nakshatra(number: int) -> ChartNakshatra:
    """
    Build ChartNakshatra for a nakshatra number (1-27).
    """

    if not isinstance(number, int) or not 1 <= number <= 27:
        raise ValueError(f"nakshatra number out of range: {number}")

    return ChartNakshatra(
        number=number,
        name=nakshatra_name(number),
        start=(number - 1) * NAKSHATRA_SPAN,
        end=number * NAKSHATRA_SPAN,
    )
