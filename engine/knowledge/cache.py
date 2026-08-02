from typing import Any


class KnowledgeCache:
    """Simple in-memory cache for immutable knowledge."""

    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}

    def has(self, key: str) -> bool:
        return key in self._cache

    def get(self, key: str) -> Any:
        return self._cache[key]

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value

    def clear(self) -> None:
        self._cache.clear()