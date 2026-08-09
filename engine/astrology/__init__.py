"""
Astrology Engine

Importing this package registers the certified production vargas
that are served through the generic registry. D1, D9, and D10 remain
hard-wired to their certified modules and never route through the
registry. CERTIFIED_PRODUCTION_VARGAS is the single source of truth
for the sanctioned registry state; tests and certifiers assert
against it.
"""

from engine.astrology import varga_d3  # noqa: F401  (registers D3)
from engine.astrology import varga_d12  # noqa: F401  (registers D12)

#: The sanctioned registry contents, sorted as registered_vargas()
#: returns them. Every addition requires its own approved ADR and
#: certification artifact.
CERTIFIED_PRODUCTION_VARGAS = (
    (3, "parashara"),    # ADR-VARGA-D3-001, VARGA_D3_V1
    (12, "parashara"),   # ADR-VARGA-D12-001, VARGA_D12_V1
)
