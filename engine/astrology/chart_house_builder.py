from engine.astrology.degrees import degree_in_sign
from engine.astrology.signs import zodiac_sign
from engine.models.chart_house import ChartHouse


def build_chart_house(number: int, cusp: float) -> ChartHouse:
    return ChartHouse(
        number=number,
        cusp=cusp,
        sign=zodiac_sign(cusp),
        degree=degree_in_sign(cusp),
    )