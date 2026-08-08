from dataclasses import dataclass


@dataclass(frozen=True)
class DashamsaPlanet:
    name: str
    longitude: float
    sign: int
    degree: float
    segment: int