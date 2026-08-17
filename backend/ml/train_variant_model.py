"""
Train the variant-aware XGBoost car price prediction model.

The existing production model is not modified.
"""

from pathlib import Path
import json
import joblib

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from xgboost import XGBRegressor

from backend.ml.variant_feature_engineering import (
    engineer_variant_features
)


# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "backend"
    / "data"
    / "processed"
    / "car_price_variant_training.csv"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "backend"
    / "models"
)

MODEL_PATH = (
    MODEL_DIR
    / "variant_xgb_model.pkl"
)

REFERENCE_COLUMNS_PATH = (
    MODEL_DIR
    / "variant_reference_columns.json"
)

METRICS_PATH = (
    MODEL_DIR
    / "variant_model_metrics.json"
)


# ==========================================================
# Create model directory
# ==========================================================

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# Load dataset
# ==========================================================

print("=" * 70)
print("VARIANT XGBOOST TRAINING")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")


# ==========================================================
# Target
# ==========================================================

TARGET = "selling_price"


X = df.drop(
    columns=[TARGET]
)

y = df[TARGET]


# ==========================================================
# Feature Engineering
# ==========================================================

print("\nEngineering features...")

X_encoded, reference_columns = (
    engineer_variant_features(X)
)

print(
    f"Generated features: {X_encoded.shape[1]}"
)


# ==========================================================
# Train/Test Split
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X_encoded,
    y,
    test_size=0.20,
    random_state=42
)

print("\nDataset split:")

print(
    f"Training rows: {len(X_train):,}"
)

print(
    f"Testing rows : {len(X_test):,}"
)


# ==========================================================
# XGBoost Model
# ==========================================================

print("\nTraining XGBoost...")

model = XGBRegressor(
    n_estimators=500,
    max_depth=7,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1
)


model.fit(
    X_train,
    y_train
)


# ==========================================================
# Prediction
# ==========================================================

print("\nEvaluating model...")

predictions = model.predict(
    X_test
)


# ==========================================================
# Metrics
# ==========================================================

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)


print("\n" + "=" * 70)
print("VARIANT MODEL RESULTS")
print("=" * 70)

print(
    f"MAE : ₹{mae:,.2f}"
)

print(
    f"R²  : {r2:.6f}"
)

print("=" * 70)


# ==========================================================
# Save Model
# ==========================================================

print("\nSaving model...")

joblib.dump(
    model,
    MODEL_PATH
)


# ==========================================================
# Save Reference Columns
# ==========================================================

with open(
    REFERENCE_COLUMNS_PATH,
    "w"
) as file:

    json.dump(
        reference_columns,
        file,
        indent=2
    )


# ==========================================================
# Save Metrics
# ==========================================================

metrics = {
    "model": "XGBRegressor",
    "dataset_rows": int(len(df)),
    "features": int(X_encoded.shape[1]),
    "n_estimators": 500,
    "max_depth": 7,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "MAE": float(mae),
    "R2": float(r2)
}


with open(
    METRICS_PATH,
    "w"
) as file:

    json.dump(
        metrics,
        file,
        indent=2
    )


# ==========================================================
# Complete
# ==========================================================

print("\nModel saved:")
print(MODEL_PATH)

print("\nReference columns saved:")
print(REFERENCE_COLUMNS_PATH)

print("\nMetrics saved:")
print(METRICS_PATH)

print("\nVariant model training completed.")