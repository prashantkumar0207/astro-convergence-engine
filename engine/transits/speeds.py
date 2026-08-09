"""
Per-body maximum apparent geocentric longitude speeds
(TRANSIT_V1, ADR-0008, Decision TR-B).

Values are deliberately GENEROUS upper bounds on |dL/dt| in degrees
per day (Swiss Ephemeris apparent geocentric extremes, rounded UP),
then multiplied by the approved safety factor of 4 when sizing the
sampling grid, so a crossing can never hide between samples and
every station is bracketed. Overestimating costs extra samples;
underestimating could miss events, so all rounding is upward.

Sources for the extreme magnitudes: Swiss Ephemeris apparent daily
motion ranges (Moon up to ~15.4 deg/day at perigee; Mercury up to
~2.2 deg/day; Venus ~1.27; Sun ~1.02; Mars ~0.8; Jupiter ~0.25;
Saturn ~0.14; Uranus ~0.07; Neptune ~0.045; Pluto ~0.05; mean node
~0.053 retrograde, true node oscillating within ~0.25).
"""

#: Generous |speed| upper bounds, degrees per day.
MAX_SPEED_DEG_PER_DAY = {
    "Sun": 1.1,
    "Moon": 16.0,
    "Mercury": 2.5,
    "Venus": 1.4,
    "Mars": 0.9,
    "Jupiter": 0.3,
    "Saturn": 0.2,
    "Uranus": 0.1,
    "Neptune": 0.1,
    "Pluto": 0.1,
    "Rahu": 0.3,
    "Ketu": 0.3,
    "MeanNode": 0.3,
    "TrueNode": 0.3,
}

#: Approved safety factor (Decision TR-B).
SAFETY_FACTOR = 4.0

#: Maximum longitude motion allowed between grid samples, degrees.
#: Well under 90 so the wrapped difference to any target is
#: unambiguous between consecutive samples.
MAX_MOTION_PER_STEP_DEG = 45.0


def grid_step_days(body: str) -> float:
    """Sampling step guaranteeing motion < MAX_MOTION_PER_STEP_DEG."""

    return MAX_MOTION_PER_STEP_DEG / (MAX_SPEED_DEG_PER_DAY[body] * SAFETY_FACTOR)
