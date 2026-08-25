"""
Astrology Engine

Importing this package registers the certified production vargas
that are served through the generic registry. D1, D9, and D10 remain
hard-wired to their certified modules and never route through the
registry. CERTIFIED_PRODUCTION_VARGAS is the single source of truth
for the sanctioned registry state; tests and certifiers assert
against it.
"""

from engine.astrology import varga_d2  # noqa: F401  (registers D2)
from engine.astrology import varga_d3  # noqa: F401  (registers D3)
from engine.astrology import varga_d7  # noqa: F401  (registers D7)
from engine.astrology import varga_d12  # noqa: F401  (registers D12)
from engine.astrology import varga_d30  # noqa: F401  (registers D30)
from engine.astrology import varga_d45  # noqa: F401  (registers D45)

#: The sanctioned registry contents, sorted as registered_vargas()
#: returns them. Every addition requires its own approved ADR and
#: certification artifact.
CERTIFIED_PRODUCTION_VARGAS = (
    (2, "parashara"),    # ADR-0011, VARGA_D2_V1
    (3, "parashara"),    # ADR-0009, VARGA_D3_V1
    (7, "parashara"),    # ADR-0011, VARGA_D7_V1
    (12, "parashara"),   # ADR-0010, VARGA_D12_V1
    (30, "parashara"),   # ADR-0011, VARGA_D30_V1
    (45, "parashara"),   # ADR-0077, VARGA_D45_V1
)
