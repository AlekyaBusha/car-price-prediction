"""
backend/services/variant_prediction_service.py

Generates predicted prices for all variants of a selected
brand and model.
"""

from pathlib import Path
import json
import joblib
import pandas as pd

from backend.ml.variant_feature_engineering import (
    engineer_variant_features
)


class VariantPredictionService:

    # ======================================================
    # Paths
    # ======================================================

    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    DATA_PATH = (
        PROJECT_ROOT
        / "backend"
        / "data"
        / "processed"
        / "car_price_variant_training.csv"
    )

    MODEL_PATH = (
        PROJECT_ROOT
        / "backend"
        / "models"
        / "variant_xgb_model.pkl"
    )

    REFERENCE_COLUMNS_PATH = (
        PROJECT_ROOT
        / "backend"
        / "models"
        / "variant_reference_columns.json"
    )

    # ======================================================
    # Load model and dataset
    # ======================================================

    df = pd.read_csv(DATA_PATH)

    model = joblib.load(MODEL_PATH)

    with open(
        REFERENCE_COLUMNS_PATH,
        "r"
    ) as file:

        reference_columns = json.load(file)

    # ======================================================
    # Get model data
    # ======================================================

    @classmethod
    def get_model_data(
        cls,
        brand,
        model
    ):

        df = cls.df[
            (cls.df["brand"].astype(str).str.lower() == str(brand).lower())
            &
            (cls.df["model"].astype(str).str.lower() == str(model).lower())
        ].copy()

        return df

    # ======================================================
    # Get variant specifications
    # ======================================================

    @classmethod
    def get_variant_specifications(
        cls,
        df
    ):

        results = []

        # --------------------------------------------------
        # Group by variant
        # --------------------------------------------------

        for variant_name, group in df.groupby(
            "variant",
            dropna=False
        ):

            # Ignore unknown variants
            if str(variant_name).lower() == "unknown":
                continue

            # ------------------------------------------------
            # Most common categorical values
            # ------------------------------------------------

            fuel_type = (
                group["fuel_type"]
                .dropna()
                .mode()
            )

            transmission_type = (
                group["transmission_type"]
                .dropna()
                .mode()
            )

            engine_type = (
                group["engine_type"]
                .dropna()
                .mode()
            )

            seats = (
                group["seats"]
                .dropna()
                .mode()
            )

            # ------------------------------------------------
            # Median numerical specification
            # ------------------------------------------------

            max_power = pd.to_numeric(
                group["max_power"],
                errors="coerce"
            ).median()

            # ------------------------------------------------
            # Skip incomplete variants
            # ------------------------------------------------

            if fuel_type.empty:
                fuel = "unknown"
            else:
                fuel = str(fuel_type.iloc[0])

            if transmission_type.empty:
                transmission = "unknown"
            else:
                transmission = str(
                    transmission_type.iloc[0]
                )

            if engine_type.empty:
                engine = "unknown"
            else:
                engine = str(
                    engine_type.iloc[0]
                )

            if seats.empty:
                seat_count = 5
            else:
                seat_count = float(
                    seats.iloc[0]
                )

            if pd.isna(max_power):
                max_power = 0
            else:
                max_power = float(max_power)

            results.append(
                {
                    "variant": str(variant_name),

                    "fuel_type": fuel,

                    "transmission_type": transmission,

                    "engine_type": engine,

                    "seats": seat_count,

                    "max_power": max_power,
                }
            )

        return results

    # ======================================================
    # Predict all variants
    # ======================================================

    @classmethod
    def predict_variants(
        cls,
        brand,
        model,
        vehicle_age,
        km_driven,
        mileage=5,
        engine=None,
        seats=None,
    ):

        # --------------------------------------------------
        # Find selected model
        # --------------------------------------------------

        model_df = cls.get_model_data(
            brand,
            model
        )

        if model_df.empty:

            return {
                "success": False,
                "message": (
                    f"No data found for "
                    f"{brand} {model}"
                ),
                "variants": []
            }

        # --------------------------------------------------
        # Apply optional filters: engine (displacement) and seats
        # If engine is provided (in CC), filter by approximate
        # liter displacement contained in engine_type strings.
        # If seats is provided, filter by seats numeric value.
        # --------------------------------------------------

        if engine is not None:

            try:

                liters = round(float(engine) / 1000.0, 1)

                liters_str = str(liters)

                model_df = model_df[
                    model_df["engine_type"].astype(str).str.lower().str.contains(liters_str)
                ].copy()

            except Exception:

                # If parsing fails, leave unfiltered
                pass

        if seats is not None:

            try:

                seats_val = float(seats)

                model_df = model_df[
                    pd.to_numeric(model_df["seats"], errors="coerce") == seats_val
                ].copy()

            except Exception:

                # If parsing fails, leave unfiltered
                pass

        if model_df.empty:

            return {
                "success": False,
                "message": (
                    f"No data found for "
                    f"{brand} {model}"
                ),
                "variants": []
            }

        # --------------------------------------------------
        # Get variants
        # --------------------------------------------------

        variants = cls.get_variant_specifications(
            model_df
        )

        if not variants:

            return {
                "success": False,
                "message": (
                    "No variants available "
                    "for this model."
                ),
                "variants": []
            }

        results = []

        # --------------------------------------------------
        # Predict every variant
        # --------------------------------------------------

        for variant in variants:

            input_data = {
                "brand": str(brand).lower(),

                "model": str(model).lower(),

                "variant": variant["variant"].lower(),

                "fuel_type": variant["fuel_type"],

                "transmission_type":
                    variant["transmission_type"],

                "vehicle_age": float(
                    vehicle_age
                ),

                "km_driven": float(
                    km_driven
                ),

                # Seats: use provided seats if present, otherwise use variant value
                "seats": float(
                    seats if seats is not None else variant["seats"]
                ),

                "max_power": float(
                    variant["max_power"]
                ),

                # Engine type remains the variant's engine_type (categorical)
                "engine_type": variant[
                    "engine_type"
                ],

                # Mileage is included as an input numeric feature (optional)
                "mileage": float(mileage),
            }

            # ----------------------------------------------
            # DataFrame
            # ----------------------------------------------

            df = pd.DataFrame(
                [input_data]
            )

            # ----------------------------------------------
            # Feature engineering
            # ----------------------------------------------

            encoded_df, _ = (
                engineer_variant_features(
                    df,
                    reference_columns=cls.reference_columns
                )
            )

            # ----------------------------------------------
            # Prediction
            # ----------------------------------------------

            predicted_price = cls.model.predict(
                encoded_df
            )[0]

            predicted_price = round(
                float(predicted_price),
                2
            )

            # ----------------------------------------------
            # Result
            # ----------------------------------------------

            results.append(
                {
                    "variant": variant["variant"],

                    "fuel_type":
                        variant["fuel_type"],

                    "transmission_type":
                        variant["transmission_type"],

                    "engine_type":
                        variant["engine_type"],

                    "seats":
                        (seats if seats is not None else variant["seats"]),

                    "max_power":
                        variant["max_power"],

                    "predicted_price":
                        predicted_price,
                }
            )

        # --------------------------------------------------
        # Sort highest price first
        # --------------------------------------------------

        results.sort(
            key=lambda item:
                item["predicted_price"],
            reverse=True
        )

        return {
            "success": True,

            "brand": brand,

            "model": model,

            "vehicle_age": vehicle_age,

            "km_driven": km_driven,

            "mileage": mileage,

            "count": len(results),

            "variants": results,

            "currency": "INR",
        }
