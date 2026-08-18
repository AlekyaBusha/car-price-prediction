"""
backend/ml/evaluate_model.py

Evaluates the production XGBoost model (xgb_model.pkl) and Variant XGBoost model (variant_xgb_model_v2.pkl) on untouched test sets.
Calculates and prints exact MAE, RMSE, R2, MedAE, and MAPE.
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
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score, median_absolute_error

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = PROJECT_ROOT / "backend" / "models"
sys.path.append(str(PROJECT_ROOT))
from backend.ml.feature_engineering import engineer_features


def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    non_zero = y_true != 0
    return float(np.mean(np.abs((y_true[non_zero] - y_pred[non_zero]) / y_true[non_zero])) * 100)


def evaluate_production_model():
    print("=" * 70)
    print("PRODUCTION XGBOOST MODEL EVALUATION (xgb_model.pkl)")
    print("=" * 70)

    data_path = PROJECT_ROOT / "backend" / "data" / "processed" / "cleaned_car_data.csv"
    df = pd.read_csv(data_path)

    model_path = MODELS_DIR / "xgb_model.pkl"
    ref_path = MODELS_DIR / "reference_columns.json"
    freq_path = MODELS_DIR / "model_freq_map.json"

    if not model_path.exists() or not ref_path.exists() or not freq_path.exists():
        print("Production XGBoost artifacts not found.")
        return {}

    model = joblib.load(model_path)
    with open(ref_path) as f:
        ref_cols = json.load(f)
    with open(freq_path) as f:
        freq_map = json.load(f)

    train_df, test_df = train_test_split(df, test_size=0.20, random_state=42)

    X_test, _ = engineer_features(
        test_df,
        freq_map=freq_map,
        reference_columns=ref_cols
    )
    y_test = test_df["selling_price"]

    raw_preds = model.predict(X_test)
    preds = np.expm1(raw_preds)

    metrics = {
        "MAE": float(mean_absolute_error(y_test, preds)),
        "RMSE": float(root_mean_squared_error(y_test, preds)),
        "R2": float(r2_score(y_test, preds)),
        "MedAE": float(median_absolute_error(y_test, preds)),
        "MAPE": float(mean_absolute_percentage_error(y_test, preds)),
    }

    print(f"Dataset Records: {len(df):,} (Train: {len(train_df):,}, Test: {len(test_df):,})")
    print(f"Feature Count  : {len(ref_cols)} columns")
    print(f"MAE            : ₹{metrics['MAE']:,.2f}")
    print(f"RMSE           : ₹{metrics['RMSE']:,.2f}")
    print(f"R² Score       : {metrics['R2']:.6f} ({metrics['R2']*100:.2f}%)")
    print(f"Median AE      : ₹{metrics['MedAE']:,.2f}")
    print(f"MAPE           : {metrics['MAPE']:.2f}%")
    print("=" * 70)

    return metrics


def evaluate_variant_models():
    print("\n" + "=" * 70)
    print("VARIANT XGBOOST MODEL EVALUATION (variant_xgb_model_v2.pkl)")
    print("=" * 70)

    data_path = PROJECT_ROOT / "backend" / "data" / "processed" / "car_price_variant_training.csv"
    if not data_path.exists():
        print(f"Variant dataset not found at {data_path}")
        return {}

    df = pd.read_csv(data_path)
    v2_model_path = MODELS_DIR / "variant_xgb_model_v2.pkl"
    v2_ref_path = MODELS_DIR / "variant_reference_columns_v2.json"

    if not v2_model_path.exists() or not v2_ref_path.exists():
        print("Variant V2 model artifacts not found.")
        return {}

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
        "MedAE": float(median_absolute_error(y_test, preds_v2)),
        "MAPE": float(mean_absolute_percentage_error(y_test, preds_v2)),
    }

    print(f"Dataset Records: {len(df):,} (Train: {len(X_train_v2):,}, Test: {len(X_test_v2):,})")
    print(f"MAE            : ₹{v2_metrics['MAE']:,.2f}")
    print(f"RMSE           : ₹{v2_metrics['RMSE']:,.2f}")
    print(f"R² Score       : {v2_metrics['R2']:.6f} ({v2_metrics['R2']*100:.2f}%)")
    print(f"Median AE      : ₹{v2_metrics['MedAE']:,.2f}")
    print(f"MAPE           : {v2_metrics['MAPE']:.2f}%")
    print("=" * 70)

    return v2_metrics


if __name__ == "__main__":
    evaluate_production_model()
    evaluate_variant_models()
