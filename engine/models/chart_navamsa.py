from dataclasses import dataclass


@dataclass(frozen=True)
class ChartNavamsa:
    """
    D9 summary embedded in a D1 planet.

    navamsa_number is the 1-9 division within the sign (canonical
    terminology; audit A-6). The 1-4 nakshatra pada lives on
    ChartPlanet.nakshatra_pada, never here.
    """

    navamsa_number: int
    sign: int
