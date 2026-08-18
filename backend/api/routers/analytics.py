"""
backend/api/routers/analytics.py

Model Accuracy & Metrics API Router
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/accuracy")
def get_accuracy_metrics():
    """
    Returns the four key comparison metrics:
    Accuracy, Precision, Recall, and F1 Score.
    """
    return {
        "success": True,
        "title": "Comparison of Model Evaluation Metrics",
        "metrics": [
            {"name": "Accuracy", "value": 0.97, "formatted": "0.97"},
            {"name": "Precision", "value": 1.00, "formatted": "1.00"},
            {"name": "Recall", "value": 0.10, "formatted": "0.10"},
            {"name": "F1 Score", "value": 0.18, "formatted": "0.18"}
        ]
    }
