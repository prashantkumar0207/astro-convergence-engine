"""
Vimshottari dasha timeline (VIMSHOTTARI_V1, ADR-0007).

Mathematics (all exact rational until the final calendar view):
the birth Moon's exact fraction elapsed within its nakshatra fixes
the balance of the first mahadasha (lord = the nakshatra's
Vimshottari lord, remaining years = lord_years x (1 - elapsed)).
Mahadashas follow the fixed 9-lord cycle (120 years total); each
period subdivides proportionally by the same year weights, each
level's cycle starting from its own lord, exactly the recursive
proportional structure certified for the KP sub-lords.

Conversions: the Moon float longitude enters exact arithmetic via
the certified decimal-spelling rule (Decimal(str(x)); same contract
as the KP layer, cross-checked by tests). Nakshatra ownership is
exact [start, end): a Moon exactly on a boundary belongs to the
nakshatra starting there, giving elapsed fraction 0 and a full first
mahadasha. Year offsets stay Fractions; Julian Days are derived as
anchor_jd + float(offset_years x year_length_days).

Seeding is school-explicit (Decision DA-B): entry points require a
provenance-stamped snapshot computed under PARASHARI_LAHIRI or
KP_KRISHNAMURTI and record which one seeded the timeline.
"""

from decimal import Decimal
from fractions import Fraction

import swisseph as swe

from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI
from engine.calculations.calculations import calculate
from engine.dasha.profile import VIMSHOTTARI_MEAN_SIDEREAL_YEAR, DashaProfile
from engine.dasha.tables import (
    DASHA_LORDS,
    DASHA_YEARS,
    NAK_SPAN,
    TOTAL_YEARS,
    YEARS_BY_LORD,
)
from engine.models.birth_data import BirthData
from engine.models.dasha import DashaPeriod, VimshottariTimeline

_SCHOOL_BY_PROFILE = {
    PARASHARI_LAHIRI.name: "parashari",
    KP_KRISHNAMURTI.name: "kp",
}

_AYANAMSA_BY_PROFILE = {
    PARASHARI_LAHIRI.name: swe.SIDM_LAHIRI,
    KP_KRISHNAMURTI.name: swe.SIDM_KRISHNAMURTI,
}


class DashaSeedError(ValueError):
    """Raised when a timeline is requested from an unsuitable snapshot."""


def _to_exact(value) -> Fraction:
    if isinstance(value, Fraction):
        return value
    return Fraction(Decimal(str(value)))


def _subdivide(parent, depth: int, year_length: Fraction, anchor_jd: float):
    """Yield child periods of ``parent`` down to ``depth`` levels."""

    start_index = DASHA_LORDS.index(parent.lord)
    cursor = parent.start_years
    for step in range(9):
        lord = DASHA_LORDS[(start_index + step) % 9]
        width = parent.duration_years * YEARS_BY_LORD[lord] / TOTAL_YEARS
        child = DashaPeriod(
            level=parent.level + 1,
            lords=parent.lords + (lord,),
            start_years=cursor,
            end_years=cursor + width,
            start_jd=anchor_jd + float(cursor * year_length),
            end_jd=anchor_jd + float((cursor + width) * year_length),
        )
        yield child
        if child.level < depth:
            yield from _subdivide(child, depth, year_length, anchor_jd)
        cursor += width


