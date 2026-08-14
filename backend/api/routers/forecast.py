"""
backend/api/routers/forecast.py

Forecast API
"""

from fastapi import APIRouter

from backend.api.schemas import CarInput
from backend.services.forecast_service import forecast_service

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)


@router.post("/")
def forecast(car: CarInput):

    forecast_result = forecast_service.forecast(
        car.model_dump(exclude_none=True)
    )

    return {
        "success": True,
        "forecast": forecast_result
    }