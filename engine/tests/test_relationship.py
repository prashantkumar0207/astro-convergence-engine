import pytest
from dataclasses import FrozenInstanceError

from engine.models import Relationship, PlanetRelationship


def test_planet_relationship_creation():
    relationship = PlanetRelationship(
        source="Sun",
        target="Moon",
        natural=Relationship.FRIEND,
        temporary=None,
        compound=Relationship.FRIEND,
    )

    assert relationship.source == "Sun"
    assert relationship.target == "Moon"
    assert relationship.natural == Relationship.FRIEND
    assert relationship.temporary is None
    assert relationship.compound == Relationship.FRIEND


def test_planet_relationship_is_immutable():
    relationship = PlanetRelationship(
        source="Sun",
        target="Moon",
        natural=Relationship.FRIEND,
        temporary=None,
        compound=Relationship.FRIEND,
    )

    with pytest.raises(FrozenInstanceError):
        relationship.source = "Mars"