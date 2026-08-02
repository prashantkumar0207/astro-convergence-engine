from dataclasses import dataclass


@dataclass(frozen=True)
class ChartPada:
    number: int
    nakshatra: int
    start: float
    end: float