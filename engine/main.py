"""
FastAPI surface for the calculation engine.

The API serializes provenance-stamped facts produced by the
validated pipeline; it performs no astrology itself (audit
AI/LLM boundary requirement).
"""

from dataclasses import asdict

import swisseph as swe
from fastapi import FastAPI

from engine.calculations.calculations import calculate
from engine.models.birth_data import BirthData
from engine.version import ENGINE_VERSION

app = FastAPI(
    title="Astro Convergence Engine",
    version=ENGINE_VERSION,
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "engine": "astro-convergence",
        "version": ENGINE_VERSION,
    }


@app.get("/engine/info")
def engine_info():
    return {
        "swisseph_version": swe.version,
        "library": swe.__file__,
    }


@app.get("/engine/test")
def engine_test():
    result = calculate(
        BirthData(
            year=1989,
            month=7,
            day=12,
            hour=16,
            minute=44,
            second=0.0,
            latitude=25.5941,
            longitude=85.1376,
            timezone="Asia/Kolkata",
        )
    )

    # AstronomyResult is a frozen dataclass, not a pydantic model;
    # the previous .model_dump() call raised AttributeError
    # (audit finding, section 24).
    return asdict(result)
