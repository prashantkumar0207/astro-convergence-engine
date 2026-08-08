from dataclasses import dataclass
from engine.models.chart_navamsa import ChartNavamsa


@dataclass(frozen=True)
class ChartPlanet:

    name: str

    longitude: float

    sign: int

    degree: float

    house: int

    nakshatra: int

    #: Nakshatra pada (1-4). Canonical name per audit A-6;
    #: the 1-9 navamsa division is `navamsa.navamsa_number`.
    nakshatra_pada: int

    navamsa: ChartNavamsa | None = None

    latitude: float = 0.0

    speed: float = 0.0

    distance: float = 0.0

    retrograde: bool = False