"""
backend/api/routers/forecast.py

Forecast API
"""

from fastapi import APIRouter, HTTPException

from backend.api.schemas import CarInput
from backend.services.forecast_service import forecast_service


router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)


@router.post("/")
def forecast(car: CarInput):

    try:

        car_data = car.model_dump()

        # These fields are required by the forecast engine
        if car_data.get("vehicle_age") is None:

            raise HTTPException(
                status_code=400,
                detail="Vehicle age is required for price forecast."
            )


        if car_data.get("km_driven") is None:

            raise HTTPException(
                status_code=400,
                detail="KM driven is required for price forecast."
            )


        forecast_result = forecast_service.forecast(
            car_data
        )


        return {
            "success": True,
            "forecast": forecast_result
        }


    except HTTPException:
        raise


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )