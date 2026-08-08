from dataclasses import dataclass


@dataclass(frozen=True)
class NavamsaPlanet:
    """
    A planet in the D9 chart.

    navamsa_number is the 1-9 division within the source sign
    (canonical terminology per audit A-6; formerly named `pada`).
    """

    name: str
    longitude: float
    sign: int
    degree: float
    navamsa_number: int
