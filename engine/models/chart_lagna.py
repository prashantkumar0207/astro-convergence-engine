from dataclasses import dataclass


@dataclass(frozen=True)
class ChartLagna:
    longitude: float
    sign: int
    degree: float
    nakshatra: int
    pada: int