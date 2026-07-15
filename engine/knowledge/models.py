"""
Knowledge Engine Domain Models

Canonical data structures used by the Astro Convergence Engine.

These models are intentionally independent of storage,
serialization and UI layers.

Author: Astro Convergence Engine
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime
from uuid import uuid4


# ============================================================
# ENUMS
# ============================================================


class NodeType(str, Enum):
    """High-level knowledge object."""

    CONCEPT = "concept"
    QUESTION = "question"
    RULE = "rule"
    FORMULA = "formula"
    PERSON = "person"
    PLANET = "planet"
    HOUSE = "house"
    SIGN = "sign"
    NAKSHATRA = "nakshatra"
    YOGA = "yoga"
    DASHA = "dasha"
    EVENT = "event"
    UNKNOWN = "unknown"


class RelationType(str, Enum):
    """Relationship between two nodes."""

    IS_A = "is_a"
    PART_OF = "part_of"
    DEPENDS_ON = "depends_on"
    REFERENCES = "references"
    REQUIRES = "requires"
    DERIVED_FROM = "derived_from"
    SIMILAR_TO = "similar_to"
    CONTRADICTS = "contradicts"
    ALIAS_OF = "alias_of"


class SourceType(str, Enum):
    """Origin of knowledge."""

    MANUAL = "manual"
    IMPORTED = "imported"
    GENERATED = "generated"
    RESEARCH = "research"
    USER = "user"


class ValidationState(str, Enum):
    """Validation lifecycle."""

    DRAFT = "draft"
    REVIEW = "review"
    VERIFIED = "verified"
    LOCKED = "locked"


# ============================================================
# BASE MODEL
# ============================================================


@dataclass(slots=True)
class BaseModel:
    """
    Base object inherited by all knowledge entities.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    version: int = 1

    metadata: Dict[str, Any] = field(default_factory=dict)

    def touch(self) -> None:
        """Update modification timestamp."""
        self.updated_at = datetime.utcnow()


# ============================================================
# ALIAS
# ============================================================


@dataclass(slots=True)
class Alias(BaseModel):
    """
    Alternative names for a node.
    """

    value: str = ""

    language: str = "en"

    preferred: bool = False


# ============================================================
# REFERENCE
# ============================================================


@dataclass(slots=True)
class Reference(BaseModel):
    """
    Evidence supporting a node.
    """

    title: str = ""

    source: str = ""

    url: Optional[str] = None

    page: Optional[str] = None

    notes: str = ""


# ============================================================
# RELATION
# ============================================================


@dataclass(slots=True)
class Relation(BaseModel):
    """
    Directed edge between two knowledge nodes.
    """

    source_node: str = ""

    target_node: str = ""

    relation: RelationType = RelationType.REFERENCES

    weight: float = 1.0

    bidirectional: bool = False


# ============================================================
# KNOWLEDGE NODE
# ============================================================


@dataclass(slots=True)
class KnowledgeNode(BaseModel):
    """
    Primary entity inside HLKG.
    """

    canonical_id: str = ""

    title: str = ""

    description: str = ""

    node_type: NodeType = NodeType.UNKNOWN

    source_type: SourceType = SourceType.MANUAL

    validation_state: ValidationState = ValidationState.DRAFT

    aliases: List[Alias] = field(default_factory=list)

    references: List[Reference] = field(default_factory=list)

    relationships: List[Relation] = field(default_factory=list)

    tags: List[str] = field(default_factory=list)

    attributes: Dict[str, Any] = field(default_factory=dict)

    confidence: float = 1.0

    active: bool = True

    def add_alias(self, alias: Alias) -> None:
        self.aliases.append(alias)

    def add_reference(self, reference: Reference) -> None:
        self.references.append(reference)

    def add_relation(self, relation: Relation) -> None:
        self.relationships.append(relation)

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)