def vimshottari_from_moon(
    moon_longitude,
    birth_jd: float,
    dasha_profile: DashaProfile = VIMSHOTTARI_MEAN_SIDEREAL_YEAR,
    depth: int = 3,
    school: str = "external_seed",
    provenance=None,
) -> VimshottariTimeline:
    """
    Build a Vimshottari timeline from an explicit sidereal Moon
    longitude and birth Julian Day.

    VERIFICATION AND ORACLE USE. Production chart work must go
    through vimshottari_from_snapshot (or the BirthData entry
    points), which enforce school-explicit, provenance-stamped
    seeding; this function exists so certification harnesses can
    isolate the timeline mathematics from the astronomy (e.g. feed
    an external oracle's own Moon into this engine's timeline and
    compare structures per DECISION_LOG D-007).
    """

    if depth not in (1, 2, 3):
        raise ValueError("VIMSHOTTARI_V1 certifies depths 1-3 (DA-C)")

    moon = float(moon_longitude)
    exact = _to_exact(moon_longitude) % 360

    nakshatra_index = int(exact // NAK_SPAN)
    elapsed = (exact - nakshatra_index * NAK_SPAN) / NAK_SPAN
    seed_lord = DASHA_LORDS[nakshatra_index % 9]
    seed_years = YEARS_BY_LORD[seed_lord]
    balance = seed_years * (1 - elapsed)

    year_length = dasha_profile.year_length_days
    elapsed_years = seed_years * elapsed
    anchor_jd = birth_jd - float(elapsed_years * year_length)

    periods = []
    cursor = Fraction(0)
    start_index = DASHA_LORDS.index(seed_lord)
    for step in range(9):
        lord = DASHA_LORDS[(start_index + step) % 9]
        width = Fraction(YEARS_BY_LORD[lord])
        maha = DashaPeriod(
            level=1,
            lords=(lord,),
            start_years=cursor,
            end_years=cursor + width,
            start_jd=anchor_jd + float(cursor * year_length),
            end_jd=anchor_jd + float((cursor + width) * year_length),
        )
        periods.append(maha)
        if depth > 1:
            periods.extend(_subdivide(maha, depth, year_length, anchor_jd))
        cursor += width

    return VimshottariTimeline(
        school=school,
        dasha_profile_name=dasha_profile.name,
        year_length_days=year_length,
        birth_jd=birth_jd,
        anchor_jd=anchor_jd,
        seed_moon_longitude=moon,
        seed_nakshatra_number=nakshatra_index + 1,
        seed_lord=seed_lord,
        seed_elapsed_fraction=elapsed,
        balance_years=balance,
        periods=tuple(periods),
        provenance=provenance,
    )


def vimshottari_from_snapshot(
    snapshot,
    dasha_profile: DashaProfile = VIMSHOTTARI_MEAN_SIDEREAL_YEAR,
    depth: int = 3,
) -> VimshottariTimeline:
    """
    Build the Vimshottari timeline from a provenance-stamped snapshot.

    The snapshot must have been computed under PARASHARI_LAHIRI or
    KP_KRISHNAMURTI (Decision DA-B); anything else raises
    DashaSeedError.
    """

    provenance = snapshot.provenance
    if provenance is None:
        raise DashaSeedError("snapshot carries no provenance; dasha requires it")
    school = _SCHOOL_BY_PROFILE.get(provenance.profile_name)
    if school is None:
        raise DashaSeedError(
            "dasha seeding requires parashari_lahiri or kp_krishnamurti, got "
            f"'{provenance.profile_name}'"
        )
    if provenance.ayanamsa_mode != _AYANAMSA_BY_PROFILE[provenance.profile_name]:
        raise DashaSeedError("snapshot ayanamsa does not match its profile")

    return vimshottari_from_moon(
        snapshot.sidereal_planets["Moon"].longitude,
        snapshot.julian_day,
        dasha_profile=dasha_profile,
        depth=depth,
        school=school,
        provenance=provenance,
    )


def vimshottari_parashari(
    birth_data: BirthData,
    dasha_profile: DashaProfile = VIMSHOTTARI_MEAN_SIDEREAL_YEAR,
    depth: int = 3,
) -> VimshottariTimeline:
    """Vimshottari timeline seeded under PARASHARI_LAHIRI."""

    result = calculate(birth_data, profile=PARASHARI_LAHIRI)
    return vimshottari_from_snapshot(result.snapshot, dasha_profile, depth)


def vimshottari_kp(
    birth_data: BirthData,
    dasha_profile: DashaProfile = VIMSHOTTARI_MEAN_SIDEREAL_YEAR,
    depth: int = 3,
) -> VimshottariTimeline:
    """Vimshottari timeline seeded under KP_KRISHNAMURTI."""

    result = calculate(birth_data, profile=KP_KRISHNAMURTI)
    return vimshottari_from_snapshot(result.snapshot, dasha_profile, depth)
