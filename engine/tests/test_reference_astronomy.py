"""
Independent astronomical reference tests (audit findings F-01,
F-07, and the Tier-0 requirements).

These are the tests the audit found missing: actual longitudes,
ascendants, cusps, and Julian Days asserted against INDEPENDENT
references, collected by the default pytest run.

Reference sources:

1. The swetest 2.10.03 reference binary bundled with this
   repository, executed independently of the Python engine
   (values hard-coded below from its output).
2. The published Astrodienst swetest fixture already present at
   the repository root (1946-12-28, Fagan-Bradley).
3. The defining J2000 epoch (JD 2451545.0 at 2000-01-01 12:00 UT).
4. Cross-check against the certified legacy kernel executed with
   the same profile (different code path, FLG_SIDEREAL end to end).
"""

import swisseph as swe

from engine.astronomy.astronomy_snapshot import astronomy_snapshot
from engine.astronomy.profile import (
    KP_KRISHNAMURTI,
    PARASHARI_LAHIRI,
    CalculationProfile,
)


def angular_arcsec(a: float, b: float) -> float:
    return abs(((a - b + 180.0) % 360.0) - 180.0) * 3600.0


# JD 2447719.968055556 == 1989-07-12 11:14:00 UT.
CANONICAL_JD = 2447719.968055556
PATNA_LAT = 25.5941
PATNA_LON = 85.1376

# Output of the bundled swetest 2.10.03 binary:
#   swetest -b12.7.1989 -ut11:14:00 -p01 -eswe -sid1
#           -house85.1376,25.5941,P -fPl
SWETEST_SUN_SIDEREAL = 86.3688406
SWETEST_MOON_SIDEREAL = 192.3040141
SWETEST_ASCENDANT = 239.0275081
SWETEST_MC = 160.6102382
SWETEST_CUSP_2 = 271.1974055
SWETEST_CUSP_9 = 126.3068472

TOLERANCE_ARCSEC = 0.5


def test_julian_day_j2000_anchor():
    assert swe.julday(2000, 1, 1, 12.0, swe.GREG_CAL) == 2451545.0


def test_engine_sidereal_planets_match_swetest_reference():
    snap = astronomy_snapshot(CANONICAL_JD, PATNA_LAT, PATNA_LON)

    sun_err = angular_arcsec(
        snap.sidereal_planets["Sun"].longitude, SWETEST_SUN_SIDEREAL
    )
    moon_err = angular_arcsec(
        snap.sidereal_planets["Moon"].longitude, SWETEST_MOON_SIDEREAL
    )

    assert sun_err <= TOLERANCE_ARCSEC, f"Sun error {sun_err} arcsec"
    assert moon_err <= TOLERANCE_ARCSEC, f"Moon error {moon_err} arcsec"


def test_engine_ascendant_and_cusps_match_swetest_reference():
    snap = astronomy_snapshot(CANONICAL_JD, PATNA_LAT, PATNA_LON)

    assert snap.houses.frame == "sidereal"

    asc_err = angular_arcsec(snap.houses.ascendant, SWETEST_ASCENDANT)
    mc_err = angular_arcsec(snap.houses.mc, SWETEST_MC)
    c2_err = angular_arcsec(snap.houses.houses[1], SWETEST_CUSP_2)
    c9_err = angular_arcsec(snap.houses.houses[8], SWETEST_CUSP_9)

    for label, err in (
        ("ascendant", asc_err),
        ("mc", mc_err),
        ("cusp2", c2_err),
        ("cusp9", c9_err),
    ):
        assert err <= TOLERANCE_ARCSEC, f"{label} error {err} arcsec"


def test_planets_and_houses_share_the_sidereal_frame():
    """
    Regression test for audit BLOCKER F-01 (23.71 degree frame
    mismatch): the ascendant must match an independent sidereal
    house computation, not the tropical one.
    """
    snap = astronomy_snapshot(CANONICAL_JD, PATNA_LAT, PATNA_LON)

    swe.set_sid_mode(snap.ayanamsa.mode)

    _, ascmc_sid = swe.houses_ex(
        CANONICAL_JD, PATNA_LAT, PATNA_LON, b"P", swe.FLG_SIDEREAL
    )
    _, ascmc_trop = swe.houses_ex(
        CANONICAL_JD, PATNA_LAT, PATNA_LON, b"P", 0
    )

    assert angular_arcsec(snap.houses.ascendant, ascmc_sid[0]) < 1e-6
    # And it must NOT be the tropical value (which is a full
    # ayanamsa away).
    assert angular_arcsec(snap.houses.ascendant, ascmc_trop[0]) > 3600.0


