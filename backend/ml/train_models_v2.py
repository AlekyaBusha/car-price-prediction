"""
backend/ml/train_models_v2.py

Trains V2 models for Unified Prediction and Variant Prediction.
Calculates honest test metrics (MAE, RMSE, R2, MAPE) on an untouched 20% holdout test set.
Saves:
- backend/models/unified_xgb_model_v2.pkl
- backend/models/unified_reference_columns_v2.json
- backend/models/unified_model_metrics_v2.json
- backend/models/variant_xgb_model_v2.pkl
- backend/models/variant_reference_columns_v2.json
- backend/models/variant_model_metrics_v2.json
"""

import sys
import os

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
from xgboost import XGBRegressor

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = PROJECT_ROOT / "backend" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    non_zero = y_true != 0
    return float(np.mean(np.abs((y_true[non_zero] - y_pred[non_zero]) / y_true[non_zero])) * 100)

def train_unified_v2():
    print("\n" + "=" * 70)
    print("TRAINING UNIFIED MODEL V2")
    print("=" * 70)

    data_path = PROJECT_ROOT / "backend" / "data" / "processed" / "unified_car_price_dataset.csv"
    df = pd.read_csv(data_path)
    print(f"Dataset shape: {df.shape}")

    # Feature Engineering
    df = df.copy()
    if "year" in df.columns:
        df = df.drop(columns=["year"])

    cat_cols = ["brand", "model", "variant", "fuel_type", "transmission_type", "engine_type"]
    for col in cat_cols:
        if col not in df.columns:
            df[col] = "unknown"
        df[col] = df[col].fillna("unknown").astype(str).str.strip().str.lower()

    num_cols = ["vehicle_age", "km_driven", "seats", "max_power"]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["km_per_year"] = df["km_driven"] / (df["vehicle_age"] + 1)
    num_cols.append("km_per_year")

    # One-hot encoding
    X_raw = df[cat_cols + num_cols]
    y = df["selling_price"]

    X_encoded = pd.get_dummies(X_raw, columns=cat_cols, drop_first=False)
    bool_cols = X_encoded.select_dtypes(include="bool").columns
    X_encoded[bool_cols] = X_encoded[bool_cols].astype(int)
    X_encoded = X_encoded.fillna(0)

    reference_columns = X_encoded.columns.tolist()
    print(f"Total features: {len(reference_columns)}")

    # Split 80/20 with random_state=42
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.20, random_state=42
    )

    y_train_log = np.log1p(y_train)

    print("Fitting XGBoost Regressor V2...")
    model_v2 = XGBRegressor(
        n_estimators=700,
        max_depth=8,
        learning_rate=0.04,
        subsample=0.85,
        colsample_bytree=0.85,
        min_child_weight=3,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
        n_jobs=-1
    )
    model_v2.fit(X_train, y_train_log)

    preds_log = model_v2.predict(X_test)
    preds = np.expm1(preds_log)
    preds = np.clip(preds, a_min=10000, a_max=None)

    mae = float(mean_absolute_error(y_test, preds))
    rmse = float(root_mean_squared_error(y_test, preds))
    r2 = float(r2_score(y_test, preds))
    mape = float(mean_absolute_percentage_error(y_test, preds))

    print("\n--- UNIFIED V2 TEST METRICS ---")
    print(f"MAE  : INR {mae:,.2f}")
    print(f"RMSE : INR {rmse:,.2f}")
    print(f"R2   : {r2:.6f}")
    print(f"MAPE : {mape:.2f}%")

    # Save artifacts
    model_path = MODELS_DIR / "unified_xgb_model_v2.pkl"
    ref_path = MODELS_DIR / "unified_reference_columns_v2.json"
    metrics_path = MODELS_DIR / "unified_model_metrics_v2.json"

    joblib.dump(model_v2, model_path)
    with open(ref_path, "w") as f:
        json.dump(reference_columns, f, indent=2)

    metrics = {
        "model": "XGBRegressor_V2",
        "dataset_rows": len(df),
        "features": len(reference_columns),
        "target_transformation": "log1p",
        "n_estimators": 700,
        "max_depth": 8,
        "learning_rate": 0.04,
        "subsample": 0.85,
        "colsample_bytree": 0.85,
        "min_child_weight": 3,
        "reg_alpha": 0.1,
        "reg_lambda": 1.0,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
        "MAPE": mape
    }
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"Saved Unified V2 artifacts to {MODELS_DIR}")
    return metrics


