"""
backend/ml/evaluate_model.py

Evaluates and compares V1 vs V2 models on untouched test sets.
Calculates and prints exact MAE, RMSE, R2, and MAPE.
"""

import sys

# Set UTF-8 encoding for standard streams
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = PROJECT_ROOT / "backend" / "models"

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    non_zero = y_true != 0
    return float(np.mean(np.abs((y_true[non_zero] - y_pred[non_zero]) / y_true[non_zero])) * 100)

def evaluate_unified_models():
    print("=" * 70)
    print("UNIFIED MODEL EVALUATION (V1 vs V2)")
    print("=" * 70)

    data_path = PROJECT_ROOT / "backend" / "data" / "processed" / "unified_car_price_dataset.csv"
    df = pd.read_csv(data_path)

    # 1. Evaluate V1
    v1_model_path = MODELS_DIR / "unified_xgb_model.pkl"
    v1_ref_path = MODELS_DIR / "unified_reference_columns.json"

    v1_metrics = {}
    if v1_model_path.exists() and v1_ref_path.exists():
        v1_model = joblib.load(v1_model_path)
        with open(v1_ref_path) as f:
            v1_ref_cols = json.load(f)

        cat_cols = ["brand", "model", "variant", "fuel_type", "transmission_type", "engine_type"]
        df_v1 = df.copy()
        for col in cat_cols:
            df_v1[col] = df_v1[col].fillna("unknown").astype(str).str.strip().str.lower()
        num_cols = ["vehicle_age", "km_driven", "seats", "max_power"]
        for col in num_cols:
            df_v1[col] = pd.to_numeric(df_v1[col], errors="coerce").fillna(0)

        X_v1 = pd.get_dummies(df_v1[cat_cols + num_cols], columns=cat_cols, drop_first=False)
        bool_cols = X_v1.select_dtypes(include="bool").columns
        X_v1[bool_cols] = X_v1[bool_cols].astype(int)
        X_v1 = X_v1.reindex(columns=v1_ref_cols, fill_value=0).fillna(0)
        y = df["selling_price"]

        X_train_v1, X_test_v1, y_train, y_test = train_test_split(X_v1, y, test_size=0.2, random_state=42)
        preds_v1 = v1_model.predict(X_test_v1)
        preds_v1 = np.clip(preds_v1, a_min=10000, a_max=None)

        v1_metrics = {
            "MAE": float(mean_absolute_error(y_test, preds_v1)),
            "RMSE": float(root_mean_squared_error(y_test, preds_v1)),
            "R2": float(r2_score(y_test, preds_v1)),
            "MAPE": float(mean_absolute_percentage_error(y_test, preds_v1)),
        }

    # 2. Evaluate V2
    v2_model_path = MODELS_DIR / "unified_xgb_model_v2.pkl"
    v2_ref_path = MODELS_DIR / "unified_reference_columns_v2.json"

    v2_metrics = {}
    if v2_model_path.exists() and v2_ref_path.exists():
        v2_model = joblib.load(v2_model_path)
        with open(v2_ref_path) as f:
            v2_ref_cols = json.load(f)

        df_v2 = df.copy()
        cat_cols = ["brand", "model", "variant", "fuel_type", "transmission_type", "engine_type"]
        for col in cat_cols:
            df_v2[col] = df_v2[col].fillna("unknown").astype(str).str.strip().str.lower()
        num_cols = ["vehicle_age", "km_driven", "seats", "max_power"]
        for col in num_cols:
            df_v2[col] = pd.to_numeric(df_v2[col], errors="coerce").fillna(0)
        df_v2["km_per_year"] = df_v2["km_driven"] / (df_v2["vehicle_age"] + 1)
        num_cols.append("km_per_year")

        X_v2 = pd.get_dummies(df_v2[cat_cols + num_cols], columns=cat_cols, drop_first=False)
        bool_cols = X_v2.select_dtypes(include="bool").columns
        X_v2[bool_cols] = X_v2[bool_cols].astype(int)
        X_v2 = X_v2.reindex(columns=v2_ref_cols, fill_value=0).fillna(0)
        y = df["selling_price"]

        X_train_v2, X_test_v2, y_train, y_test = train_test_split(X_v2, y, test_size=0.2, random_state=42)
        preds_log_v2 = v2_model.predict(X_test_v2)
        preds_v2 = np.expm1(preds_log_v2)
        preds_v2 = np.clip(preds_v2, a_min=10000, a_max=None)

        v2_metrics = {
            "MAE": float(mean_absolute_error(y_test, preds_v2)),
            "RMSE": float(root_mean_squared_error(y_test, preds_v2)),
            "R2": float(r2_score(y_test, preds_v2)),
            "MAPE": float(mean_absolute_percentage_error(y_test, preds_v2)),
        }

    print("UNIFIED MODEL\n")
    print("V1")
    if v1_metrics:
        print(f"MAE = ₹{v1_metrics['MAE']:,.2f}")
        print(f"RMSE = ₹{v1_metrics['RMSE']:,.2f}")
        print(f"R² = {v1_metrics['R2']:.6f}")
        print(f"MAPE = {v1_metrics['MAPE']:.2f}%")
    else:
        print("V1 model artifacts not found.")

    print("\nV2")
    if v2_metrics:
        print(f"MAE = ₹{v2_metrics['MAE']:,.2f}")
        print(f"RMSE = ₹{v2_metrics['RMSE']:,.2f}")
        print(f"R² = {v2_metrics['R2']:.6f}")
        print(f"MAPE = {v2_metrics['MAPE']:.2f}%")
    else:
        print("V2 model artifacts not found.")

    return v1_metrics, v2_metrics


