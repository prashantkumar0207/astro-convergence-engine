"""
D30 Trimsamsa: production varga (VARGA_D30_V1, ADR-0011).

Classical source (Decision VB-A): Brihat Parashara Hora Shastra,
trimsamsa description. The five tara grahas rule unequal parts, no
luminaries. ODD signs: 5 degrees Mars (target Aries), 5 Saturn
(Aquarius), 8 Jupiter (Sagittarius), 7 Mercury (Gemini), 5 Venus
(Libra). EVEN signs, reversed order: 5 Venus (Taurus), 7 Mercury
(Virgo), 8 Jupiter (Pisces), 5 Saturn (Capricorn), 5 Mars (Scorpio).
Each planet's target is the sign it rules with the matching gender:
odd-sign segments target male (odd) signs, even-sign segments female
(even) signs, a constraint re-derived in tests. Only this Parashara
variant is certified.
"""

from engine.astrology.varga_registry import (
    register_varga_rule,
    registered_vargas,
)
from engine.astrology.varga_rules import SegmentVargaRule

_ODD = ((5.0, 0), (5.0, 10), (8.0, 8), (7.0, 2), (5.0, 6))
_EVEN = ((5.0, 1), (7.0, 5), (8.0, 11), (5.0, 9), (5.0, 7))

D30_PARASHARA = SegmentVargaRule(
    segments=(
        _ODD,    # Aries
        _EVEN,   # Taurus
        _ODD,    # Gemini
        _EVEN,   # Cancer
        _ODD,    # Leo
        _EVEN,   # Virgo
        _ODD,    # Libra
        _EVEN,   # Scorpio
        _ODD,    # Sagittarius
        _EVEN,   # Capricorn
        _ODD,    # Aquarius
        _EVEN,   # Pisces
    ),
    division=30,
)

D30_SCHOOL = "parashara"


def ensure_registered() -> None:
    """Register D30 Parashara if not already present (idempotent)."""

    if (30, D30_SCHOOL) not in registered_vargas():
        register_varga_rule(30, D30_SCHOOL, D30_PARASHARA)


ensure_registered()
