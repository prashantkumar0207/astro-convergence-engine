from dataclasses import dataclass


@dataclass(frozen=True)
class ChartLagna:
    longitude: float
    sign: int
    degree: float
    nakshatra: int
    #: Nakshatra pada (1-4), canonical name per audit A-6.
    nakshatra_pada: int