"""M-04 (G1 audit; ADR-0111; DP-025 A2 Option 1): DrishtiChart discloses its house convention.

The defect: provenance.house_system is 'P' (Placidus, the snapshot's cusps) while every
aspected_houses value is whole-sign, and nothing on the model said so. The remedy is one additive
field. These tests check the field against an independent whole-sign derivation, and check that the
comparison rejects a chart whose disclosure or houses are wrong.
"""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from engine.models.birth_data import BirthData  # noqa: E402
from engine.models.drishti import DrishtiChart  # noqa: E402
from engine.parashari.drishti import parashari_drishti  # noqa: E402

BIRTHS = (
    BirthData(1990, 1, 15, 6, 0, 0.0, 25.6, 85.1333, "Asia/Kolkata"),
    BirthData(1975, 7, 4, 18, 30, 0.0, -33.8688, 151.2093, "Australia/Sydney"),
    BirthData(2001, 11, 23, 23, 45, 0.0, 51.5, -0.12, "Europe/London"),
)


def disclosure_is_consistent(chart: DrishtiChart) -> bool:
    """True only if the disclosed convention is whole-sign and every house agrees with it.

    The whole-sign house of sign s, counted from ascendant sign a (both 1-based), is
    ((s - a) % 12) + 1. That is derived here, not taken from the production code.
    """

    if chart.houses_convention != "whole_sign":
        return False
    for planet in chart.drishti:
        expected = tuple((sign - chart.ascendant_sign) % 12 + 1 for sign in planet.aspected_signs)
        if tuple(planet.aspected_houses) != expected:
            return False
    return True


@pytest.mark.parametrize("birth", BIRTHS)
def test_real_charts_disclose_whole_sign_houses(birth):
    chart = parashari_drishti(birth)
    assert chart.houses_convention == "whole_sign"
    assert disclosure_is_consistent(chart)


def test_the_defect_the_field_exists_to_disclose_is_still_real():
    """Provenance still names Placidus. The disclosure is what makes the houses unambiguous."""

    chart = parashari_drishti(BIRTHS[0])
    assert chart.provenance.house_system == "P"
    assert any(planet.aspected_houses for planet in chart.drishti)


def test_the_disclosure_is_the_only_new_field():
    names = [field.name for field in dataclasses.fields(DrishtiChart)]
    assert names == ["ascendant_sign", "planet_signs", "drishti", "provenance", "houses_convention"]


@pytest.mark.parametrize("label,mutate", [
    ("a wrong convention", lambda chart: dataclasses.replace(chart, houses_convention="placidus")),
    ("an empty convention", lambda chart: dataclasses.replace(chart, houses_convention="")),
    ("houses shifted by one", lambda chart: dataclasses.replace(chart, drishti=tuple(
        dataclasses.replace(planet, aspected_houses=tuple(house % 12 + 1 for house in planet.aspected_houses))
        for planet in chart.drishti))),
])
def test_the_check_rejects_a_wrong_disclosure(label, mutate):
    chart = parashari_drishti(BIRTHS[1])
    assert disclosure_is_consistent(chart)
    assert not disclosure_is_consistent(mutate(chart)), label
