"""
Knowledge Schema Validator
==========================

Validates knowledge JSON files against JSON Schema definitions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


class SchemaValidator:
    """
    Generic validator for all knowledge assets.
    """

    @staticmethod
    def load_json(path: Path) -> dict[str, Any]:
        """
        Load a JSON file from disk.
        """

        if not path.exists():
            raise FileNotFoundError(path)

        with path.open("r", encoding="utf-8") as fp:
            return json.load(fp)

    def validate(
        self,
        schema_path: Path,
        data_path: Path,
    ) -> bool:
        """
        Validate a JSON file against a JSON Schema.
        """

        schema = self.load_json(schema_path)
        data = self.load_json(data_path)

        validator = Draft202012Validator(schema)

        validator.validate(data)

        return True