def evaluate_variant_models():
    print("\n" + "=" * 70)
    print("VARIANT MODEL EVALUATION (V1 vs V2)")
    print("=" * 70)

    data_path = PROJECT_ROOT / "backend" / "data" / "processed" / "car_price_variant_training.csv"
    df = pd.read_csv(data_path)

    # 1. Evaluate Variant V1
    v1_model_path = MODELS_DIR / "variant_xgb_model.pkl"
    v1_ref_path = MODELS_DIR / "variant_reference_columns.json"

    v1_metrics = {}
    if v1_model_path.exists() and v1_ref_path.exists():
        v1_model = joblib.load(v1_model_path)
        with open(v1_ref_path) as f:
            v1_ref_cols = json.load(f)

        cat_cols = ["brand", "model", "variant", "fuel_type", "transmission_type", "engine_type"]
        df_v1 = df.copy()
        for col in cat_cols:
            df_v1[col] = df_v1[col].fillna("unknown").astype(str).str.strip().str.lower()
        num_cols = ["vehicle_age", "km_driven", "seats", "max_power"]
        for col in num_cols:
            df_v1[col] = pd.to_numeric(df_v1[col], errors="coerce").fillna(0)

        X_v1 = pd.get_dummies(df_v1[cat_cols + num_cols], columns=cat_cols, drop_first=False)
        bool_cols = X_v1.select_dtypes(include="bool").columns
        X_v1[bool_cols] = X_v1[bool_cols].astype(int)
        X_v1 = X_v1.reindex(columns=v1_ref_cols, fill_value=0).fillna(0)
        y = df["selling_price"]

        X_train_v1, X_test_v1, y_train, y_test = train_test_split(X_v1, y, test_size=0.2, random_state=42)
        preds_v1 = v1_model.predict(X_test_v1)
        preds_v1 = np.clip(preds_v1, a_min=10000, a_max=None)

        v1_metrics = {
            "MAE": float(mean_absolute_error(y_test, preds_v1)),
            "RMSE": float(root_mean_squared_error(y_test, preds_v1)),
            "R2": float(r2_score(y_test, preds_v1)),
            "MAPE": float(mean_absolute_percentage_error(y_test, preds_v1)),
        }

    # 2. Evaluate Variant V2
    v2_model_path = MODELS_DIR / "variant_xgb_model_v2.pkl"
    v2_ref_path = MODELS_DIR / "variant_reference_columns_v2.json"

    v2_metrics = {}
    if v2_model_path.exists() and v2_ref_path.exists():
        v2_model = joblib.load(v2_model_path)
        with open(v2_ref_path) as f:
            v2_ref_cols = json.load(f)

        df_v2 = df.copy()
        cat_cols = ["brand", "model", "variant", "fuel_type", "transmission_type", "engine_type"]
        for col in cat_cols:
            df_v2[col] = df_v2[col].fillna("unknown").astype(str).str.strip().str.lower()
        num_cols = ["vehicle_age", "km_driven", "seats", "max_power"]
        for col in num_cols:
            df_v2[col] = pd.to_numeric(df_v2[col], errors="coerce").fillna(0)
        df_v2["km_per_year"] = df_v2["km_driven"] / (df_v2["vehicle_age"] + 1)
        num_cols.append("km_per_year")

        X_v2 = pd.get_dummies(df_v2[cat_cols + num_cols], columns=cat_cols, drop_first=False)
        bool_cols = X_v2.select_dtypes(include="bool").columns
        X_v2[bool_cols] = X_v2[bool_cols].astype(int)
        X_v2 = X_v2.reindex(columns=v2_ref_cols, fill_value=0).fillna(0)
        y = df["selling_price"]

        X_train_v2, X_test_v2, y_train, y_test = train_test_split(X_v2, y, test_size=0.2, random_state=42)
        preds_log_v2 = v2_model.predict(X_test_v2)
        preds_v2 = np.expm1(preds_log_v2)
        preds_v2 = np.clip(preds_v2, a_min=10000, a_max=None)

        v2_metrics = {
            "MAE": float(mean_absolute_error(y_test, preds_v2)),
            "RMSE": float(root_mean_squared_error(y_test, preds_v2)),
            "R2": float(r2_score(y_test, preds_v2)),
            "MAPE": float(mean_absolute_percentage_error(y_test, preds_v2)),
        }

    print("VARIANT MODEL\n")
    print("V1")
    if v1_metrics:
        print(f"MAE = ₹{v1_metrics['MAE']:,.2f}")
        print(f"RMSE = ₹{v1_metrics['RMSE']:,.2f}")
        print(f"R² = {v1_metrics['R2']:.6f}")
        print(f"MAPE = {v1_metrics['MAPE']:.2f}%")
    else:
        print("Variant V1 model artifacts not found.")

    print("\nV2")
    if v2_metrics:
        print(f"MAE = ₹{v2_metrics['MAE']:,.2f}")
        print(f"RMSE = ₹{v2_metrics['RMSE']:,.2f}")
        print(f"R² = {v2_metrics['R2']:.6f}")
        print(f"MAPE = {v2_metrics['MAPE']:.2f}%")
    else:
        print("Variant V2 model artifacts not found.")

    return v1_metrics, v2_metrics


if __name__ == "__main__":
    evaluate_unified_models()
    evaluate_variant_models()
