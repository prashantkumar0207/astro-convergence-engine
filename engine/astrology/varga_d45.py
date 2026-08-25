"""
D45 Akshavedamsa: sixth production varga through the generic registry
(VARGA_D45_V1, ADR-0077).

Classical source (ADR-0077 section 1): Parashara/BPHS. Each sign
divides into forty-five equal parts of 30/45 = 2/3 degree. For a
planet occupying a movable sign (Aries/Cancer/Libra/Capricorn), the
first akshavedamsa belongs to Aries; for a fixed sign (Taurus/Leo/
Scorpio/Aquarius), to Leo; for a dual sign (Gemini/Virgo/Sagittarius/
Pisces), to Sagittarius. Counting proceeds forward for all twelve
source signs - this is the framework's CyclicVargaRule exactly.

Independently cross-checked against PyJHora's own akshavedamsa_chart
(Traditional Parasara method, chart_method=1) as corroboration, not
authority (ADR-0077 section 1) - both agree exactly across 36
spot-check points and at the three identified floating-point boundary
cases (k=13, 26, 29 of 44 internal per-sign boundaries; ADR-0077
section 3). Only this Traditional Parasara construction is certified;
PyJHora's own Parivritti cyclical, even-reversal, and alternate/
Somanatha variants are explicit non-claims.

The frozen rule below is preserved exactly as certified
(certification/VARGA_D45_V1_certification.json) - do not alter the
table for implementation convenience; any change requires its own ADR
and recertification.
"""

from engine.astrology.varga_registry import (
    register_varga_rule,
    registered_vargas,
)
from engine.astrology.varga_rules import CyclicVargaRule

#: Movable signs (Aries/Cancer/Libra/Capricorn) start at Aries (0);
#: fixed signs (Taurus/Leo/Scorpio/Aquarius) start at Leo (4); dual
#: signs (Gemini/Virgo/Sagittarius/Pisces) start at Sagittarius (8).
#: Frozen literals, verified cell by cell in tests.
D45_PARASHARA = CyclicVargaRule(
    divisions=45,
    start_sign=(0, 4, 8, 0, 4, 8, 0, 4, 8, 0, 4, 8),
    direction=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
)

D45_SCHOOL = "parashara"


def ensure_registered() -> None:
    """Register D45 Parashara if not already present (idempotent)."""

    if (45, D45_SCHOOL) not in registered_vargas():
        register_varga_rule(45, D45_SCHOOL, D45_PARASHARA)


ensure_registered()
