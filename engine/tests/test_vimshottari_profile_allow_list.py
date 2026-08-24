"""
Certified dasha-profile allow-list and year_length_days type enforcement
(H-06, DP-017 Option 1, ADR-0070).

engine/dasha/profile.py previously accepted any DashaProfile, certified
or not, and any type for year_length_days, including a float, silently
destroying the "exact rational arithmetic throughout" guarantee the
module's own docstrings advertise. Mirrors engine/astrology/
CERTIFIED_PRODUCTION_VARGAS / UnsupportedVargaError, keyed on the full
frozen instance rather than name alone (see engine/dasha/profile.py's
own CERTIFIED_DASHA_PROFILES docstring for why: a name-only allow-list
would let a same-named profile with a different year_length_days
through, the same class of gap B-01 found and fixed for divisional
charts).
"""

from fractions import Fraction

import pytest

from engine.dasha.profile import (
    CERTIFIED_DASHA_PROFILES,
    VIMSHOTTARI_MEAN_SIDEREAL_YEAR,
    DashaProfile,
    UnsupportedDashaProfileError,
    validate_dasha_profile,
)
from engine.dasha.vimshottari import vimshottari_from_moon

BIRTH_JD = 2451545.0  # J2000.0, matching this suite's existing convention


def test_certified_profile_accepted():
    """The one certified profile passes validate_dasha_profile() directly."""

    validate_dasha_profile(VIMSHOTTARI_MEAN_SIDEREAL_YEAR)  # must not raise


def test_certified_profile_accepted_via_entry_point():
    """vimshottari_from_moon() still accepts the certified profile, default and explicit."""

    default = vimshottari_from_moon(100.0, BIRTH_JD, depth=1)
    explicit = vimshottari_from_moon(
        100.0, BIRTH_JD, dasha_profile=VIMSHOTTARI_MEAN_SIDEREAL_YEAR, depth=1
    )
    assert default.dasha_profile_name == "vimshottari_mean_sidereal_year"
    assert default == explicit


def test_uncertified_profile_refused():
    uncertified = DashaProfile("i_made_this_up", Fraction(360), "no source")

    with pytest.raises(UnsupportedDashaProfileError, match="not production-certified"):
        validate_dasha_profile(uncertified)

    with pytest.raises(UnsupportedDashaProfileError, match="not production-certified"):
        vimshottari_from_moon(100.0, BIRTH_JD, dasha_profile=uncertified, depth=1)


def test_float_year_length_refused():
    """A float year_length_days is refused even under the certified profile's own name -
    the type check and the certification-identity check are independent guards."""

    float_year = DashaProfile("vimshottari_mean_sidereal_year", 365.256364, "no source")

    with pytest.raises(UnsupportedDashaProfileError, match="not Fraction"):
        validate_dasha_profile(float_year)

    with pytest.raises(UnsupportedDashaProfileError, match="not Fraction"):
        vimshottari_from_moon(100.0, BIRTH_JD, dasha_profile=float_year, depth=1)


def test_uncertified_name_with_correct_type_still_refused():
    """A well-typed but uncertified profile fails the identity check, not the type check."""

    uncertified_but_exact = DashaProfile(
        "a_plausible_new_convention", Fraction(365, 1), "no source"
    )

    with pytest.raises(UnsupportedDashaProfileError, match="not production-certified"):
        validate_dasha_profile(uncertified_but_exact)


def test_certified_dasha_profiles_contains_exactly_the_one_certified_instance():
    assert CERTIFIED_DASHA_PROFILES == (VIMSHOTTARI_MEAN_SIDEREAL_YEAR,)


def test_existing_certified_behavior_unchanged():
    """Frozen values already independently verified for H-05 (DP-016/ADR-0069) still match
    exactly - the guard rejects other inputs, it does not touch the certified computation."""

    timeline = vimshottari_from_moon(5.0, BIRTH_JD, depth=1)
    assert timeline.seed_lord == "Ke"
    assert timeline.anchor_jd == 2450586.2020445
    assert timeline.periods[1].lord == "Ve"
    assert timeline.periods[1].start_jd == 2453142.9965925002
