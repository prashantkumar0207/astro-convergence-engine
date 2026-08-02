"""
Tests for Knowledge Schema Validation
"""

from pathlib import Path

import pytest

from engine.knowledge.validator import SchemaValidator


SCHEMA = Path("schemas/planet.schema.json")


def test_missing_schema_file():
    """Validator should raise FileNotFoundError for missing schema."""

    validator = SchemaValidator()

    with pytest.raises(FileNotFoundError):
        validator.validate(
            Path("schemas/does_not_exist.json"),
            Path("knowledge/data/planets.json"),
        )


def test_missing_data_file():
    """Validator should raise FileNotFoundError for missing data."""

    validator = SchemaValidator()

    with pytest.raises(FileNotFoundError):
        validator.validate(
            SCHEMA,
            Path("knowledge/data/does_not_exist.json"),
        )