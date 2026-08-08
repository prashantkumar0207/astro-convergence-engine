"""
Planet Strength

Shadbala (or any graded strength system) is NOT implemented.
Audit mandate Phase 12: do not implement strength as a placeholder
returning 0.0, because a silent zero reads as a computed value.
"""


def planet_strength(*args, **kwargs) -> float:
    raise NotImplementedError(
        "Planet strength (Shadbala) is not implemented yet. "
        "A placeholder 0.0 was previously returned here; that was "
        "removed so unimplemented strength can never masquerade "
        "as a computed value."
    )
