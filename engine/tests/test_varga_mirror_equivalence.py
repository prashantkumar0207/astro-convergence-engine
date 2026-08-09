"""
Phase B equivalence certification: certified D9/D10 vs generic
classifier + mirror tables.

Two genuinely independent computation paths are compared:

  PATH 1 (certified, production authority):
      engine.astrology.navamsa_chart / dashamsa_chart

  PATH 2 (generic):
      varga_mirrors tables + varga_classifier.classify

Neither path calls the other. The mirror tables are additionally
verified CELL BY CELL against independent re-derivations of the
classical rules written inside this test file (not imported from
production), so a future edit to either table breaks this battery.

Longitude equivalence is asserted BIT-IDENTICAL (==, not approx):
the certified expanded-longitude convention is d_sign*30 +
fraction*30, and the generic classifier must reproduce it exactly
for these equal-division vargas.
"""

import hashlib
import math

from engine.astrology.dashamsa_chart import (
    dashamsa_longitude,
    dashamsa_sign,
)
from engine.astrology.navamsa_chart import (
    navamsa_longitude,
    navamsa_number,
    navamsa_sign,
)
from engine.astrology.varga_classifier import classify
from engine.astrology.varga_mirrors import (
    D9_PARASHARA_MIRROR,
    D10_PARASHARA_MIRROR,
)

# ------------------------------------------------------------------
# Rule-table verification (cell by cell, against independent
# re-derivations written here, and against a second hand
# transcription).
# ------------------------------------------------------------------

# Independent second transcription of the tables (typed separately
# from varga_mirrors.py; if either copy is edited, this fails).
D9_TABLE_TRANSCRIPTION = (0, 9, 6, 3, 0, 9, 6, 3, 0, 9, 6, 3)
D10_TABLE_TRANSCRIPTION = (0, 9, 2, 11, 4, 1, 6, 3, 8, 5, 10, 7)


def test_d9_table_matches_transcription_and_classical_derivation():
    assert D9_PARASHARA_MIRROR.divisions == 9
    assert D9_PARASHARA_MIRROR.start_sign == D9_TABLE_TRANSCRIPTION
    assert D9_PARASHARA_MIRROR.direction == (1,) * 12

    movable = {0, 3, 6, 9}
    fixed = {1, 4, 7, 10}

    for sign in range(12):
        if sign in movable:
            expected = sign
        elif sign in fixed:
            expected = (sign + 8) % 12  # 9th sign from it
        else:
            expected = (sign + 4) % 12  # 5th sign from it (dual)

        assert D9_PARASHARA_MIRROR.start_sign[sign] == expected, sign


def test_d10_table_matches_transcription_and_classical_derivation():
    assert D10_PARASHARA_MIRROR.divisions == 10
    assert D10_PARASHARA_MIRROR.start_sign == D10_TABLE_TRANSCRIPTION
    assert D10_PARASHARA_MIRROR.direction == (1,) * 12

    for sign in range(12):
        # Odd zodiac signs are 0-based even indices.
        expected = sign if sign % 2 == 0 else (sign + 8) % 12

        assert D10_PARASHARA_MIRROR.start_sign[sign] == expected, sign


# ------------------------------------------------------------------
# Equivalence helpers: the generic path's derived longitude for an
# equal-division varga is d_sign*30 + fraction*30 (the certified
# convention). Computed HERE, not inside the classifier, per the
# Phase A refinement that longitude projection is a derived concern.
# ------------------------------------------------------------------


def generic_d9(x: float):
    c = classify(x, D9_PARASHARA_MIRROR)
    return c.d_sign, c.d_sign * 30.0 + c.fraction * 30.0, c.division_number


def generic_d10(x: float):
    c = classify(x, D10_PARASHARA_MIRROR)
    return c.d_sign, c.d_sign * 30.0 + c.fraction * 30.0, c.division_number


def sweep_points():
    """51,429 dense sweep points plus the mandated special values."""
    x = 0.0
    while x < 360.0:
        yield x
        x += 0.007
    yield from (0.0, 360.0, 720.0, -360.0, -0.001, -1e-16, -1e-14,
                -1e-12, 359.99999999999994)


def boundary_points():
    """Exact division edges, immediately below/above, and ULP
    neighbors, for both the 9-fold and 10-fold divisions across the
    whole zodiac."""
    for divisions in (9, 10):
        width = 30.0 / divisions
        for sign in range(12):
            for k in range(divisions + 1):
                edge = sign * 30.0 + k * width
                yield edge
                for d in (1e-9, 1e-11, 5e-11, 1e-12, 1e-13):
                    yield edge - d
                    yield edge + d
                y = edge
                for _ in range(10):
                    y = math.nextafter(y, 0.0)
                    yield y
                y = edge
                for _ in range(10):
                    y = math.nextafter(y, 720.0)
                    yield y


