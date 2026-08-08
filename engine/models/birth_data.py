from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BirthData:
    """
    Immutable birth data used throughout the engine.

    All calculations originate from this object.

    Attributes
    ----------
    year, month, day, hour, minute, second
        Local civil date and time of birth, proleptic Gregorian
        calendar (dates recorded in the Julian calendar must be
        converted by the caller).
    latitude
        Geographic latitude in degrees, north positive, [-90, 90].
    longitude
        Geographic longitude in degrees, east positive, [-180, 180].
        NOTE: geographic, not ecliptic; see engine/models docs.
    timezone
        IANA timezone name (e.g. "Asia/Kolkata"). Fixed numeric
        offsets are not accepted by the validated pipeline because
        they silently ignore DST and historical offset changes.
    fold
        Disambiguation for local times that occur twice during a
        DST fall-back transition: 0 selects the first occurrence
        (default), 1 the second, per PEP 495.
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

    fold: int = 0
