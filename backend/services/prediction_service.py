"""
backend/services/prediction_service.py

Handles car price prediction.
This service receives user input, converts it into model features,
predicts the price, and returns the result.
"""

import pandas as pd

from backend.ml.feature_engineering import engineer_features
from backend.ml.model_loader import loader


class PredictionService:

    @staticmethod
    def predict(car_data: dict):
        """
        Predict car price from user input.

        Parameters
        ----------
        car_data : dict
            User input from API.

        Returns
        -------
        dict
            Prediction result.
        """

        # Convert dictionary into DataFrame
        df = pd.DataFrame([car_data])

        # Apply feature engineering
        encoded_df, _ = engineer_features(
            df,
            freq_map=loader.freq_map,
            reference_columns=loader.reference_columns
        )

        # Predict
        predicted_price = loader.model.predict(encoded_df)[0]

        # Round price
        predicted_price = round(float(predicted_price), 2)

        return {
            "success": True,
            "predicted_price": predicted_price,
            "currency": "INR"
        }