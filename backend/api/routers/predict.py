"""
backend/api/routers/predict.py

Prediction API Router
"""

from fastapi import APIRouter, HTTPException

from backend.api.schemas import CarInput, PredictionResponse
from backend.services.prediction_service import PredictionService

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


@router.post("/", response_model=PredictionResponse)
def predict_price(car: CarInput):
    """
    Predict the selling price of a car.
    """

    try:

        result = PredictionService.predict(car.model_dump())

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )