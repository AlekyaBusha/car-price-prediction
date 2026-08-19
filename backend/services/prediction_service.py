"""
backend/services/prediction_service.py

Handles car price prediction, fair price range calculation, and fallback detection.
"""

import numpy as np
import pandas as pd

from backend.ml.feature_engineering import engineer_features
from backend.ml.model_loader import loader
from backend.ml.price_range import get_price_range
from backend.utils.data_loader import data_loader


class PredictionService:

    # ==========================================================
    # Helper: Check if exact combination exists in dataset
    # ==========================================================

    @staticmethod
    def is_exact_dataset_match(car_data: dict) -> bool:
        """
        Checks if the user's specific Brand + Model + Fuel + Transmission combination
        exists in the training dataset.
        """
        df = data_loader.df
        brand = str(car_data.get("brand", "")).strip().lower()
        model = str(car_data.get("model", "")).strip().lower()
        fuel = str(car_data.get("fuel_type", "")).strip().lower()
        trans = str(car_data.get("transmission_type", "")).strip().lower()

        if not brand or not model or model in ["", "no models", "unknown", "none"] or not fuel or not trans:
            return False

        mask = (
            (df["brand"].astype(str).str.strip().str.lower() == brand) &
            (df["model"].astype(str).str.strip().str.lower() == model) &
            (df["fuel_type"].astype(str).str.strip().str.lower() == fuel) &
            (df["transmission_type"].astype(str).str.strip().str.lower() == trans)
        )

        return bool(mask.any())

    # ==========================================================
    # Normal Single Prediction
    # ==========================================================

    @classmethod
    def predict(cls, car_data: dict):
        """
        Predict car price from user input using the trained XGBoost model.

        Returns:
            dict:
                success
                predicted_price
                price_range
                currency
                prediction_mode ("xgboost" or "xgboost_fallback")
                message (informational notice if fallback mode is used)
        """

        # -----------------------------------------------------
        # Determine prediction mode (exact match vs fallback)
        # -----------------------------------------------------
        is_exact = cls.is_exact_dataset_match(car_data)
        prediction_mode = "xgboost" if is_exact else "xgboost_fallback"

        message = None
        if not is_exact:
            message = (
                "Prediction confidence may be lower because this vehicle configuration "
                "is not sufficiently represented in the training data. "
                "Providing complete and accurate vehicle details can improve the estimate."
            )

        # -----------------------------------------------------
        # Convert input dictionary into DataFrame
        # -----------------------------------------------------

        df = pd.DataFrame([car_data])

        # -----------------------------------------------------
        # Apply robust feature engineering
        # -----------------------------------------------------

        encoded_df, _ = engineer_features(
            df,
            freq_map=loader.freq_map,
            reference_columns=loader.reference_columns
        )

        # -----------------------------------------------------
        # Predict price using CURRENT XGBoost model
        # (convert from log1p scale)
        # -----------------------------------------------------

        raw_pred = loader.model.predict(
            encoded_df
        )[0]

        predicted_price = round(
            float(np.expm1(raw_pred)),
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
            "currency": "INR",
            "prediction_mode": prediction_mode,
            "message": message
        }

    # ==========================================================
    # Multiple Prediction Options
    # ==========================================================

    @staticmethod
    def predict_options(
        car_data: dict,
        combinations: list
    ):
        """
        Generate predictions for valid
        Engine + Max Power + Seats combinations.
        """
        from backend.services.dropdown_service import dropdown_service

        if not combinations:
            combinations = dropdown_service.get_vehicle_spec_combinations(
                car_data.get("brand"),
                car_data.get("model")
            )

        results = []

        # ======================================================
        # Generate prediction for every valid combination
        # ======================================================

        for combination in combinations:

            option_data = car_data.copy()
            option_data["engine"] = combination.get("engine")
            option_data["max_power"] = combination.get("max_power")
            option_data["seats"] = combination.get("seats")

            df = pd.DataFrame([option_data])

            encoded_df, _ = engineer_features(
                df,
                freq_map=loader.freq_map,
                reference_columns=loader.reference_columns
            )

            raw_pred = loader.model.predict(
                encoded_df
            )[0]

            predicted_price = round(
                float(np.expm1(raw_pred)),
                2
            )

            results.append(
                {
                    "engine": combination.get("engine"),
                    "max_power": combination.get("max_power"),
                    "seats": combination.get("seats"),
                    "predicted_price": predicted_price
                }
            )

        # Sort highest price first
        results.sort(
            key=lambda item: item["predicted_price"],
            reverse=True
        )

        return {
            "success": True,
            "count": len(results),
            "options": results,
            "currency": "INR"
        }