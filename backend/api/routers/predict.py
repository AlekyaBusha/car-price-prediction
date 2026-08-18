"""
backend/api/routers/predict.py

Prediction API Router
"""

from fastapi import APIRouter, HTTPException
from typing import Optional

from backend.api.schemas import (
    CarInput,
    PredictionResponse,
    VariantPredictionInput
)

from backend.services.prediction_service import (
    PredictionService
)

from backend.services.variant_prediction_service import (
    VariantPredictionService
)


router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


# ==========================================================
# Normal Prediction
# ==========================================================

@router.post(
    "/",
    response_model=PredictionResponse
)
def predict_price(car: CarInput):
    """
    Predict the selling price of a car.
    """

    try:

        result = PredictionService.predict(
            car.model_dump()
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================================
# Predict Price Options
# ==========================================================

@router.post("/options/")
def predict_price_options(car: CarInput):

    try:

        from backend.services.dropdown_service import (
            dropdown_service
        )

        combinations = (
            dropdown_service.get_vehicle_spec_combinations(
                car.brand,
                car.model
            )
        )

        result = PredictionService.predict_options(
            car.model_dump(),
            combinations
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================================
# Predict All Variants
# ==========================================================

@router.post("/variants")
def predict_variants(
    car: VariantPredictionInput
):
    """
    Predict prices for all variants of a selected brand and model.
    """

    try:

        result = VariantPredictionService.predict_variants(
            brand=car.brand,
            model=car.model,
            vehicle_age=car.vehicle_age,
            km_driven=car.km_driven,
            mileage=car.mileage,
            engine=car.engine,
            seats=car.seats,
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )