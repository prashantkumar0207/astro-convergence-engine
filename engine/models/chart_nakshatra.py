from dataclasses import dataclass


@dataclass(frozen=True)
class ChartNakshatra:
    number: int
    name: str
    start: float
    end: float