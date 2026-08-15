"""
backend/api/routers/explain.py

Explainability API
"""

from fastapi import APIRouter, HTTPException

from backend.api.schemas import CarInput
from backend.ml.feature_engineering import engineer_features
from backend.ml.forecast_engine import build_car_row
from backend.ml.model_loader import loader
from backend.services.explain_service import explain_service


router = APIRouter(
    prefix="/explain",
    tags=["Explainability"]
)


@router.post("/")
def explain(car: CarInput):

    try:

        # IMPORTANT:
        # Use the same model_dump() behavior as /predict/
        car_data = car.model_dump()

        # Convert input into DataFrame
        row_df = build_car_row(car_data)

        # Apply exactly the same feature engineering
        # used by the prediction endpoint
        encoded_df, _ = engineer_features(
            row_df,
            freq_map=loader.freq_map,
            reference_columns=loader.reference_columns
        )

        # Generate SHAP explanation
        explanation = explain_service.explain(
            encoded_df
        )

        # Generate prediction using the SAME encoded row
        predicted_price = loader.model.predict(
            encoded_df
        )[0]

        return {
            "success": True,
            "prediction": round(
                float(predicted_price),
                2
            ),
            "top_features": explanation
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )