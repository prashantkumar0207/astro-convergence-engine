"""
D7 Saptamsa: production varga (VARGA_D7_V1, ADR-0011).

Classical source (Decision VB-A): Brihat Parashara Hora Shastra,
saptamsa description: each sign divides into seven parts of 30/7
degrees; ODD signs count the seven lords from the sign itself, EVEN
signs from the SEVENTH sign from it, forward in both cases. This is
the first production CyclicVargaRule with a non-identity start table.
Only this Parashara variant is certified; backward-counting variants
are explicit non-claims.

Start table below is frozen literals (0-based signs), verified cell
by cell in tests: odd signs (Aries, Gemini, ...; even 0-based index)
start at themselves, even signs (Taurus, Cancer, ...; odd 0-based
index) at the seventh from themselves.
"""

from engine.astrology.varga_registry import (
    register_varga_rule,
    registered_vargas,
)
from engine.astrology.varga_rules import CyclicVargaRule

D7_PARASHARA = CyclicVargaRule(
    divisions=7,
    start_sign=(0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5),
    direction=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
)

D7_SCHOOL = "parashara"


def ensure_registered() -> None:
    """Register D7 Parashara if not already present (idempotent)."""

    if (7, D7_SCHOOL) not in registered_vargas():
        register_varga_rule(7, D7_SCHOOL, D7_PARASHARA)


ensure_registered()
