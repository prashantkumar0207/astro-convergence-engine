"""
Dasha calculation profiles (VIMSHOTTARI_V1, ADR-0007).

Decision DA-A (approved 2026-08-09): the year-length convention is an
EXPLICIT profile field with no hidden default resolution; traditions
and software differ (mean/true sidereal, tropical, savana 360-day,
lunar), and the choice moves period boundaries by days to months over
a lifetime. VIMSHOTTARI_MEAN_SIDEREAL_YEAR is the V1 certified
profile, pinned to the external oracle's documented constant
(PyJHora 4.8.7 const.sidereal_year = 365.256364 days, the mean
sidereal year). Additional conventions may be added later as new
named profiles, each requiring its own certification.
"""

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class DashaProfile:
    """
    Frozen dasha timing conventions.

    Attributes
    ----------
    name
        Stable identifier recorded in every timeline's provenance.
    year_length_days
        EXACT length of one dasha year in days.
    source
        Where this convention is documented.
    """

    name: str
    year_length_days: Fraction
    source: str


VIMSHOTTARI_MEAN_SIDEREAL_YEAR = DashaProfile(
    name="vimshottari_mean_sidereal_year",
    year_length_days=Fraction(365256364, 1000000),
    source=(
        "Mean sidereal year, 365.256364 days; PyJHora 4.8.7 "
        "const.sidereal_year (external oracle convention, "
        "DHASA_YEAR_DURATION.MEAN_SIDEREAL_YEAR)"
    ),
)


class UnsupportedDashaProfileError(NotImplementedError):
    """Raised when a dasha profile is not production-certified (H-06, ADR-0070)."""


#: The sanctioned VIMSHOTTARI_V1 profile set (H-06, ADR-0070). Keyed on the
#: full frozen instance, not on `name` alone: `DashaProfile` auto-generates
#: field-by-field `__eq__`, so `in` here verifies `year_length_days` and
#: `source` too, not just the name - a name-only allow-list would let a
#: same-named profile carrying a different (uncertified) year_length_days
#: through, the exact class of gap this repository's own varga-registry
#: remediation (B-01, `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`) found
#: and fixed for divisional charts. Every addition requires its own
#: approved ADR and certification artifact, mirroring
#: `engine.astrology.CERTIFIED_PRODUCTION_VARGAS`.
CERTIFIED_DASHA_PROFILES = (VIMSHOTTARI_MEAN_SIDEREAL_YEAR,)  # ADR-0007, VIMSHOTTARI_V1


def validate_dasha_profile(profile: DashaProfile) -> None:
    """
    Refuse a dasha profile VIMSHOTTARI_V1 has not certified (H-06,
    ADR-0070). Two independent checks, in this order so each failure
    mode gets its own clear message:

    1. `year_length_days` must actually be a `Fraction` - the type the
       module's own docstrings promise "exact rational arithmetic
       throughout" on. A same-valued `float` is checked separately
       from certification-identity below because `Fraction(365256364,
       1000000) != 365.256364` in Python's own float representation
       (verified: they are not bit-exact), so relying on the identity
       check alone to also catch a wrong-typed field would be an
       accident of this one profile's specific numbers, not a real
       guarantee.
    2. The profile must be one of `CERTIFIED_DASHA_PROFILES` exactly -
       not merely share a certified name.

    Raises `UnsupportedDashaProfileError` (a `NotImplementedError`
    subclass, matching `UnsupportedVargaError`'s own convention) naming
    what is actually wrong and what is certified.
    """

    if not isinstance(profile.year_length_days, Fraction):
        raise UnsupportedDashaProfileError(
            f"dasha profile {profile.name!r} has year_length_days of type "
            f"{type(profile.year_length_days).__name__}, not Fraction - "
            "VIMSHOTTARI_V1 certifies exact rational year lengths only."
        )

    if profile not in CERTIFIED_DASHA_PROFILES:
        certified_names = tuple(p.name for p in CERTIFIED_DASHA_PROFILES)
        raise UnsupportedDashaProfileError(
            f"dasha profile {profile.name!r} is not production-certified. "
            f"Certified: {certified_names}."
        )
