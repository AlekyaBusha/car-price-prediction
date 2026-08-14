"""
Depreciation forecast engine for car price prediction.

Predicts today's price and future prices by increasing
vehicle_age and km_driven.
"""

import pandas as pd

from backend.ml.feature_engineering import engineer_features
from backend.ml.model_loader import loader


ANNUAL_KM_ESTIMATE = 12000
MONTHS_AHEAD = [0, 6, 12, 24]


def build_car_row(car_details: dict) -> pd.DataFrame:
    """
    Converts dictionary into DataFrame.
    """
    return pd.DataFrame([car_details])


def forecast_price(car_details: dict, months_ahead=None):
    """
    Predict current and future prices.
    """

    if months_ahead is None:
        months_ahead = MONTHS_AHEAD

    model = loader.model
    freq_map = loader.freq_map
    reference_columns = loader.reference_columns

    forecasts = []

    for months in months_ahead:

        projected = car_details.copy()

        projected["vehicle_age"] = (
            car_details["vehicle_age"] + (months / 12)
        )

        projected["km_driven"] = (
            car_details["km_driven"]
            + (months / 12) * ANNUAL_KM_ESTIMATE
        )

        row_df = build_car_row(projected)

        encoded_df, _ = engineer_features(
            row_df,
            freq_map=freq_map,
            reference_columns=reference_columns
        )

        price = model.predict(encoded_df)[0]

        forecasts.append(
            {
                "months": months,
                "price": round(float(price), 2)
            }
        )

    return forecasts