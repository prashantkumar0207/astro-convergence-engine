"""
Dasha calculation profiles (VIMSHOTTARI_V1, ADR-DASHA-001).

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
