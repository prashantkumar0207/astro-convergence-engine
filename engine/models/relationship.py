from dataclasses import dataclass
from enum import Enum


class Relationship(Enum):
    GREAT_FRIEND = "great_friend"
    FRIEND = "friend"
    NEUTRAL = "neutral"
    ENEMY = "enemy"
    GREAT_ENEMY = "great_enemy"


@dataclass(frozen=True)
class PlanetRelationship:
    source: str
    target: str
    natural: Relationship | None
    temporary: Relationship | None
    compound: Relationship