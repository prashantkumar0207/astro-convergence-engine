from datetime import datetime
from datetime import timedelta
from datetime import timezone

import swisseph as swe
from fastapi import FastAPI

from engine.calculations.calculations import calculate

app = FastAPI(
    title="Astro Convergence Engine",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "engine": "astro-convergence",
        "version": "0.1.0",
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
        birth_datetime=datetime(
            1989,
            7,
            12,
            16,
            44,
            tzinfo=timezone(timedelta(hours=5, minutes=30)),
        ),
        latitude=25.5941,
        longitude=85.1376,
    )

    return result.model_dump()