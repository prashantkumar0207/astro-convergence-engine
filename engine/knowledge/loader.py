import json
from pathlib import Path
from typing import Any


class KnowledgeLoader:
    """Loads JSON knowledge files."""

    @staticmethod
    def load(path: Path) -> Any:
        if not path.exists():
            raise FileNotFoundError(path)

        with path.open("r", encoding="utf-8") as file:
            return json.load(file)