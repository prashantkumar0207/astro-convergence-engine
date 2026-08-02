from typing import Any

from .registry import KnowledgeRegistry


class KnowledgeResolver:
    """Resolves immutable knowledge from the registry."""

    @staticmethod
    def resolve(dataset: str) -> Any:
        return KnowledgeRegistry.get(dataset)