"""
backend/api/routers/health.py

Health Check API
"""

from fastapi import APIRouter

from backend.ml.model_loader import loader

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
def health():

    return {
        "status": "Healthy",
        "model_loaded": loader.model is not None,
        "shap_loaded": loader.shap_explainer is not None,
        "model_metrics": loader.metrics
    }