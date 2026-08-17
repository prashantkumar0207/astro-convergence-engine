"""
Varga Rule Contracts (Phase A of the Generic Varga Architecture ADR)

Two frozen, data-only rule kinds cover every classical varga shape:

- CyclicVargaRule: N equal divisions of 30/N degrees, a 12-entry
  START-SIGN TABLE (one 0-based D-sign per 0-based source sign), and
  a per-source-sign counting direction (+1 forward, -1 reverse).
  Covers D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D40, D45, D60
  and their cyclic school variants.

- SegmentVargaRule: per-source-sign tuples of (width_degrees,
  target_sign) whose widths sum to exactly 30. Covers the structural
  outliers D30 (unequal widths, arbitrary targets) and D2 (two-sign
  output space).

Rules are TABLES, not functions, by explicit ADR decision: the
original D10 defect was a wrong start-sign function; tables can be
verified cell by cell against the classical source text before any
longitude arithmetic runs.

Phase A registers NO production varga. These contracts carry no
mathematics of their own; the certified D9/D10 modules remain the
authoritative production implementations.
"""

import hashlib
from dataclasses import dataclass


class InvalidVargaRuleError(ValueError):
    """Raised when a varga rule violates its structural contract."""


@dataclass(frozen=True)
class CyclicVargaRule:
    """
    N equal divisions counted cyclically from a per-sign start sign.

    Attributes
    ----------
    divisions
        Number of equal parts per sign (width = 30/divisions deg).
    start_sign
        Tuple of exactly 12 entries; start_sign[s] is the 0-based
        D-chart sign of the FIRST division of 0-based source sign s.
    direction
        Tuple of exactly 12 entries of +1 (count forward) or -1
        (count backward) per source sign. All default Parashara
        schools use +1 everywhere; the dimension exists because
        recognized school variants count even signs in reverse.
    """

    divisions: int
    start_sign: tuple[int, ...]
    direction: tuple[int, ...] = (1,) * 12

    def __post_init__(self):
        if not isinstance(self.divisions, int) or self.divisions < 1:
            raise InvalidVargaRuleError(
                f"divisions must be a positive integer, got {self.divisions}"
            )

        if len(self.start_sign) != 12:
            raise InvalidVargaRuleError(
                f"start_sign must have exactly 12 entries, got "
                f"{len(self.start_sign)}"
            )

        for s in self.start_sign:
            if not isinstance(s, int) or not 0 <= s <= 11:
                raise InvalidVargaRuleError(
                    f"start_sign entries must be 0-based sign indices "
                    f"0..11, got {s!r}"
                )

        if len(self.direction) != 12:
            raise InvalidVargaRuleError(
                f"direction must have exactly 12 entries, got "
                f"{len(self.direction)}"
            )

        for d in self.direction:
            if d not in (1, -1):
                raise InvalidVargaRuleError(
                    f"direction entries must be +1 or -1, got {d!r}"
                )


@dataclass(frozen=True)
class SegmentVargaRule:
    """
    Non-uniform division: per source sign, an ordered tuple of
    (width_degrees, target_sign) segments whose widths sum to
    exactly 30 degrees.

    Attributes
    ----------
    segments
        Tuple of exactly 12 per-source-sign tuples. Each inner
        entry is (width_degrees > 0, 0-based target sign 0..11).
    division
        The varga's own division number (its D-number: 3, 2, 30,
        ...), self-declared here rather than inferred from
        `len(segments[s])`. The two are deliberately NOT required to
        agree: D30 Trimsamsa has five unequal per-sign segments, one
        per ruling planet, registered under division 30 - segment
        count cannot stand in for division identity for this rule
        kind the way `divisions` does for `CyclicVargaRule`. This
        field exists so `register_varga_rule` can verify a segment
        rule actually is the rule it claims to be when registered
        (B-01, `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`), the
        same protection `CyclicVargaRule.divisions` already gives
        that rule kind.
    """

    segments: tuple[tuple[tuple[float, int], ...], ...]
    division: int

    #: Tolerance for the per-sign width sum check. Widths are
    #: classical whole/simple degrees; this only absorbs float
    #: representation, never a real deficit.
    _SUM_TOLERANCE = 1e-9

    def __post_init__(self):
        if (
            not isinstance(self.division, int)
            or isinstance(self.division, bool)
            or self.division < 2
        ):
            raise InvalidVargaRuleError(
                f"division must be an integer >= 2, got {self.division!r}"
            )

        if len(self.segments) != 12:
            raise InvalidVargaRuleError(
                f"segments must have exactly 12 per-sign entries, got "
                f"{len(self.segments)}"
            )

        segment_counts = set()
        for sign_index, sign_segments in enumerate(self.segments):
            if not sign_segments:
                raise InvalidVargaRuleError(
                    f"sign {sign_index}: at least one segment required"
                )
            segment_counts.add(len(sign_segments))

            total = 0.0
            for entry in sign_segments:
                if len(entry) != 2:
                    raise InvalidVargaRuleError(
                        f"sign {sign_index}: segment entries must be "
                        f"(width, target_sign), got {entry!r}"
                    )
                width, target = entry
                if not isinstance(width, (int, float)) or width <= 0:
                    raise InvalidVargaRuleError(
                        f"sign {sign_index}: segment width must be "
                        f"positive, got {width!r}"
                    )
                if not isinstance(target, int) or not 0 <= target <= 11:
                    raise InvalidVargaRuleError(
                        f"sign {sign_index}: target sign must be 0..11, "
                        f"got {target!r}"
                    )
                total += float(width)

            if abs(total - 30.0) > self._SUM_TOLERANCE:
                raise InvalidVargaRuleError(
                    f"sign {sign_index}: segment widths sum to {total}, "
                    f"must sum to exactly 30 degrees"
                )

        # Cardinality invariant (B-01): every sign must carve the same
        # NUMBER of segments as every other sign in this rule. Widths
        # and targets may differ (that is the whole point of a
        # SegmentVargaRule), but a rule that gives one sign 3 segments
        # and another 5 is malformed regardless of division identity.
        if len(segment_counts) != 1:
            raise InvalidVargaRuleError(
                "segment count per sign is not uniform across all 12 "
                f"signs: counts seen = {sorted(segment_counts)}"
            )


def rule_content_sha256(rule) -> str:
    """
    Deterministic content fingerprint of a frozen varga rule's own
    table data (B-02, `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`).

    This pins CONTENT, not object identity: two rules built from
    identical table data hash identically, which is intentional.
    Object identity (`get_varga_rule(N, school) is DN_PARASHARA`) is a
    separate check catching a different failure mode - a swap of
    which object is registered under a key. This hash catches the
    complementary case: the certified module re-imported after its
    literals were edited would construct a new, differently-hashing
    object, even if it were then registered validly under the same
    key. Neither check alone proves both "the certified object" and
    "the certified content"; together they do.
    """

    if isinstance(rule, CyclicVargaRule):
        payload = repr(("cyclic", rule.divisions, rule.start_sign, rule.direction))
    elif isinstance(rule, SegmentVargaRule):
        payload = repr(("segment", rule.division, rule.segments))
    else:
        raise TypeError(f"unknown rule type: {type(rule)!r}")

    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
