"""The EVR identifier family (ADR-0113 s2 B; ADR-0115 s3; docs/NAMING_STANDARD.md s2).

Event records, eight digits, zero-padded, monotone, immutable and never reused. Issued only by an
EventStore's own durable counter, at first persistence. ENT's allocation procedure is not extended
to this family (ADR-0113 s2 B); this one is decided by ADR-0115 s3. This module validates and
formats; it never allocates.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from engine.evidence.identifiers import IdentifierError

FAMILY = "EVR"
WIDTH = 8
PATTERN = re.compile(r"EVR-\d{8}")
FIRST, LAST = 1, 10 ** WIDTH - 1

__all__ = ["FAMILY", "WIDTH", "PATTERN", "FIRST", "LAST", "EventRecordId", "IdentifierError"]


@dataclass(frozen=True, slots=True, order=True)
class EventRecordId:
    """One EVR identifier. Construct from an issued number, or parse an exact string."""

    value: str

    def __post_init__(self):
        if not isinstance(self.value, str) or PATTERN.fullmatch(self.value) is None:
            raise IdentifierError(f"not an EVR identifier: {self.value!r}")
        if int(self.value[len(FAMILY) + 1:]) < FIRST:
            raise IdentifierError(f"EVR numbers start at {FIRST}: {self.value!r}")

    @classmethod
    def from_number(cls, number: int) -> "EventRecordId":
        if isinstance(number, bool) or not isinstance(number, int) or not FIRST <= number <= LAST:
            raise IdentifierError(f"EVR number out of range: {number!r}")
        return cls(f"{FAMILY}-{number:0{WIDTH}d}")

    @property
    def number(self) -> int:
        return int(self.value[len(FAMILY) + 1:])

    def __str__(self) -> str:
        return self.value
