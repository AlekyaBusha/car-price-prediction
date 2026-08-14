"""
Depreciation forecast engine for car price prediction.

Reuses the trained model — no new training required. Given a car's
current details, predicts its price today and at +6/+12/+24 months
by incrementing vehicle_age and km_driven and re-running prediction.
"""

import os
import json
import joblib
import pandas as pd

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from feature_engineering import engineer_features

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')

ANNUAL_KM_ESTIMATE = 12000  # avg km driven per year, used to project future mileage
MONTHS_AHEAD = [0, 6, 12, 24]


def load_artifacts(models_dir: str = None):
    """Loads the trained model, freq_map, and reference_columns needed for inference."""
    if models_dir is None:
        models_dir = MODELS_DIR

    model = joblib.load(os.path.join(models_dir, 'best_model.pkl'))

    with open(os.path.join(models_dir, 'model_freq_map.json'), 'r') as f:
        freq_map = json.load(f)

    with open(os.path.join(models_dir, 'reference_columns.json'), 'r') as f:
        reference_columns = json.load(f)

    return model, freq_map, reference_columns


def build_car_row(car_details: dict) -> pd.DataFrame:
    """
    Converts a car_details dict into a single-row DataFrame with the
    raw columns expected by engineer_features (before encoding).

    car_details must include:
      brand, model, vehicle_age, km_driven, seller_type, fuel_type,
      transmission_type, mileage, engine, max_power, seats
    """
    return pd.DataFrame([car_details])


def forecast_price(car_details: dict, months_ahead: list = None):
    """
    Predicts the car's price today and at each future point in months_ahead
    by incrementing vehicle_age and km_driven, then re-encoding and re-predicting
    with the existing trained model.

    Returns a list of dicts: [{"months": 0, "price": 650000.0}, ...]
    """
    if months_ahead is None:
        months_ahead = MONTHS_AHEAD

    model, freq_map, reference_columns = load_artifacts()

    forecasts = []
    for months in months_ahead:
        projected = car_details.copy()
        projected['vehicle_age'] = car_details['vehicle_age'] + (months / 12)
        projected['km_driven'] = car_details['km_driven'] + (months / 12) * ANNUAL_KM_ESTIMATE

        row_df = build_car_row(projected)
        encoded_df, _ = engineer_features(row_df, freq_map=freq_map, reference_columns=reference_columns)

        price = model.predict(encoded_df)[0]
        forecasts.append({"months": months, "price": round(float(price), 2)})

    return forecasts


if __name__ == '__main__':
    # Quick manual test with a sample car
    sample_car = {
        "brand": "Maruti",
        "model": "Swift",
        "vehicle_age": 3,
        "km_driven": 40000,
        "seller_type": "Individual",
        "fuel_type": "Petrol",
        "transmission_type": "Manual",
        "mileage": 21.0,
        "engine": 1197,
        "max_power": 82.0,
        "seats": 5
    }

    results = forecast_price(sample_car)

    print("Depreciation forecast:")
    for r in results:
        print(f"  +{r['months']:>2} months: ₹{r['price']:,.0f}")