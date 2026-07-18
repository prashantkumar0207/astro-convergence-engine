import pytest
from dataclasses import FrozenInstanceError

from engine.models import (
    Relationship,
    PlanetRelationship,
    RelationshipMatrix,
)


def test_relationship_matrix_creation():
    rel = PlanetRelationship(
        source="Sun",
        target="Moon",
        natural=Relationship.FRIEND,
        temporary=None,
        compound=Relationship.FRIEND,
    )

    matrix = RelationshipMatrix(
        relationships=(rel,),
    )

    assert len(matrix.relationships) == 1
    assert matrix.relationships[0] == rel


def test_relationship_matrix_is_immutable():
    rel = PlanetRelationship(
        source="Sun",
        target="Moon",
        natural=Relationship.FRIEND,
        temporary=None,
        compound=Relationship.FRIEND,
    )

    matrix = RelationshipMatrix(
        relationships=(rel,),
    )

    with pytest.raises(FrozenInstanceError):
        matrix.relationships = ()