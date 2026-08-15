"""
XGBoost training pipeline for car price prediction.

This is an experiment against the existing Random Forest model.
It does NOT overwrite best_model.pkl.
"""

import json
import os
import sys

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor


# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

from feature_engineering import engineer_features


DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "cleaned_car_data.csv"
)

MODELS_DIR = os.path.join(
    PROJECT_ROOT,
    "models"
)

XGB_MODEL_PATH = os.path.join(
    MODELS_DIR,
    "xgb_model.pkl"
)

XGB_METRICS_PATH = os.path.join(
    MODELS_DIR,
    "xgb_metrics.json"
)


# ==========================================================
# Load and prepare data
# ==========================================================

def load_data():

    print("Loading dataset...")

    df = pd.read_csv(DATA_PATH)

    print("Dataset shape:", df.shape)

    encoded_df, freq_map = engineer_features(df)

    X = encoded_df.drop(
        columns=["selling_price"]
    )

    y = encoded_df["selling_price"]

    return X, y


# ==========================================================
# Train XGBoost
# ==========================================================

def train_model(X, y):

    print("Splitting dataset...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    print("Training XGBoost...")

    model = XGBRegressor(
        n_estimators=300,
        max_depth=6,
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

    print("Training complete.")

    # ------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------

    predictions = model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    metrics = {
        "model": "XGBRegressor",
        "n_estimators": 300,
        "max_depth": 6,
        "learning_rate": 0.05,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "MAE": float(mae),
        "R2": float(r2)
    }

    return model, metrics


# ==========================================================
# Save model
# ==========================================================

def save_model(model, metrics):

    print("Saving XGBoost model...")

    os.makedirs(
        MODELS_DIR,
        exist_ok=True
    )

    joblib.dump(
        model,
        XGB_MODEL_PATH,
        compress=3
    )

    with open(
        XGB_METRICS_PATH,
        "w"
    ) as f:

        json.dump(
            metrics,
            f,
            indent=4
        )

    print()
    print("XGBoost model saved:")
    print(XGB_MODEL_PATH)

    print()
    print("Metrics saved:")
    print(XGB_METRICS_PATH)


# ==========================================================
# Main
# ==========================================================

def main():

    X, y = load_data()

    model, metrics = train_model(
        X,
        y
    )

    save_model(
        model,
        metrics
    )

    print()
    print("=" * 50)
    print("XGBOOST RESULTS")
    print("=" * 50)

    print(
        f"MAE: ₹{metrics['MAE']:,.2f}"
    )

    print(
        f"R²: {metrics['R2']:.6f}"
    )

    print("=" * 50)


if __name__ == "__main__":
    main()