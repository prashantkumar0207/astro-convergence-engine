"""
D2 Hora: production varga (VARGA_D2_V1, ADR-0011).

Classical source (Decision VB-A): Brihat Parashara Hora Shastra,
hora description: each sign divides into two 15 degree halves; in
ODD signs the first half is the Sun's hora and the second the
Moon's, in EVEN signs the reverse. Traditional Parashara output
space is TWO signs only: the Sun's hora maps to Leo, the Moon's to
Cancer. Tests pin that no other sign can ever appear. Only this
variant is certified; parivritti/Uma-Shambu horas are explicit
non-claims.
"""

from engine.astrology.varga_registry import (
    register_varga_rule,
    registered_vargas,
)
from engine.astrology.varga_rules import SegmentVargaRule

_LEO = 4
_CANCER = 3

_ODD = ((15.0, _LEO), (15.0, _CANCER))
_EVEN = ((15.0, _CANCER), (15.0, _LEO))

D2_PARASHARA = SegmentVargaRule(segments=(
    _ODD, _EVEN, _ODD, _EVEN, _ODD, _EVEN,
    _ODD, _EVEN, _ODD, _EVEN, _ODD, _EVEN,
))

D2_SCHOOL = "parashara"


def ensure_registered() -> None:
    """Register D2 Parashara if not already present (idempotent)."""

    if (2, D2_SCHOOL) not in registered_vargas():
        register_varga_rule(2, D2_SCHOOL, D2_PARASHARA)


ensure_registered()
