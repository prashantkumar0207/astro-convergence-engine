from dataclasses import dataclass

from .relationship import PlanetRelationship


@dataclass(frozen=True)
class RelationshipMatrix:
    relationships: tuple[PlanetRelationship, ...]