def train_variant_v2():
    print("\n" + "=" * 70)
    print("TRAINING VARIANT MODEL V2")
    print("=" * 70)

    data_path = PROJECT_ROOT / "backend" / "data" / "processed" / "car_price_variant_training.csv"
    df = pd.read_csv(data_path)
    print(f"Dataset shape: {df.shape}")

    df = df.copy()
    if "year" in df.columns:
        df = df.drop(columns=["year"])

    cat_cols = ["brand", "model", "variant", "fuel_type", "transmission_type", "engine_type"]
    for col in cat_cols:
        if col not in df.columns:
            df[col] = "unknown"
        df[col] = df[col].fillna("unknown").astype(str).str.strip().str.lower()

    num_cols = ["vehicle_age", "km_driven", "seats", "max_power"]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["km_per_year"] = df["km_driven"] / (df["vehicle_age"] + 1)
    num_cols.append("km_per_year")

    X_raw = df[cat_cols + num_cols]
    y = df["selling_price"]

    X_encoded = pd.get_dummies(X_raw, columns=cat_cols, drop_first=False)
    bool_cols = X_encoded.select_dtypes(include="bool").columns
    X_encoded[bool_cols] = X_encoded[bool_cols].astype(int)
    X_encoded = X_encoded.fillna(0)

    reference_columns = X_encoded.columns.tolist()
    print(f"Total features: {len(reference_columns)}")

    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.20, random_state=42
    )

    y_train_log = np.log1p(y_train)

    print("Fitting XGBoost Variant Regressor V2...")
    model_v2 = XGBRegressor(
        n_estimators=700,
        max_depth=8,
        learning_rate=0.04,
        subsample=0.85,
        colsample_bytree=0.85,
        min_child_weight=3,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
        n_jobs=-1
    )
    model_v2.fit(X_train, y_train_log)

    preds_log = model_v2.predict(X_test)
    preds = np.expm1(preds_log)
    preds = np.clip(preds, a_min=10000, a_max=None)

    mae = float(mean_absolute_error(y_test, preds))
    rmse = float(root_mean_squared_error(y_test, preds))
    r2 = float(r2_score(y_test, preds))
    mape = float(mean_absolute_percentage_error(y_test, preds))

    print("\n--- VARIANT V2 TEST METRICS ---")
    print(f"MAE  : INR {mae:,.2f}")
    print(f"RMSE : INR {rmse:,.2f}")
    print(f"R2   : {r2:.6f}")
    print(f"MAPE : {mape:.2f}%")

    model_path = MODELS_DIR / "variant_xgb_model_v2.pkl"
    ref_path = MODELS_DIR / "variant_reference_columns_v2.json"
    metrics_path = MODELS_DIR / "variant_model_metrics_v2.json"

    joblib.dump(model_v2, model_path)
    with open(ref_path, "w") as f:
        json.dump(reference_columns, f, indent=2)

    metrics = {
        "model": "XGBRegressor_Variant_V2",
        "dataset_rows": len(df),
        "features": len(reference_columns),
        "target_transformation": "log1p",
        "n_estimators": 700,
        "max_depth": 8,
        "learning_rate": 0.04,
        "subsample": 0.85,
        "colsample_bytree": 0.85,
        "min_child_weight": 3,
        "reg_alpha": 0.1,
        "reg_lambda": 1.0,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
        "MAPE": mape
    }
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"Saved Variant V2 artifacts to {MODELS_DIR}")
    return metrics


if __name__ == "__main__":
    train_unified_v2()
    train_variant_v2()
