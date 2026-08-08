"""
Provenance Model

Remediates audit finding F-20: computed astronomical facts must be
self-describing. A snapshot without provenance cannot be audited,
and a convergence layer cannot safely join facts whose frames,
ayanamsas, or ephemeris modes are unknown.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Provenance:
    """
    Describes exactly how an astronomical snapshot was computed.

    Attributes
    ----------
    profile_name
        Name of the CalculationProfile used.
    ayanamsa_mode
        Swiss Ephemeris sidereal mode (swe.SIDM_*).
    frame
        Reference frame of all longitudes in the snapshot
        ("sidereal" for the production pipeline).
    house_system
        Swiss Ephemeris house system code as a string (e.g. "P").
    node_policy
        Which lunar node represents Rahu ("mean" or "true").
    ephemeris_mode
        Actual ephemeris used: "swieph" or "moseph".
    time_basis
        Time scale note. The engine passes UTC-derived Julian Days
        to swe.*_ut functions, which expect UT1; the difference
        (|UT1-UTC| <= 0.9 s) is accepted and documented.
    """

    profile_name: str
    ayanamsa_mode: int
    frame: str
    house_system: str
    node_policy: str
    ephemeris_mode: str
    time_basis: str = "UTC treated as UT1 (|dUT1| <= 0.9 s)"
