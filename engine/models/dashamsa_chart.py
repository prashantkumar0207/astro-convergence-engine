from dataclasses import dataclass

from engine.models.dashamsa_planet import DashamsaPlanet


@dataclass(frozen=True)
class DashamsaChart:
    ascendant: float
    ascendant_sign: int
    planets: dict[str, DashamsaPlanet]