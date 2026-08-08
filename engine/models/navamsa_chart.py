from dataclasses import dataclass
from engine.models.navamsa_planet import NavamsaPlanet

@dataclass(frozen=True)
class NavamsaChart:
    ascendant: float
    ascendant_sign: int
    planets: dict[str, NavamsaPlanet]
