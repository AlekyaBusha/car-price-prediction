"""
backend/api/routers/explain.py

Explainability API
"""

from fastapi import APIRouter

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

    car_data = car.model_dump(exclude_none=True)

    row_df = build_car_row(car_data)

    encoded_df, _ = engineer_features(
        row_df,
        freq_map=loader.freq_map,
        reference_columns=loader.reference_columns
    )

    explanation = explain_service.explain(encoded_df)

    return {
        "success": True,
        "prediction": float(loader.model.predict(encoded_df)[0]),
        "top_features": explanation
    }