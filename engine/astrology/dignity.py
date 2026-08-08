"""
Planetary Dignity and Natural Relationship Accessors

Single authoritative source (audit Phase 12): the data lives in
engine/knowledge/data/dignities.json and
natural_relationships.json, populated from the classical BPHS
tables with citations in the file metadata. This module is the
only code path for dignity facts; no other module may duplicate
these values.

Rahu and Ketu are intentionally absent from the computed accessors
because their dignities and friendships differ across traditions;
the variants are recorded in the data file and must be selected
explicitly by a future per-tradition profile, never silently.
"""

from engine.knowledge.repository import KnowledgeRepository
from engine.models.relationship import Relationship


def _dignity_table() -> dict[str, dict]:
    payload = KnowledgeRepository.dignities()
    return {row["planet"]: row for row in payload["dignities"]}


def _relationship_table() -> dict[str, dict]:
    payload = KnowledgeRepository.natural_relationships()
    return {row["planet"]: row for row in payload["relationships"]}


def dignity(planet: str) -> dict:
    """Full dignity record for a planet."""
    table = _dignity_table()
    if planet not in table:
        raise KeyError(f"No dignity record for {planet}")
    return table[planet]


def is_exalted(planet: str, sign: int) -> bool:
    """True when the planet stands in its exaltation sign."""
    record = dignity(planet)
    if record.get("traditions_differ"):
        raise ValueError(
            f"{planet} exaltation differs across traditions; "
            "select a variant explicitly."
        )
    return record["exaltation_sign"] == sign


def is_debilitated(planet: str, sign: int) -> bool:
    """True when the planet stands in its debilitation sign."""
    record = dignity(planet)
    if record.get("traditions_differ"):
        raise ValueError(
            f"{planet} debilitation differs across traditions; "
            "select a variant explicitly."
        )
    return record["debilitation_sign"] == sign


def is_own_sign(planet: str, sign: int) -> bool:
    """True when the planet stands in one of its own signs."""
    return sign in dignity(planet)["own_signs"]


def is_moolatrikona(planet: str, sign: int, degree: float) -> bool:
    """True when the planet stands in its moolatrikona span."""
    record = dignity(planet)
    if "moolatrikona_sign" not in record:
        raise ValueError(f"No moolatrikona consensus for {planet}.")
    if record["moolatrikona_sign"] != sign:
        return False
    low, high = record["moolatrikona_range"]
    return low <= degree < high


def natural_relationship(source: str, target: str) -> Relationship:
    """
    BPHS naisargika relationship of `source` toward `target`.

    NOT symmetric: Mercury treats the Moon as an enemy while the
    Moon treats Mercury as a friend. That asymmetry is classical.
    """
    table = _relationship_table()
    if source not in table:
        raise KeyError(f"No natural relationship record for {source}")

    row = table[source]

    if target in row["friends"]:
        return Relationship.FRIEND
    if target in row["enemies"]:
        return Relationship.ENEMY
    if target in row["neutral"]:
        return Relationship.NEUTRAL

    raise KeyError(f"{target} not classified relative to {source}")
