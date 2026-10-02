"""
ScamShield AI — FastAPI application entry point.
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import init_db
from app.routes import analyze_router, scans_router, recovery_router
from app.ml.predictor import get_predictor  # warm up at startup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    logger.info("ScamShield AI starting up…")
    await init_db()
    # Warm-up ML model (loads from disk once)
    predictor = get_predictor()
    if predictor.is_loaded:
        logger.info("ML model loaded successfully.")
    else:
        logger.warning(
            "ML model not found — using rule-based fallback. "
            "Run `cd ml && python src/train.py` to train."
        )
    yield
    logger.info("ScamShield AI shutting down.")


app = FastAPI(
    title="ScamShield AI",
    description="AI-powered multimodal scam investigation and digital safety platform.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
_origins = settings.cors_origins
_allow_credentials = "*" not in _origins   # credentials not allowed with wildcard

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global exception handler ──────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error. Please try again."},
    )


# ── Routes ────────────────────────────────────────────────────────────────────
app.include_router(analyze_router, prefix="/api")
app.include_router(scans_router, prefix="/api")
app.include_router(recovery_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "name": "ScamShield AI",
        "tagline": "Don't Just Detect the Scam. Understand the Attack.",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/api/health")
async def health():
    predictor = get_predictor()
    return {
        "status": "ok",
        "version": "1.0.0",
        "ml_model_loaded": predictor.is_loaded,
        "ml_method": "ml_model" if predictor.is_loaded else "rule_based_fallback",
    }
