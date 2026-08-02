from typing import Any

from .repository import KnowledgeRepository


class KnowledgeRegistry:
    """Central access point for immutable knowledge."""

    _cache: dict[str, Any] = {}

    @classmethod
    def get(cls, name: str) -> Any:
        if name not in cls._cache:
            loader = getattr(KnowledgeRepository, name)
            cls._cache[name] = loader()

        return cls._cache[name]

    @classmethod
    def clear(cls) -> None:
        cls._cache.clear()