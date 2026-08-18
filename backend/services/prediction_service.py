"""
backend/services/prediction_service.py

Handles car price prediction and fair price range calculation.
"""

import numpy as np
import pandas as pd

from backend.ml.feature_engineering import engineer_features
from backend.ml.model_loader import loader
from backend.ml.price_range import get_price_range


class PredictionService:

    # ==========================================================
    # Normal Single Prediction
    # ==========================================================

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
        # Predict price (convert from log1p scale)
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
            "currency": "INR"
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

        Each combination comes from the actual dataset.
        """

        results = []

        # ======================================================
        # Generate prediction for every valid combination
        # ======================================================

        for combination in combinations:

            # --------------------------------------------------
            # Copy original user input
            # --------------------------------------------------

            option_data = car_data.copy()

            # --------------------------------------------------
            # Set Engine, Max Power and Seats
            # --------------------------------------------------

            option_data["engine"] = combination["engine"]

            option_data["max_power"] = combination["max_power"]

            option_data["seats"] = combination["seats"]

            # --------------------------------------------------
            # Convert numeric values
            # --------------------------------------------------

            option_data["engine"] = float(
                option_data["engine"]
            )

            option_data["max_power"] = float(
                option_data["max_power"]
            )

            option_data["seats"] = float(
                option_data["seats"]
            )

            # --------------------------------------------------
            # Convert input into DataFrame
            # --------------------------------------------------

            df = pd.DataFrame(
                [option_data]
            )

            # --------------------------------------------------
            # Apply the SAME feature engineering
            # used by the normal prediction
            # --------------------------------------------------

            encoded_df, _ = engineer_features(
                df,
                freq_map=loader.freq_map,
                reference_columns=loader.reference_columns
            )

            # --------------------------------------------------
            # Ensure numeric columns are numeric
            # --------------------------------------------------

            for column in [
                "engine",
                "max_power",
                "seats"
            ]:

                if column in encoded_df.columns:

                    encoded_df[column] = pd.to_numeric(
                        encoded_df[column],
                        errors="coerce"
                    )

            # --------------------------------------------------
            # Check for invalid numeric values
            # --------------------------------------------------

            numeric_columns = [
                column
                for column in [
                    "engine",
                    "max_power",
                    "seats"
                ]
                if column in encoded_df.columns
            ]

            if encoded_df[
                numeric_columns
            ].isnull().any().any():

                raise ValueError(
                    "Invalid numeric values found in "
                    "engine, max_power, or seats."
                )

            # --------------------------------------------------
            # Predict price (convert from log1p scale)
            # --------------------------------------------------

            raw_pred = loader.model.predict(
                encoded_df
            )[0]

            predicted_price = round(
                float(np.expm1(raw_pred)),
                2
            )

            # --------------------------------------------------
            # Store prediction
            # --------------------------------------------------

            results.append(
                {
                    "engine": combination["engine"],
                    "max_power": combination["max_power"],
                    "seats": combination["seats"],
                    "predicted_price": predicted_price
                }
            )

        # ======================================================
        # Sort results
        # Highest predicted price first
        # ======================================================

        results.sort(
            key=lambda item: item["predicted_price"],
            reverse=True
        )

        # ======================================================
        # Return response
        # ======================================================

        return {
            "success": True,
            "count": len(results),
            "options": results,
            "currency": "INR"
        }