# ------------------------------------------------------------------
# D9 equivalence
# ------------------------------------------------------------------


def test_d9_dense_sweep_sign_longitude_and_number_equivalence():
    count = 0
    for x in sweep_points():
        g_sign, g_lon, g_num = generic_d9(x)

        assert g_sign == navamsa_sign(x), x
        assert g_lon == navamsa_longitude(x), x  # bit-identical
        assert g_num == navamsa_number(x), x
        count += 1

    assert count >= 50_000


def test_d9_boundary_and_ulp_battery():
    checked = 0
    for x in boundary_points():
        g_sign, g_lon, _ = generic_d9(x)

        assert g_sign == navamsa_sign(x), x
        assert g_lon == navamsa_longitude(x), x
        assert 0.0 <= g_lon < 360.0, x
        assert int(g_lon // 30.0) % 12 == g_sign, x
        checked += 1

    assert checked > 5_000


def test_d9_output_hash_equivalence():
    certified = hashlib.sha256()
    generic = hashlib.sha256()

    for x in sweep_points():
        certified.update(
            f"{navamsa_sign(x)},{navamsa_longitude(x)!r},"
            f"{navamsa_number(x)};".encode()
        )
        g_sign, g_lon, g_num = generic_d9(x)
        generic.update(f"{g_sign},{g_lon!r},{g_num};".encode())

    assert certified.hexdigest() == generic.hexdigest()


# ------------------------------------------------------------------
# D10 equivalence
# ------------------------------------------------------------------


def test_d10_dense_sweep_sign_and_longitude_equivalence():
    count = 0
    for x in sweep_points():
        g_sign, g_lon, _ = generic_d10(x)

        assert g_sign == dashamsa_sign(x), x
        assert g_lon == dashamsa_longitude(x), x  # bit-identical
        count += 1

    assert count >= 50_000


def test_d10_all_120_segments_equivalence():
    for sign in range(12):
        for segment in range(10):
            x = sign * 30.0 + segment * 3.0 + 1.5

            g_sign, g_lon, g_num = generic_d10(x)

            assert g_sign == dashamsa_sign(x), (sign, segment)
            assert g_lon == dashamsa_longitude(x), (sign, segment)
            assert g_num == segment + 1, (sign, segment)


def test_d10_boundary_and_ulp_battery():
    checked = 0
    for x in boundary_points():
        g_sign, g_lon, _ = generic_d10(x)

        assert g_sign == dashamsa_sign(x), x
        assert g_lon == dashamsa_longitude(x), x
        assert 0.0 <= g_lon < 360.0, x
        assert int(g_lon // 30.0) % 12 == g_sign, x
        checked += 1

    assert checked > 5_000


def test_d10_output_hash_equivalence():
    certified = hashlib.sha256()
    generic = hashlib.sha256()

    for x in sweep_points():
        certified.update(
            f"{dashamsa_sign(x)},{dashamsa_longitude(x)!r};".encode()
        )
        g_sign, g_lon, _ = generic_d10(x)
        generic.update(f"{g_sign},{g_lon!r};".encode())

    assert certified.hexdigest() == generic.hexdigest()


# ------------------------------------------------------------------
# Mirror status guards
# ------------------------------------------------------------------


def test_mirrors_are_not_registered_and_dispatcher_unchanged():
    from engine.astrology.varga_registry import registered_vargas

    # REPLACED (was: registry empty): D3 Drekkana is a certified
    # production entry (ADR-VARGA-D3-001). The mirror guard is that
    # D9/D10 keys are NOT in the registry under any school and the
    # certified modules still serve them.
    from engine.astrology import CERTIFIED_PRODUCTION_VARGAS

    assert registered_vargas() == CERTIFIED_PRODUCTION_VARGAS
    assert not any(division in (1, 9, 10) for division, _school in registered_vargas())

    # The dispatcher still serves D9/D10 from the certified modules.
    from engine.calculations.calculations import calculate
    from engine.astrology.divisional_chart import divisional_chart
    from engine.models.birth_data import BirthData
    from engine.models.dashamsa_chart import DashamsaChart
    from engine.models.navamsa_chart import NavamsaChart

    snapshot = calculate(
        BirthData(1989, 7, 12, 16, 44, 0.0, 25.5941, 85.1376,
                  "Asia/Kolkata")
    ).snapshot

    assert isinstance(divisional_chart(snapshot, 9), NavamsaChart)
    assert isinstance(divisional_chart(snapshot, 10), DashamsaChart)
