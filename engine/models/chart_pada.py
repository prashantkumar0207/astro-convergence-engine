from dataclasses import dataclass


@dataclass(frozen=True)
class ChartPada:
    """
    One of the 108 global pada spans of the zodiac.

    `number` is the GLOBAL pada index (1-108), a distinct concept
    from the per-nakshatra pada (1-4, ChartPlanet.nakshatra_pada)
    and the navamsa number (1-9, ChartNavamsa.navamsa_number).
    """

    number: int
    nakshatra: int
    start: float
    end: float