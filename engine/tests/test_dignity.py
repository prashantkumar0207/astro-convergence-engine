"""
Dignity and natural-relationship data tests.

Expected values are the classical BPHS tables, hand-entered here
independently of the JSON data files so a data-entry error in
either copy surfaces as a failure.
"""

import pytest

from engine.astrology.dignity import (
    dignity,
    is_debilitated,
    is_exalted,
    is_moolatrikona,
    is_own_sign,
    natural_relationship,
)
from engine.models.relationship import Relationship


# planet -> (exaltation sign, deep degree, debilitation sign)
CLASSICAL_EXALTATIONS = {
    "Sun": (1, 10.0, 7),
    "Moon": (2, 3.0, 8),
    "Mars": (10, 28.0, 4),
    "Mercury": (6, 15.0, 12),
    "Jupiter": (4, 5.0, 10),
    "Venus": (12, 27.0, 6),
    "Saturn": (7, 20.0, 1),
}

CLASSICAL_OWN_SIGNS = {
    "Sun": {5},
    "Moon": {4},
    "Mars": {1, 8},
    "Mercury": {3, 6},
    "Jupiter": {9, 12},
    "Venus": {2, 7},
    "Saturn": {10, 11},
}


def test_all_seven_classical_exaltations_and_debilitations():
    for planet, (ex_sign, ex_deg, deb_sign) in CLASSICAL_EXALTATIONS.items():
        record = dignity(planet)

        assert record["exaltation_sign"] == ex_sign, planet
        assert record["exaltation_degree"] == ex_deg, planet
        assert record["debilitation_sign"] == deb_sign, planet

        # Debilitation is always the 7th sign from exaltation.
        assert (deb_sign - ex_sign) % 12 == 6, planet

        assert is_exalted(planet, ex_sign)
        assert is_debilitated(planet, deb_sign)
        assert not is_exalted(planet, deb_sign)


def test_all_own_signs():
    for planet, signs in CLASSICAL_OWN_SIGNS.items():
        assert set(dignity(planet)["own_signs"]) == signs, planet
        for sign in signs:
            assert is_own_sign(planet, sign)


def test_moolatrikona_spans():
    assert is_moolatrikona("Sun", 5, 10.0)
    assert not is_moolatrikona("Sun", 5, 25.0)
    assert is_moolatrikona("Mars", 1, 5.0)
    assert not is_moolatrikona("Mars", 8, 5.0)
    assert is_moolatrikona("Moon", 2, 15.0)
    assert not is_moolatrikona("Moon", 2, 2.0)  # first 3 deg: exaltation


def test_rahu_ketu_require_explicit_tradition_choice():
    with pytest.raises(ValueError):
        is_exalted("Rahu", 2)
    with pytest.raises(ValueError):
        is_debilitated("Ketu", 8)


def test_naisargika_relationships_classical_anchors():
    assert natural_relationship("Sun", "Moon") == Relationship.FRIEND
    assert natural_relationship("Sun", "Venus") == Relationship.ENEMY
    assert natural_relationship("Sun", "Mercury") == Relationship.NEUTRAL

    # The classical asymmetry: Mercury treats the Moon as an
    # enemy, the Moon treats Mercury as a friend.
    assert natural_relationship("Mercury", "Moon") == Relationship.ENEMY
    assert natural_relationship("Moon", "Mercury") == Relationship.FRIEND

    assert natural_relationship("Saturn", "Mars") == Relationship.ENEMY
    assert natural_relationship("Venus", "Saturn") == Relationship.FRIEND


def test_relationship_table_is_complete_for_seven_planets():
    planets = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
               "Saturn")

    for source in planets:
        for target in planets:
            if source == target:
                continue
            rel = natural_relationship(source, target)
            assert rel in (
                Relationship.FRIEND,
                Relationship.NEUTRAL,
                Relationship.ENEMY,
            ), (source, target)
