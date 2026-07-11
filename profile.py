"""CALCULATION_PROFILE_V1 - every calculation choice pinned and versioned."""
import swisseph as swe

PROFILE = {
  "profile_id": "ASTRO_KERNEL_CALC_PROFILE_V1",
  "engine": "Swiss Ephemeris via pyswisseph",
  "pyswisseph_version": str(swe.version),
  "ephemeris_mode": "MOSHIER analytical (SEFLG_MOSEPH). NOTE: no Swiss Ephemeris data files present "
                    "in this environment; production must pin sepl*/semo* (DE431-based) files and re-run.",
  "frame": "geocentric, apparent (light-time + aberration applied), true equinox of date "
           "(precession + nutation), standard Swiss Ephemeris apparent-position pipeline",
  "delta_t": "Swiss Ephemeris internal deltat() model, logged per run",
  "zodiac": "sidereal; tropical intermediate computed then ayanamsha applied by swisseph",
  "ayanamsha_primary": "SIDM_KRISHNAMURTI (swisseph implementation of KP/Krishnamurti)",
  "ayanamsha_probes": "SIDM_LAHIRI, SIDM_KRISHNAMURTI, SIDM_KRISHNAMURTI_VP291 (if available in build)",
  "node_mode_primary": "MEAN_NODE - IDENTIFIED from both Brihat cases (True-node runs mis-fit Rahu-Ketu by 1.0-1.6 deg; mean-node residual ~ +40 arcsec). KundliStar True-Node setting belongs to the KundliStar app profile, a different fixture set",
  "node_mode_probe": "MEAN_NODE (diagnostic only)",
  "ketu": "Rahu + 180 deg (mod 360)",
  "houses": "Placidus via swe.houses_ex with sidereal flag; Ascendant = ascmc[0]",
  "polar_policy": "Placidus undefined above polar circles; swisseph default fallback (Porphyry) applies; "
                  "all fixture latitudes < 31N so the edge case is unexercised here and flagged for production tests",
  "internal_precision": "full float64 longitudes end-to-end; DMS is display-only and is never fed back; "
                        "hierarchy interval ownership uses exact rational arithmetic with [start,end) rule",
  "timezone": "IANA tzdb via Python zoneinfo (Asia/Kolkata); IST = UTC+5:30, no DST in any fixture era",
  "place_resolution": "static gazetteer v0 (PLACES below) from standard references; proprietary app place "
                      "databases may differ - differences are reported, never silently fitted",
  "error_metric": "absolute angular error in arc-seconds; never percentage",
}

PLACES = {
  "Delhi":    {"lat": 28.6667, "lon": 77.2167},
  "Jaipur":   {"lat": 26.9167, "lon": 75.8167},
  "Patna":    {"lat": 25.6000, "lon": 85.1333},
  "Dehradun": {"lat": 30.3165, "lon": 78.0322},
}
