"""
backend/services/prediction_service.py

Handles car price prediction and fair price range calculation.
"""

import pandas as pd

from backend.ml.feature_engineering import engineer_features
from backend.ml.model_loader import loader
from backend.ml.price_range import get_price_range


class PredictionService:

    @staticmethod
    def predict(car_data: dict):
        """
        Predict car price from user input.

        Returns:
            dict:
                success
                predicted_price
                price_range
                currency
        """

        # -----------------------------------------------------
        # Convert input dictionary into DataFrame
        # -----------------------------------------------------

        df = pd.DataFrame([car_data])

        # -----------------------------------------------------
        # Apply feature engineering
        # -----------------------------------------------------

        encoded_df, _ = engineer_features(
            df,
            freq_map=loader.freq_map,
            reference_columns=loader.reference_columns
        )

        # -----------------------------------------------------
        # Predict price
        # -----------------------------------------------------

        predicted_price = loader.model.predict(encoded_df)[0]

        predicted_price = round(
            float(predicted_price),
            2
        )

        # -----------------------------------------------------
        # Calculate fair price range
        # -----------------------------------------------------

        price_range = get_price_range(
            predicted_price
        )

        # -----------------------------------------------------
        # Return response
        # -----------------------------------------------------

        return {
            "success": True,

            "predicted_price": predicted_price,

            "price_range": price_range,

            "currency": "INR"
        }