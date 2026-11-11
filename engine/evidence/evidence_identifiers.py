"""The EVD and RUL identifier families (ADR-0113 s2 B; ADR-0119 AC1, AC2; docs/NAMING_STANDARD.md s2).

- EVD: evidence items, ten digits, zero-padded, monotone, immutable and never reused.
- RUL: rules, six digits, under the same rules. Each version of a rule is identified separately, by
  the pair (rule identifier, version number), so a new version never takes a new RUL number.

Both are issued only by an EvidenceStore's own durable counters, one per family, at first
persistence. ENT's allocation procedure is not extended to them (ADR-0113 s2 B). This module
validates and formats; it never allocates. The WP-E4 RUL records are synthetic structural
references only (ADR-0119 D1, AC3): a RUL number here is not proof of registration or validation in
the future rule registry, and authorizes no interpretation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from engine.evidence.identifiers import IdentifierError

EVD_FAMILY = "EVD"
EVD_WIDTH = 10
EVD_PATTERN = re.compile(r"EVD-\d{10}")
RUL_FAMILY = "RUL"
RUL_WIDTH = 6
RUL_PATTERN = re.compile(r"RUL-\d{6}")
FIRST = 1
EVD_LAST = 10 ** EVD_WIDTH - 1
RUL_LAST = 10 ** RUL_WIDTH - 1

__all__ = ["EVD_FAMILY", "EVD_WIDTH", "EVD_PATTERN", "RUL_FAMILY", "RUL_WIDTH", "RUL_PATTERN", "FIRST", "EVD_LAST",
           "RUL_LAST", "EvidenceId", "RuleId", "IdentifierError"]


def _number(value: str, family: str) -> int:
    return int(value[len(family) + 1:])


@dataclass(frozen=True, slots=True, order=True)
class EvidenceId:
    """One EVD identifier. Construct from an issued number, or parse an exact string."""

    value: str

    def __post_init__(self):
        if not isinstance(self.value, str) or EVD_PATTERN.fullmatch(self.value) is None:
            raise IdentifierError(f"not an EVD identifier: {self.value!r}")
        if _number(self.value, EVD_FAMILY) < FIRST:
            raise IdentifierError(f"EVD numbers start at {FIRST}: {self.value!r}")

    @classmethod
    def from_number(cls, number: int) -> "EvidenceId":
        if isinstance(number, bool) or not isinstance(number, int) or not FIRST <= number <= EVD_LAST:
            raise IdentifierError(f"EVD number out of range: {number!r}")
        return cls(f"{EVD_FAMILY}-{number:0{EVD_WIDTH}d}")

    @property
    def number(self) -> int:
        return _number(self.value, EVD_FAMILY)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, order=True)
class RuleId:
    """One RUL identifier. A rule's versions share it and are told apart by their version number."""

    value: str

    def __post_init__(self):
        if not isinstance(self.value, str) or RUL_PATTERN.fullmatch(self.value) is None:
            raise IdentifierError(f"not a RUL identifier: {self.value!r}")
        if _number(self.value, RUL_FAMILY) < FIRST:
            raise IdentifierError(f"RUL numbers start at {FIRST}: {self.value!r}")

    @classmethod
    def from_number(cls, number: int) -> "RuleId":
        if isinstance(number, bool) or not isinstance(number, int) or not FIRST <= number <= RUL_LAST:
            raise IdentifierError(f"RUL number out of range: {number!r}")
        return cls(f"{RUL_FAMILY}-{number:0{RUL_WIDTH}d}")

    @property
    def number(self) -> int:
        return _number(self.value, RUL_FAMILY)

    def __str__(self) -> str:
        return self.value
