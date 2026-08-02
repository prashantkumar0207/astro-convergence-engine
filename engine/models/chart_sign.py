from dataclasses import dataclass


@dataclass(frozen=True)
class ChartSign:
    number: int
    start: float
    end: float