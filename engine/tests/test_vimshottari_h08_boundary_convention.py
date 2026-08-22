"""
H-08 boundary-convention pin and disclosure field (DP-018 Option 3, ADR-0071).

VIMSHOTTARI_V1's seed nakshatra classification uses the KP layer's exact
[start, end) boundary-ownership rule (Decimal(str(x)), no float-noise
tolerance) for every seeding school, including Parashari - ratified as the
deliberate convention by ADR-0071, unchanged by it. engine.astrology.
nakshatra's own classifier instead promotes a float within 1e-10 degrees
below a boundary up to it, a different rule for a different purpose
(absorbing ephemeris float noise). At six specific float spellings of
nakshatra boundaries these two conventions disagree about which nakshatra
a longitude belongs to, and therefore about the dasha seed lord. This file
pins exactly where and why (the audit's own "Tests required" line) and
asserts the new seed_boundary_convention disclosure field names the
convention explicitly, mirroring engine.models.transit_event.TransitEvent.
declared_division (H-02, ADR-0065).
"""

from engine.astrology import longitude_utils
from engine.astrology.nakshatra import nakshatra
from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI
from engine.dasha import tables as dasha_tables
from engine.dasha.vimshottari import vimshottari_kp, vimshottari_parashari
from engine.dasha.vimshottari import vimshottari_from_moon
from engine.models.birth_data import BirthData
from engine.models.dasha import SEED_BOUNDARY_CONVENTION_KP_EXACT

NAK_SPAN = dasha_tables.NAK_SPAN
BIRTH_JD = 2451545.0  # J2000.0, matching this suite's existing convention
BIRTH = BirthData(1985, 12, 21, 14, 40, 0.0, 25.6, 85.1333, "Asia/Kolkata")

# The exact boundary-float spellings (float(k * 360/27) for k in 0..26)
# where VIMSHOTTARI_V1's KP-exact seed classification disagrees with
# engine.astrology.nakshatra.nakshatra()'s tolerance-promoted convention.
# Independently reproduced and pinned this session (DP-018, ADR-0071); a
# change to this set signals either convention's rounding behaviour moved
# and needs a fresh owner decision, not a silent test update.
DIVERGENT_BOUNDARY_K = (7, 11, 14, 17, 22, 25)


def _boundary_floats():
    return {k: float(NAK_SPAN * k) for k in range(27)}


def test_exactly_the_documented_six_boundaries_diverge():
    boundaries = _boundary_floats()
    diverging = [
        k
        for k, moon in boundaries.items()
        if nakshatra(moon) != vimshottari_from_moon(moon, BIRTH_JD, depth=1).seed_nakshatra_number
    ]
    assert tuple(sorted(diverging)) == DIVERGENT_BOUNDARY_K


def test_divergent_boundaries_are_off_by_exactly_one_nakshatra():
    """Pins the direction and magnitude of the divergence, not merely its
    existence: at these points the dasha seed always reports the
    classifier's nakshatra number minus one."""

    boundaries = _boundary_floats()
    for k in DIVERGENT_BOUNDARY_K:
        moon = boundaries[k]
        classifier = nakshatra(moon)
        dasha_seed = vimshottari_from_moon(moon, BIRTH_JD, depth=1).seed_nakshatra_number
        assert dasha_seed == classifier - 1, (k, moon, classifier, dasha_seed)


def test_non_divergent_boundaries_still_agree():
    """Negative control for the pin itself: the other 21 boundary floats
    agree exactly, proving the assertions above are not vacuous and would
    also catch the divergent set growing."""

    boundaries = _boundary_floats()
    for k, moon in boundaries.items():
        if k in DIVERGENT_BOUNDARY_K:
            continue
        classifier = nakshatra(moon)
        dasha_seed = vimshottari_from_moon(moon, BIRTH_JD, depth=1).seed_nakshatra_number
        assert dasha_seed == classifier, (k, moon, classifier, dasha_seed)


def test_negative_control_pin_would_catch_a_changed_tolerance(monkeypatch):
    """Proves the pin can actually detect a real change, not just describe
    today's numbers: with the engine-wide boundary tolerance disabled, the
    divergent set is NOT the pinned six (verified this session: it becomes
    {17} alone), so a regression in either convention's own rounding
    behaviour would fail this file's other tests, not pass silently."""

    boundaries = _boundary_floats()
    baseline = tuple(
        sorted(
            k
            for k, moon in boundaries.items()
            if nakshatra(moon) != vimshottari_from_moon(moon, BIRTH_JD, depth=1).seed_nakshatra_number
        )
    )
    assert baseline == DIVERGENT_BOUNDARY_K

    monkeypatch.setattr(longitude_utils, "BOUNDARY_TOLERANCE", 0.0)
    mutated = tuple(
        sorted(
            k
            for k, moon in boundaries.items()
            if nakshatra(moon) != vimshottari_from_moon(moon, BIRTH_JD, depth=1).seed_nakshatra_number
        )
    )
    assert mutated != DIVERGENT_BOUNDARY_K

    monkeypatch.undo()
    restored = tuple(
        sorted(
            k
            for k, moon in boundaries.items()
            if nakshatra(moon) != vimshottari_from_moon(moon, BIRTH_JD, depth=1).seed_nakshatra_number
        )
    )
    assert restored == DIVERGENT_BOUNDARY_K


def test_seed_boundary_convention_field_present_and_explicit():
    """The disclosure field names the convention for every timeline,
    regardless of seeding school - it does not vary by school today
    because Option 3 ratifies the status quo rather than changing it."""

    direct = vimshottari_from_moon(93.33333333333333, BIRTH_JD, depth=1)
    parashari = vimshottari_parashari(BIRTH, depth=1)
    kp = vimshottari_kp(BIRTH, depth=1)
    assert direct.seed_boundary_convention == SEED_BOUNDARY_CONVENTION_KP_EXACT
    assert parashari.seed_boundary_convention == SEED_BOUNDARY_CONVENTION_KP_EXACT
    assert kp.seed_boundary_convention == SEED_BOUNDARY_CONVENTION_KP_EXACT
    # Both certified schools remain represented, confirming the field is
    # independent of - not a proxy for - which school seeded the timeline.
    assert parashari.provenance.profile_name == PARASHARI_LAHIRI.name
    assert kp.provenance.profile_name == KP_KRISHNAMURTI.name


def test_existing_certified_behavior_unchanged():
    """H-05's own frozen baseline (ADR-0069) still matches exactly - the
    new field is additive disclosure only, it does not touch any
    calculated value."""

    timeline = vimshottari_from_moon(5.0, BIRTH_JD, depth=1)
    assert timeline.seed_lord == "Ke"
    assert timeline.anchor_jd == 2450586.2020445
    assert timeline.periods[1].lord == "Ve"
    assert timeline.periods[1].start_jd == 2453142.9965925002
