"""
Astrology Engine

Importing this package registers the certified production vargas
that are served through the generic registry (currently D3
Drekkana, VARGA_D3_V1). D1, D9, and D10 remain hard-wired to their
certified modules and never route through the registry.
"""

from engine.astrology import varga_d3  # noqa: F401  (registers D3)
