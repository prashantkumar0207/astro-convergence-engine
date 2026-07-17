from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BirthData:
    """
    Immutable birth data used throughout the engine.

    All calculations originate from this object.
    """

    year: int
    month: int
    day: int

    hour: int
    minute: int
    second: float

    latitude: float
    longitude: float

    timezone: str