def test_engine_matches_certified_legacy_kernel_same_profile():
    """
    Cross-check against the certified legacy kernel running the
    identical profile (Lahiri, mean node, Placidus, strict SWIEPH).
    Different code path, same convention: agreement must be at the
    milli-arcsecond level.
    """
    from legacy import engine as legacy_engine

    out = legacy_engine.compute(
        "1989-07-12",
        "16:44",
        PATNA_LAT,
        PATNA_LON,
        ayan="LAHIRI",
        node="MEAN",
        tz="Asia/Kolkata",
        ephe="SWIEPH",
        ephe_path=str(
            __import__("pathlib").Path(__file__).resolve().parents[2]
        ),
        strict_ephe=True,
    )

    snap = astronomy_snapshot(
        out["input"]["jd_ut"], PATNA_LAT, PATNA_LON, PARASHARI_LAHIRI
    )

    for name in ("Sun", "Moon", "Mars", "Saturn", "Rahu", "Ketu"):
        err = angular_arcsec(
            snap.sidereal_planets[name].longitude,
            out["bodies"][name]["lon_deg"],
        )
        assert err < 0.001, f"{name} differs {err} arcsec from legacy"

    asc_err = angular_arcsec(
        snap.houses.ascendant, out["bodies"]["Ascendant"]["lon_deg"]
    )
    assert asc_err < 0.001

    # Restore process state for other tests.
    from engine.astronomy.ephemeris import initialize_ephemeris

    initialize_ephemeris(force=True)


def test_published_astrodienst_fixture_through_engine_profile():
    """
    The Astrodienst-published 1946 fixture (repository root),
    now exercised through the ENGINE pipeline with an explicit
    Fagan-Bradley profile and strict SWIEPH.
    """
    fagan = CalculationProfile(
        name="test_fagan_bradley",
        ayanamsa_mode=swe.SIDM_FAGAN_BRADLEY,
        house_system=b"P",
        node_policy="mean",
    )

    julian_day = swe.julday(1946, 12, 28, 9 + 33 / 60, swe.GREG_CAL)

    snap = astronomy_snapshot(julian_day, 0.0, 0.0, fagan)

    expected_sun = 252 + 3 / 60 + 47.2564 / 3600
    expected_moon = 305 + 24 / 60 + 0.6672 / 3600

    sun_err = angular_arcsec(
        snap.sidereal_planets["Sun"].longitude, expected_sun
    )
    moon_err = angular_arcsec(
        snap.sidereal_planets["Moon"].longitude, expected_moon
    )

    assert sun_err <= TOLERANCE_ARCSEC, f"Sun error {sun_err} arcsec"
    assert moon_err <= TOLERANCE_ARCSEC, f"Moon error {moon_err} arcsec"


def test_multiple_epochs_and_locations_frame_consistency():
    """Sidereal frame invariant across epochs, hemispheres, and
    high latitude (Reykjavik, 64.1 N)."""
    cases = (
        (swe.julday(1900, 1, 1, 6.0, swe.GREG_CAL), 51.5074, -0.1278),
        (swe.julday(1992, 4, 15, 22.5, swe.GREG_CAL), 64.1466, -21.9426),
        (swe.julday(2000, 6, 21, 3.0, swe.GREG_CAL), -33.8688, 151.2093),
        (swe.julday(2350, 12, 31, 12.0, swe.GREG_CAL), 48.8566, 2.3522),
    )

    for julian_day, lat, lon in cases:
        snap = astronomy_snapshot(julian_day, lat, lon)

        swe.set_sid_mode(snap.ayanamsa.mode)
        _, ascmc = swe.houses_ex(julian_day, lat, lon, b"P", swe.FLG_SIDEREAL)

        assert angular_arcsec(snap.houses.ascendant, ascmc[0]) < 1e-6
        assert len(snap.houses.houses) == 12
        assert all(0.0 <= c < 360.0 for c in snap.houses.houses)


def test_kp_profile_records_krishnamurti_and_differs_from_lahiri():
    lahiri = astronomy_snapshot(CANONICAL_JD, PATNA_LAT, PATNA_LON)
    kp = astronomy_snapshot(
        CANONICAL_JD, PATNA_LAT, PATNA_LON, KP_KRISHNAMURTI
    )

    assert lahiri.provenance.ayanamsa_mode == swe.SIDM_LAHIRI
    assert kp.provenance.ayanamsa_mode == swe.SIDM_KRISHNAMURTI
    assert kp.provenance.profile_name == "kp_krishnamurti"

    # Lahiri and Krishnamurti differ by roughly 5-6 arcmin.
    diff_arcmin = abs(lahiri.ayanamsa.value - kp.ayanamsa.value) * 60.0
    assert 3.0 < diff_arcmin < 10.0

    # The whole snapshot follows the profile, not a hidden default.
    sun_shift = angular_arcsec(
        lahiri.sidereal_planets["Sun"].longitude,
        kp.sidereal_planets["Sun"].longitude,
    )
    assert abs(sun_shift / 60.0 - diff_arcmin) < 0.1


def test_provenance_is_complete_and_accurate():
    snap = astronomy_snapshot(CANONICAL_JD, PATNA_LAT, PATNA_LON)

    p = snap.provenance
    assert p is not None
    assert p.profile_name == "parashari_lahiri"
    assert p.frame == "sidereal"
    assert p.house_system == "P"
    assert p.node_policy == "mean"
    assert p.ephemeris_mode == "swieph"
