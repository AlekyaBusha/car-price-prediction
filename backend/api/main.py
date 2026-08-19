"""
backend/api/main.py

Main FastAPI Application
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.ml.model_loader import initialize

from backend.api.routers.predict import router as predict_router
from backend.api.routers.dropdown import router as dropdown_router
from backend.api.routers.suggestions import router as suggestion_router
from backend.api.routers.forecast import router as forecast_router
from backend.api.routers.explain import router as explain_router
from backend.api.routers.health import router as health_router


# ==========================================================
# Lifespan
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize()
    print("Backend Started Successfully")
    yield


# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title="Car Price Prediction API",
    version="1.0.0",
    description="AI Powered Used Car Price Prediction System",
    lifespan=lifespan
)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# ==========================================================
# Home
# ==========================================================

@app.get("/")
def home():
    return {
        "message": "Car Price Prediction Backend Running"
    }


# ==========================================================
# Routers
# ==========================================================

app.include_router(
    predict_router
)

app.include_router(
    dropdown_router
)

app.include_router(
    suggestion_router
)

app.include_router(
    forecast_router
)

app.include_router(
    explain_router
)

app.include_router(
    health_router
)