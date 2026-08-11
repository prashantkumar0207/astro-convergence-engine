"""
D12 Dwadasamsa: second production varga through the generic registry
(VARGA_D12_V1, ADR-0010).

Classical source (Decision V12-A): Brihat Parashara Hora Shastra,
dwadasamsa description: each sign divides into twelve parts of 2.5
degrees; the first dwadasamsa belongs to the sign itself and each
subsequent part to the next sign in zodiacal order. This is the
framework's CyclicVargaRule exactly: 12 divisions, start sign = the
source sign for all twelve signs, direction forward everywhere. Only
this Parashara variant is certified; even-reversal and parivritti
variants are explicit non-claims.

This registration is the FIRST production use of the CyclicVargaRule
path (D3 exercised SegmentVargaRule); with it, both certified rule
contracts carry production traffic.

Boundary policy (Decision V12-B) and registration semantics
(Decision V12-C) are identical to VARGA_D3_V1: locked convention
inherited unchanged, registration proven non-invasive.
"""

from engine.astrology.varga_registry import (
    register_varga_rule,
    registered_vargas,
)
from engine.astrology.varga_rules import CyclicVargaRule

#: Start-sign table: the first dwadasamsa of every sign is the sign
#: itself (frozen literals, verified cell by cell in tests).
D12_PARASHARA = CyclicVargaRule(
    divisions=12,
    start_sign=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
    direction=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
)

D12_SCHOOL = "parashara"


def ensure_registered() -> None:
    """Register D12 Parashara if not already present (idempotent)."""

    if (12, D12_SCHOOL) not in registered_vargas():
        register_varga_rule(12, D12_SCHOOL, D12_PARASHARA)


ensure_registered()
