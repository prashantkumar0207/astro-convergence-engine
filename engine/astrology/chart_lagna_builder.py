from engine.astrology.degrees import degree_in_sign
from engine.astrology.nakshatra import nakshatra
from engine.astrology.pada import pada
from engine.astrology.signs import zodiac_sign
from engine.models.chart_lagna import ChartLagna


def build_chart_lagna(longitude: float) -> ChartLagna:
    return ChartLagna(
        longitude=longitude,
        sign=zodiac_sign(longitude),
        degree=degree_in_sign(longitude),
        nakshatra=nakshatra(longitude),
        pada=pada(longitude),
    )