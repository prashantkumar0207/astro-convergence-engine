"""
Deterministic Swiss Ephemeris initialization and mode guarding.

Remediates audit finding F-02: the engine previously requested
FLG_SWIEPH, never configured the ephemeris path, and discarded the
return flags, so every position silently fell back to the Moshier
analytical ephemeris.

Policy (documented per audit Phase 1 requirement 8):

- The bundled Swiss Ephemeris files (sepl_18.se1, semo_18.se1,
  seas_18.se1) cover 1800-01-01 through 2399-12-31 CE.
- In strict mode (the default), any computation for which Swiss
  Ephemeris data could not be used raises EphemerisFallbackError.
  This includes dates outside the bundled range and missing files.
  Swiss Ephemeris signals this by setting FLG_MOSEPH in the return
  flags instead of raising, so the guard inspects the flags.
- In non-strict mode the Moshier result is returned, and the caller
  receives the ACTUAL mode so it can be recorded as provenance.
  Non-strict results must never be labelled "swieph".
"""

from pathlib import Path

import swisseph as swe


class EphemerisError(RuntimeError):
    """Base class for ephemeris configuration and mode errors."""


class EphemerisFilesMissingError(EphemerisError):
    """Raised when the bundled ephemeris files cannot be located."""


class EphemerisFallbackError(EphemerisError):
    """
    Raised in strict mode when Swiss Ephemeris data was requested
    but the computation fell back to the Moshier ephemeris.
    """


#: Files required for planetary, lunar and asteroid computation.
REQUIRED_FILES = ("sepl_18.se1", "semo_18.se1", "seas_18.se1")

#: Coverage of the bundled *_18.se1 files (inclusive years, CE).
BUNDLED_RANGE_YEARS = (1800, 2399)

MODE_SWIEPH = "swieph"
MODE_MOSEPH = "moseph"

_initialized_path: str | None = None


def default_ephemeris_path() -> Path:
    """
    Return the repository root, where the bundled .se1 files live.

    Resolved package-relatively (audit DECISION_LOG D-005 discipline):
    this file is engine/astronomy/ephemeris.py, so parents[2] is the
    repository root.
    """
    return Path(__file__).resolve().parents[2]


def initialize_ephemeris(
    path: Path | str | None = None,
    force: bool = False,
) -> str:
    """
    Configure the Swiss Ephemeris search path exactly once.

    Idempotent: repeated calls with the same effective path are
    no-ops. Raises EphemerisFilesMissingError if any required file
    is absent, so misconfiguration fails loudly at initialization
    rather than silently at computation time.

    Returns the path that was configured.
    """
    global _initialized_path

    resolved = Path(path) if path is not None else default_ephemeris_path()

    if _initialized_path == str(resolved) and not force:
        return _initialized_path

    missing = [
        name for name in REQUIRED_FILES if not (resolved / name).is_file()
    ]

    if missing:
        raise EphemerisFilesMissingError(
            f"Ephemeris files missing in {resolved}: {missing}"
        )

    swe.set_ephe_path(str(resolved))
    _initialized_path = str(resolved)

    return _initialized_path


def ephemeris_mode_from_flags(retflags: int) -> str:
    """Translate Swiss Ephemeris return flags into a mode label."""
    if retflags & swe.FLG_MOSEPH:
        return MODE_MOSEPH

    if retflags & swe.FLG_SWIEPH:
        return MODE_SWIEPH

    return f"unknown({retflags})"


def calc_ut_checked(
    julian_day: float,
    body: int,
    flags: int,
    strict: bool = True,
) -> tuple[tuple[float, ...], str]:
    """
    Call swe.calc_ut with the ephemeris path guaranteed configured,
    inspect the return flags, and return (values, mode).

    In strict mode, raises EphemerisFallbackError whenever
    FLG_SWIEPH was requested but the computation actually used the
    Moshier ephemeris (missing files, out-of-range date, or any
    other silent degradation).
    """
    initialize_ephemeris()

    result = swe.calc_ut(julian_day, body, flags)

    values, retflags = result[0], result[1]

    mode = ephemeris_mode_from_flags(retflags)

    if strict and (flags & swe.FLG_SWIEPH) and mode != MODE_SWIEPH:
        raise EphemerisFallbackError(
            f"Swiss Ephemeris requested but mode was '{mode}' at "
            f"JD {julian_day} for body {body}. Bundled files cover "
            f"{BUNDLED_RANGE_YEARS[0]}-{BUNDLED_RANGE_YEARS[1]} CE."
        )

    return values, mode
