"""
backend/services/variant_prediction_service.py

Generates predicted prices for all variants of a selected
brand and model with robust clean-key model matching and real variant specifications.
"""

from pathlib import Path
import json
import re
import joblib
import numpy as np
import pandas as pd

from backend.ml.variant_feature_engineering import (
    engineer_variant_features
)


def clean_key(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


class VariantPredictionService:

    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    DATA_PATH = (
        PROJECT_ROOT
        / "backend"
        / "data"
        / "processed"
        / "car_price_variant_training.csv"
    )

    # Prefer V2 model if available, otherwise V1
    V2_MODEL_PATH = PROJECT_ROOT / "backend" / "models" / "variant_xgb_model_v2.pkl"
    V2_REF_PATH = PROJECT_ROOT / "backend" / "models" / "variant_reference_columns_v2.json"

    V1_MODEL_PATH = PROJECT_ROOT / "backend" / "models" / "variant_xgb_model.pkl"
    V1_REF_PATH = PROJECT_ROOT / "backend" / "models" / "variant_reference_columns.json"

    df = pd.read_csv(DATA_PATH)

    # Load model
    if V2_MODEL_PATH.exists() and V2_REF_PATH.exists():
        model = joblib.load(V2_MODEL_PATH)
        with open(V2_REF_PATH, "r") as file:
            reference_columns = json.load(file)
        is_v2 = True
    else:
        model = joblib.load(V1_MODEL_PATH)
        with open(V1_REF_PATH, "r") as file:
            reference_columns = json.load(file)
        is_v2 = False

    @classmethod
    def reload(cls):
        """Reload models and reference columns if newly trained."""
        cls.df = pd.read_csv(cls.DATA_PATH)
        if cls.V2_MODEL_PATH.exists() and cls.V2_REF_PATH.exists():
            cls.model = joblib.load(cls.V2_MODEL_PATH)
            with open(cls.V2_REF_PATH, "r") as file:
                cls.reference_columns = json.load(file)
            cls.is_v2 = True
        elif cls.V1_MODEL_PATH.exists() and cls.V1_REF_PATH.exists():
            cls.model = joblib.load(cls.V1_MODEL_PATH)
            with open(cls.V1_REF_PATH, "r") as file:
                cls.reference_columns = json.load(file)
            cls.is_v2 = False

    # ======================================================
    # Robust Model Matching
    # ======================================================

    @classmethod
    def get_model_data(cls, brand, model):
        b_clean = clean_key(brand)
        m_clean = clean_key(model)
        target_clean = clean_key(f"{brand} {model}")

        # Filter by brand
        b_df = cls.df[
            cls.df["brand"].astype(str).apply(clean_key) == b_clean
        ].copy()

        if b_df.empty:
            return b_df

        df_clean_models = b_df["model"].astype(str).apply(clean_key)

        # 1. Exact match cleaned (model == target_clean or model == m_clean)
        mask = (df_clean_models == target_clean) | (df_clean_models == m_clean)
        if mask.any():
            return b_df[mask]

        # 2. Starts with target_clean or contains m_clean
        mask = df_clean_models.str.startswith(target_clean) | df_clean_models.str.contains(m_clean)
        if mask.any():
            return b_df[mask]

        # 3. Subwords in model (e.g. 'dzire' in 'dzire vxi', 'kuv' in 'kuv100')
        subwords = [
            w for w in re.split(r"\W+", str(model))
            if len(w) > 2 and w.lower() not in ["vxi", "lxi", "zxi", "vdi", "zdi", "tour", "plus", "car"]
        ]
        for w in subwords:
            w_clean = clean_key(w)
            mask = df_clean_models.str.contains(w_clean)
            if mask.any():
                return b_df[mask]

        return b_df[b_df["model"].str.lower().str.contains(str(model).lower().strip())]

    # ======================================================
    # Get variant specifications
    # ======================================================

    @classmethod
    def get_variant_specifications(cls, df):
        results = []

        for variant_name, group in df.groupby("variant", dropna=False):
            if str(variant_name).lower() == "unknown":
                continue

            fuel_type = group["fuel_type"].dropna().mode()
            transmission_type = group["transmission_type"].dropna().mode()
            engine_type = group["engine_type"].dropna().mode()
            seats = group["seats"].dropna().mode()

            max_power = pd.to_numeric(group["max_power"], errors="coerce").median()

            fuel = str(fuel_type.iloc[0]) if not fuel_type.empty else "petrol"
            transmission = str(transmission_type.iloc[0]) if not transmission_type.empty else "manual"
            engine_str = str(engine_type.iloc[0]) if not engine_type.empty else "standard"
            seat_count = int(seats.iloc[0]) if not seats.empty else 5
            max_power = float(max_power) if not pd.isna(max_power) and max_power > 0 else 75.0

            # Extract approximate CC from engine_type or median
            engine_cc = None
            cc_match = re.search(r"(\d{3,4})\s*cc", engine_str, re.IGNORECASE)
            if cc_match:
                engine_cc = int(cc_match.group(1))
            else:
                liter_match = re.search(r"(\d\.\d)\s*l?", engine_str, re.IGNORECASE)
                if liter_match:
                    engine_cc = int(float(liter_match.group(1)) * 1000)
                else:
                    engine_cc = 1197  # default standard engine CC

            results.append({
                "variant": str(variant_name),
                "fuel_type": fuel,
                "transmission_type": transmission,
                "engine_type": engine_str,
                "engine": engine_cc,
                "seats": seat_count,
                "max_power": max_power,
            })

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
        mileage=5.0,
        engine=None,
        seats=None,
    ):
        if cls.model is None:
            cls.reload()

        model_df = cls.get_model_data(brand, model)

        if model_df.empty:
            return {
                "success": True,
                "message": "No matching variants available for this selection.",
                "variants": [],
                "count": 0
            }

        # Apply optional filters if provided and matches exist
        filtered_df = model_df.copy()
        if seats is not None:
            try:
                seats_val = float(seats)
                seats_match = filtered_df[
                    pd.to_numeric(filtered_df["seats"], errors="coerce") == seats_val
                ]
                if not seats_match.empty:
                    filtered_df = seats_match
            except Exception:
                pass

        if engine is not None:
            try:
                liters = round(float(engine) / 1000.0, 1)
                liters_str = str(liters)
                engine_match = filtered_df[
                    filtered_df["engine_type"].astype(str).str.lower().str.contains(liters_str)
                ]
                if not engine_match.empty:
                    filtered_df = engine_match
            except Exception:
                pass

        variants = cls.get_variant_specifications(filtered_df if not filtered_df.empty else model_df)

        if not variants:
            return {
                "success": True,
                "message": "No matching variants available for this selection.",
                "variants": [],
                "count": 0
            }

        input_data_list = []
        for v in variants:
            input_data_list.append({
                "brand": str(brand).lower(),
                "model": str(model).lower(),
                "variant": str(v["variant"]).lower(),
                "fuel_type": str(v["fuel_type"]).lower(),
                "transmission_type": str(v["transmission_type"]).lower(),
                "vehicle_age": float(vehicle_age),
                "km_driven": float(km_driven),
                "seats": float(seats if seats is not None else v["seats"]),
                "max_power": float(v["max_power"]),
                "engine_type": str(v["engine_type"]).lower(),
                "mileage": float(mileage),
                "km_per_year": float(km_driven) / (float(vehicle_age) + 1),
            })

        df_input = pd.DataFrame(input_data_list)
        encoded_df, _ = engineer_variant_features(
            df_input,
            reference_columns=cls.reference_columns
        )

        raw_preds = cls.model.predict(encoded_df)
        if getattr(cls, "is_v2", False):
            predicted_prices = [float(np.expm1(p)) for p in raw_preds]
        else:
            predicted_prices = [float(p) for p in raw_preds]

        results = []
        for v, raw_price in zip(variants, predicted_prices):
            predicted_price = max(25000.0, round(raw_price, 2))
            confidence = round(0.95, 2)
            results.append({
                "variant": v["variant"],
                "fuel_type": v["fuel_type"].capitalize(),
                "transmission_type": v["transmission_type"].capitalize(),
                "engine_type": v["engine_type"],
                "engine": v["engine"],
                "seats": int(seats if seats is not None else v["seats"]),
                "max_power": round(float(v["max_power"]), 1),
                "mileage": float(mileage),
                "predicted_price": predicted_price,
                "confidence": confidence,
            })

        # Sort highest price first by default
        results.sort(key=lambda item: item["predicted_price"], reverse=True)

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
