"""
backend/api/main.py

Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.ml.model_loader import initialize

from backend.api.routers.predict import router as predict_router
from backend.api.routers.dropdown import router as dropdown_router
from backend.api.routers.suggestions import router as suggestion_router
from backend.api.routers.forecast import router as forecast_router
from backend.api.routers.explain import router as explain_router
from backend.api.routers.health import router as health_router


# Future routers
# from backend.api.routers.explain import router as explain_router
# from backend.api.routers.forecast import router as forecast_router


app = FastAPI(
    title="Car Price Prediction API",
    version="1.0.0",
    description="AI Powered Used Car Price Prediction System"
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
# Startup
# ==========================================================

@app.on_event("startup")
def startup():
    initialize()
    print("Backend Started Successfully")


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

app.include_router(predict_router)
app.include_router(dropdown_router)
app.include_router(suggestion_router)
app.include_router(forecast_router)
app.include_router(explain_router)
app.include_router(health_router)

# app.include_router(explain_router)
# app.include_router(forecast_router)
