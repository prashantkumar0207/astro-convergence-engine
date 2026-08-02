"""
Astrological Chart
"""

from dataclasses import dataclass

from engine.models.chart_lagna import ChartLagna
from engine.models.chart_planet import ChartPlanet
from engine.models.house_position import HousePosition
from engine.models.chart_house import ChartHouse
from engine.models.chart_sign import ChartSign
from engine.models.chart_nakshatra import ChartNakshatra
from engine.models.chart_pada import ChartPada


@dataclass(frozen=True)
class Chart:
    planets: dict[str, ChartPlanet]

    chart_type: str = "D1"

    ascendant: float = 0.0

    lagna: ChartLagna | None = None

    house_map: dict[int, ChartHouse] | None = None

    sign_map: dict[int, ChartSign] | None = None

    nakshatra_map: dict[int, ChartNakshatra] | None = None

    pada_map: dict[int, ChartPada] | None = None

    ayanamsa: float = 0.0

    houses: HousePosition | None = None