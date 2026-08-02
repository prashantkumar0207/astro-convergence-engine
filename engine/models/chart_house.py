from dataclasses import dataclass


@dataclass(frozen=True)
class ChartHouse:
    number: int
    cusp: float
    sign: int
    degree: float