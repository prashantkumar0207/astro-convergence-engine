from fastapi import FastAPI
import swisseph as swe

app = FastAPI(
    title="Astro Convergence Engine",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "engine": "astro-convergence",
        "version": "0.1.0"
    }


@app.get("/engine/info")
def engine_info():
    return {
        "swisseph_version": swe.version,
        "library": swe.__file__
    }