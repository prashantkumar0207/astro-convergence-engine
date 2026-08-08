from dataclasses import dataclass

@dataclass(frozen=True)
class NavamsaPlanet:
    name: str
    longitude: float
    sign: int
    degree: float
    pada: int
