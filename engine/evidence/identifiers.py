"""The ENT identifier family (ADR-0111 s2 item 3; ADR-0114 s3; docs/NAMING_STANDARD.md s2).

Kind-neutral, eight digits, zero-padded, monotone, immutable and never reused. Issued only by an
EntityStore's durable counter, at first persistence. This module validates and formats; it never
allocates.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

FAMILY = "ENT"
WIDTH = 8
PATTERN = re.compile(r"ENT-\d{8}")
FIRST, LAST = 1, 10 ** WIDTH - 1


class IdentifierError(ValueError):
    """An identifier that is not a valid member of its family."""


@dataclass(frozen=True, slots=True, order=True)
class EntityId:
    """One ENT identifier. Construct from an issued number, or parse an exact string."""

    value: str

    def __post_init__(self):
        if not isinstance(self.value, str) or PATTERN.fullmatch(self.value) is None:
            raise IdentifierError(f"not an ENT identifier: {self.value!r}")
        if int(self.value[len(FAMILY) + 1:]) < FIRST:
            raise IdentifierError(f"ENT numbers start at {FIRST}: {self.value!r}")

    @classmethod
    def from_number(cls, number: int) -> "EntityId":
        if isinstance(number, bool) or not isinstance(number, int) or not FIRST <= number <= LAST:
            raise IdentifierError(f"ENT number out of range: {number!r}")
        return cls(f"{FAMILY}-{number:0{WIDTH}d}")

    @property
    def number(self) -> int:
        return int(self.value[len(FAMILY) + 1:])

    def __str__(self) -> str:
        return self.value
