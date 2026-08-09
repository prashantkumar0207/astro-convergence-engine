"""
Vimshottari cross-layer consistency and seeding guards
(Gate 2 of ADR-DASHA-001).
"""

from fractions import Fraction

import pytest

from engine.astronomy.profile import PARASHARI_LAHIRI
from engine.calculations.calculations import calculate
from engine.dasha import tables as dasha_tables
from engine.dasha.vimshottari import (
    DashaSeedError,
    vimshottari_from_moon,
    vimshottari_from_snapshot,
    vimshottari_kp,
    vimshottari_parashari,
)
from engine.kp import tables as kp_tables
from engine.kp.chain import kp_chain
from engine.models.birth_data import BirthData

BIRTH = BirthData(1985, 12, 21, 14, 40, 0.0, 25.6, 85.1333, "Asia/Kolkata")


def test_dasha_tables_equal_kp_tables_without_cross_import():
    # School isolation keeps two copies; this test enforces equality.
    assert dasha_tables.DASHA_LORDS == kp_tables.KP_LORDS
    assert dasha_tables.DASHA_YEARS == kp_tables.KP_YEARS
    assert dasha_tables.NAK_SPAN == kp_tables.NAK_SPAN
    import inspect

    dasha_sources = inspect.getsource(dasha_tables)
    assert "engine.kp" not in dasha_sources
    import engine.dasha.vimshottari as vim_module

    assert "engine.kp" not in inspect.getsource(vim_module)


def test_seed_agrees_with_certified_kp_chain_everywhere():
    # Same conversion rule and [start, end) ownership as the KP layer,
    # so seeding must agree with the certified chain INCLUDING at
    # exact boundaries.
    points = [i * (360.0 / 997) for i in range(997)]
    points += [float(k * dasha_tables.NAK_SPAN) for k in range(27)]
    points += [Fraction(40, 3) * k for k in range(27)]
    for moon in points:
        timeline = vimshottari_from_moon(moon, 2451545.0, depth=1)
        chain = kp_chain(moon)
        assert timeline.seed_nakshatra_number == chain.nakshatra_number, moon
        assert timeline.seed_lord == chain.nakshatra_lord, moon


def test_seed_agrees_with_engine_nakshatra_off_boundaries():
    from engine.astrology.nakshatra import nakshatra

    for i in range(997):
        moon = i * (360.0 / 997) + 0.001
        timeline = vimshottari_from_moon(moon, 2451545.0, depth=1)
        assert timeline.seed_nakshatra_number == nakshatra(moon)


def test_school_explicit_entry_points_record_school_and_profile():
    parashari = vimshottari_parashari(BIRTH, depth=1)
    kp = vimshottari_kp(BIRTH, depth=1)
    assert parashari.school == "parashari"
    assert parashari.provenance.profile_name == "parashari_lahiri"
    assert kp.school == "kp"
    assert kp.provenance.profile_name == "kp_krishnamurti"
    assert parashari.dasha_profile_name == "vimshottari_mean_sidereal_year"
    # Different ayanamsa, different Moon, potentially different balance.
    assert parashari.seed_moon_longitude != kp.seed_moon_longitude


def test_snapshot_without_provenance_rejected():
    class Bare:
        provenance = None

    with pytest.raises(DashaSeedError):
        vimshottari_from_snapshot(Bare())


def test_snapshot_with_foreign_profile_rejected():
    snapshot = calculate(BIRTH, profile=PARASHARI_LAHIRI).snapshot
    provenance = snapshot.provenance

    class Foreign:
        pass

    foreign = Foreign()
    foreign.provenance = type(provenance)(
        profile_name="some_other_profile",
        ayanamsa_mode=provenance.ayanamsa_mode,
        frame=provenance.frame,
        house_system=provenance.house_system,
        node_policy=provenance.node_policy,
        ephemeris_mode=provenance.ephemeris_mode,
        time_basis=provenance.time_basis,
    )
    with pytest.raises(DashaSeedError):
        vimshottari_from_snapshot(foreign)
