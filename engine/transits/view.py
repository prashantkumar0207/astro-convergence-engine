"""
Natal-relative transit view (TRANSIT_V1, ADR-0008).

A TransitView is the certified transit-moment snapshot annotated
with separations from a natal snapshot's points. Methodology
isolation: both snapshots MUST carry provenance and MUST have been
computed under the SAME CalculationProfile; mixing ayanamsas in a
natal-vs-transit comparison is astrologically meaningless and is
refused loudly.
"""

from dataclasses import dataclass

from engine.astronomy.astronomy_snapshot import astronomy_snapshot
from engine.astronomy.profile import CalculationProfile
from engine.models.provenance import Provenance


class TransitProfileError(ValueError):
    """Raised when natal and transit profiles do not match."""


@dataclass(frozen=True, slots=True)
class TransitContact:
    """Separation of one transiting body from one natal point."""

    transiting: str
    natal: str
    separation: float  # degrees in [0, 180]


@dataclass(frozen=True, slots=True)
class TransitView:
    """Transit positions with natal separations at one instant."""

    julian_day: float
    transit_longitudes: dict
    natal_longitudes: dict
    contacts: tuple
    provenance: Provenance


def _separation(a: float, b: float) -> float:
    return abs(((a - b + 180.0) % 360.0) - 180.0)


def transit_view(
    natal_snapshot,
    julian_day: float,
    latitude: float,
    longitude: float,
    profile: CalculationProfile,
) -> TransitView:
    """
    Compute the transit snapshot at ``julian_day`` under ``profile``
    and relate it to ``natal_snapshot``.
    """

    natal_provenance = natal_snapshot.provenance
    if natal_provenance is None:
        raise TransitProfileError("natal snapshot carries no provenance")
    if natal_provenance.profile_name != profile.name:
        raise TransitProfileError(
            "natal and transit profiles must match: natal "
            f"'{natal_provenance.profile_name}' vs transit '{profile.name}'"
        )

    moment = astronomy_snapshot(
        julian_day=julian_day,
        latitude=latitude,
        longitude=longitude,
        profile=profile,
    )

    from engine.astronomy.planet_collection import CANONICAL_GRAHAS

    transit_longitudes = {
        name: moment.sidereal_planets[name].longitude for name in CANONICAL_GRAHAS
    }
    natal_longitudes = {
        name: natal_snapshot.sidereal_planets[name].longitude
        for name in CANONICAL_GRAHAS
    }
    natal_longitudes["Ascendant"] = natal_snapshot.houses.ascendant

    contacts = tuple(
        TransitContact(
            transiting=transiting,
            natal=natal,
            separation=_separation(transit_longitudes[transiting], natal_value),
        )
        for transiting in transit_longitudes
        for natal, natal_value in natal_longitudes.items()
    )

    return TransitView(
        julian_day=julian_day,
        transit_longitudes=transit_longitudes,
        natal_longitudes=natal_longitudes,
        contacts=contacts,
        provenance=moment.provenance,
    )
