from pathlib import Path
from typing import Any

from .loader import KnowledgeLoader


class KnowledgeRepository:
    DATA_DIR = Path(__file__).parent / "data"

    @classmethod
    def load_json(cls, filename: str) -> Any:
        return KnowledgeLoader.load(cls.DATA_DIR / filename)

    @classmethod
    def planets(cls) -> Any:
        return cls.load_json("planets.json")

    @classmethod
    def signs(cls) -> Any:
        return cls.load_json("signs.json")

    @classmethod
    def houses(cls) -> Any:
        return cls.load_json("houses.json")

    @classmethod
    def dignities(cls) -> Any:
        return cls.load_json("dignities.json")

    @classmethod
    def natural_relationships(cls) -> Any:
        return cls.load_json("natural_relationships.json")

    @classmethod
    def nakshatras(cls) -> Any:
        return cls.load_json("nakshatras.json")