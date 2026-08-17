"""
Train the unified XGBoost car price prediction model.

Combines:
    1. Existing car dataset
    2. Variant-aware car dataset

The existing production model is not modified.
"""

from pathlib import Path
import json
import joblib

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from xgboost import XGBRegressor


# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "backend"
    / "data"
    / "processed"
    / "unified_car_price_dataset.csv"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "backend"
    / "models"
)

MODEL_PATH = (
    MODEL_DIR
    / "unified_xgb_model.pkl"
)

REFERENCE_COLUMNS_PATH = (
    MODEL_DIR
    / "unified_reference_columns.json"
)

METRICS_PATH = (
    MODEL_DIR
    / "unified_model_metrics.json"
)


MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# Feature configuration
# ==========================================================

CATEGORICAL_COLUMNS = [
    "brand",
    "model",
    "variant",
    "fuel_type",
    "transmission_type",
    "engine_type",
]

NUMERICAL_COLUMNS = [
    "vehicle_age",
    "km_driven",
    "seats",
    "max_power",
]


TARGET = "selling_price"


# ==========================================================
# Feature Engineering
# ==========================================================

def engineer_features(df):

    df = df.copy()

    # ------------------------------------------------------
    # Remove year
    #
    # 15,080 old records do not have year.
    # vehicle_age is available for all records.
    # ------------------------------------------------------

    if "year" in df.columns:

        df = df.drop(
            columns=["year"]
        )

    # ------------------------------------------------------
    # Categorical features
    # ------------------------------------------------------

    for column in CATEGORICAL_COLUMNS:

        if column not in df.columns:

            df[column] = "unknown"

        df[column] = (
            df[column]
            .fillna("unknown")
            .astype(str)
            .str.strip()
            .str.lower()
        )

    # ------------------------------------------------------
    # Numerical features
    # ------------------------------------------------------

    for column in NUMERICAL_COLUMNS:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df[NUMERICAL_COLUMNS] = (
        df[NUMERICAL_COLUMNS]
        .fillna(0)
    )

    # ------------------------------------------------------
    # One-hot encoding
    # ------------------------------------------------------

    df = pd.get_dummies(
        df,
        columns=CATEGORICAL_COLUMNS,
        drop_first=False
    )

    # ------------------------------------------------------
    # Convert boolean → integer
    # ------------------------------------------------------

    bool_columns = df.select_dtypes(
        include="bool"
    ).columns

    if len(bool_columns) > 0:

        df[bool_columns] = (
            df[bool_columns]
            .astype(int)
        )

    # ------------------------------------------------------
    # Convert everything to numeric
    # ------------------------------------------------------

    df = df.apply(
        pd.to_numeric,
        errors="coerce"
    )

    df = df.fillna(0)

    # ------------------------------------------------------
    # Safety check
    # ------------------------------------------------------

    object_columns = df.select_dtypes(
        include="object"
    ).columns

    if len(object_columns) > 0:

        raise ValueError(
            "Object columns remain: "
            f"{list(object_columns)}"
        )

    return df


# ==========================================================
# Load dataset
# ==========================================================

print("=" * 70)
print("UNIFIED XGBOOST TRAINING")
print("=" * 70)

print("\nLoading unified dataset...")

df = pd.read_csv(
    DATA_PATH
)

print(
    f"Rows: {len(df):,}"
)

print(
    f"Columns: {len(df.columns)}"
)


# ==========================================================
# Target and Features
# ==========================================================

X = df.drop(
    columns=[TARGET]
)

y = df[TARGET]


# ==========================================================
# Feature Engineering
# ==========================================================

print("\nEngineering features...")

X_encoded = engineer_features(
    X
)

reference_columns = (
    X_encoded.columns.tolist()
)

print(
    f"Generated features: {X_encoded.shape[1]}"
)


# ==========================================================
# Train/Test Split
# ==========================================================

X_train, X_test, y_train, y_test = (
    train_test_split(
        X_encoded,
        y,
        test_size=0.20,
        random_state=42
    )
)


print("\nDataset split:")

print(
    f"Training rows: {len(X_train):,}"
)

print(
    f"Testing rows : {len(X_test):,}"
)


# ==========================================================
# XGBoost
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
# Predictions
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
print("UNIFIED MODEL RESULTS")
print("=" * 70)

print(
    f"MAE : ₹{mae:,.2f}"
)

print(
    f"R²  : {r2:.6f}"
)

print("=" * 70)


# ==========================================================
# Save model
# ==========================================================

joblib.dump(
    model,
    MODEL_PATH
)


# ==========================================================
# Save reference columns
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
# Save metrics
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
    "R2": float(r2),
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

print("\nUnified model training completed.")