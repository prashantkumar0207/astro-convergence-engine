"""
Longitude-crossing primitive (TRANSIT_V1, ADR-0008).

Finds every instant in a window at which a body's certified sidereal
longitude crosses a target longitude.

Method (Decisions TR-A/TR-B): sample the window on a per-body grid
sized so motion between samples is provably under 45 degrees (max
speed times safety factor 4); inside each grid interval, bracket
speed sign changes and bisect on the SPEED to isolate stations, so
every remaining piece is monotone in longitude; on each monotone
piece the wrapped difference to the target crosses zero at most once
and is refined by bisection on the certified position function to a
1e-6 day bracket. Bisection is deliberate: unconditionally
convergent, and every evaluation is the certified pipeline, so event
times inherit the Tier-0 certification. At each station the tangent
rule applies: if the extremum longitude touches the target within
the residual tolerance without a sign change, a direction-0
"tangent" event is reported (documented rule from the plan).

Retrograde loops therefore yield all crossings, each flagged with
the motion direction at the event.
"""

import swisseph as swe

from engine.astronomy.planet_collection import PLANET_BODIES
from engine.astronomy.profile import CalculationProfile
from engine.astronomy.sidereal_planets import sidereal_planet_position
from engine.models.transit_event import TransitEvent
from engine.transits.speeds import grid_step_days

#: Approved event-time uncertainty guarantee (Decision TR-A; ~0.086 s).
TIME_TOLERANCE_DAYS = 1e-6

#: Actual bisection bracket width, days (~86 microseconds). Tighter
#: than the approved guarantee so the longitude residual at the event
#: meets RESIDUAL_BOUND_ARCSEC even at the Moon's maximum speed
#: (16 deg/day x 1e-9 day = 5.8e-5 arcsec).
REFINE_BRACKET_DAYS = 1e-9

#: Residual certification bound for crossings, arcseconds.
RESIDUAL_BOUND_ARCSEC = 1e-4


def _resolve_body(body: str, profile: CalculationProfile):
    """Map a canonical body name to (swe id, longitude offset deg)."""

    if body in ("Rahu", "Ketu"):
        node = "MeanNode" if profile.node_policy == "mean" else "TrueNode"
        offset = 180.0 if body == "Ketu" else 0.0
        return PLANET_BODIES[node], offset
    return PLANET_BODIES[body], 0.0


def _state(julian_day: float, body_id: int, offset: float, profile: CalculationProfile):
    position = sidereal_planet_position(
        julian_day, body_id, profile.ayanamsa_mode, strict=profile.strict_ephemeris,
    )
    return (position.longitude + offset) % 360.0, position.speed_longitude


def _wrap(delta: float) -> float:
    """Wrap a longitude difference into (-180, 180]."""

    return -((-delta + 180.0) % 360.0 - 180.0)


def find_crossings(
    body: str,
    target_longitude: float,
    jd_start: float,
    jd_end: float,
    profile: CalculationProfile,
    kind: str = "crossing",
) -> tuple:
    """
    All events at which ``body`` crosses ``target_longitude`` in
    [jd_start, jd_end] under ``profile``, ordered by time.
    """

    if jd_end <= jd_start:
        raise ValueError("empty window")
    target = target_longitude % 360.0
    body_id, offset = _resolve_body(body, profile)

    def state(julian_day):
        return _state(julian_day, body_id, offset, profile)

    def diff(longitude):
        return _wrap(longitude - target)

    # 1. Grid pass: collect monotone pieces by isolating stations.
    step = grid_step_days(body)
    grid = [jd_start]
    cursor = jd_start
    while cursor < jd_end:
        cursor = min(cursor + step, jd_end)
        grid.append(cursor)

    samples = [(julian_day, *state(julian_day)) for julian_day in grid]

    pieces = []  # (t0, lon0, t1, lon1) with monotone longitude
    stations = []  # (jd, lon) turning points
    for (t0, lon0, sp0), (t1, lon1, sp1) in zip(samples, samples[1:]):
        if sp0 == 0.0:
            sp0 = 1e-12
        if sp0 * sp1 > 0:
            pieces.append((t0, lon0, t1, lon1))
            continue
        # Station inside: bisect on speed to isolate the turning point.
        a, b = t0, t1
        lon_a = lon0
        speed_a = sp0
        while b - a > REFINE_BRACKET_DAYS:
            mid = 0.5 * (a + b)
            lon_mid, speed_mid = state(mid)
            if speed_a * speed_mid <= 0:
                b = mid
            else:
                a, lon_a, speed_a = mid, lon_mid, speed_mid
        station_jd = 0.5 * (a + b)
        station_lon, _ = state(station_jd)
        stations.append((station_jd, station_lon))
        pieces.append((t0, lon0, station_jd, station_lon))
        pieces.append((station_jd, station_lon, t1, lon1))

    # 2. Crossing pass: bisect the wrapped difference on monotone pieces.
    events = []
    for t0, lon0, t1, lon1 in pieces:
        d0, d1 = diff(lon0), diff(lon1)
        if d0 == 0.0:
            # Exact hit on a sample; the refinement below still runs
            # via the sign-change branch when d0*d1 < 0; a same-sign
            # tangency is handled by the station rule.
            pass
        if d0 * d1 >= 0:
            continue
        if abs(d0 - d1) > 180.0:
            continue  # the piece crossed target+180, not target
        a, b, da = t0, t1, d0
        while b - a > REFINE_BRACKET_DAYS:
            mid = 0.5 * (a + b)
            lon_mid, _ = state(mid)
            dm = diff(lon_mid)
            if da * dm <= 0:
                b = mid
            else:
                a, da = mid, dm
        event_jd = 0.5 * (a + b)
        lon_event, speed_event = state(event_jd)
        events.append(TransitEvent(
            body=body,
            target_longitude=target,
            julian_day=event_jd,
            direction=1 if speed_event >= 0 else -1,
            residual_arcsec=abs(diff(lon_event)) * 3600.0,
            kind=kind,
            profile_name=profile.name,
        ))

    # 3. Tangent rule: a station whose extremum touches the target
    #    without crossing (documented direction-0 event).
    for station_jd, station_lon in stations:
        residual = abs(diff(station_lon)) * 3600.0
        if residual <= RESIDUAL_BOUND_ARCSEC and not any(
            abs(event.julian_day - station_jd) <= 2 * TIME_TOLERANCE_DAYS
            for event in events
        ):
            events.append(TransitEvent(
                body=body,
                target_longitude=target,
                julian_day=station_jd,
                direction=0,
                residual_arcsec=residual,
                kind="tangent",
                profile_name=profile.name,
            ))

    return tuple(sorted(events, key=lambda event: event.julian_day))
