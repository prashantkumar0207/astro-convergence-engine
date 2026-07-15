"""
Knowledge Engine Exceptions

Custom exceptions for the Astro Convergence Engine.

These exceptions provide a consistent error hierarchy for all
knowledge-related modules.
"""

from __future__ import annotations


class KnowledgeError(Exception):
    """Base exception for the knowledge engine."""

    pass


class ValidationError(KnowledgeError):
    """Raised when validation fails."""

    pass


class DuplicateNodeError(KnowledgeError):
    """Raised when attempting to register a duplicate canonical node."""

    pass


class NodeNotFoundError(KnowledgeError):
    """Raised when a requested node cannot be found."""

    pass


class RelationshipError(KnowledgeError):
    """Raised when an invalid relationship is created."""

    pass


class RegistryError(KnowledgeError):
    """Raised for registry-related failures."""

    pass


class LoaderError(KnowledgeError):
    """Raised when loading knowledge from disk fails."""

    pass


class ResolverError(KnowledgeError):
    """Raised when dependency resolution fails."""

    pass


class CacheError(KnowledgeError):
    """Raised for cache failures."""

    pass


class SchemaError(KnowledgeError):
    """Raised when a schema is malformed or incompatible."""

    pass


class VersionError(KnowledgeError):
    """Raised when an unsupported version is encountered."""

    pass