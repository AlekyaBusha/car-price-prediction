"""
backend/ml/train_xgboost.py

Trains the improved XGBRegressor for car price prediction using:
- Target Transformation: log1p(selling_price)
- 5-Fold Cross-Validation for robust generalization
- Exact untouched 20% test-set evaluation
- Real metrics serialization to backend/ml/model_metrics.json and backend/models/xgb_metrics.json
"""

import json
import os
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error,
    r2_score,
    median_absolute_error
)
from xgboost import XGBRegressor

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_car_data.csv"
MODELS_DIR = BASE_DIR / "models"
ML_DIR = BASE_DIR / "ml"

XGB_MODEL_PATH = MODELS_DIR / "xgb_model.pkl"
XGB_METRICS_PATH = MODELS_DIR / "xgb_metrics.json"
ML_METRICS_PATH = ML_DIR / "model_metrics.json"
REF_COLUMNS_PATH = MODELS_DIR / "reference_columns.json"
FREQ_MAP_PATH = MODELS_DIR / "model_freq_map.json"

sys.path.append(str(PROJECT_ROOT))
from backend.ml.feature_engineering import engineer_features


# ==========================================================
# Training Configuration
# ==========================================================

HYPERPARAMETERS = {
    "n_estimators": 450,
    "max_depth": 7,
    "learning_rate": 0.025,
    "subsample": 0.8,
    "colsample_bytree": 0.75,
    "min_child_weight": 3,
    "gamma": 0.0,
    "reg_alpha": 0.2,
    "reg_lambda": 1.5,
    "objective": "reg:squarederror",
    "random_state": 42,
    "n_jobs": -1
}


def load_and_preprocess_data():
    print("Loading dataset from:", DATA_PATH)
    df = pd.read_csv(DATA_PATH)
    total_rows = len(df)
    print(f"Total dataset rows: {total_rows:,}")

    # Split 80/20 train/test
    train_df, test_df = train_test_split(df, test_size=0.20, random_state=42)
    print(f"Train samples: {len(train_df):,}, Test samples: {len(test_df):,}")

    # Fit feature engineering on train data
    encoded_train, freq_map = engineer_features(train_df)
    X_train = encoded_train.drop(columns=["selling_price"])
    y_train = encoded_train["selling_price"]
    reference_columns = X_train.columns.tolist()

    # Apply to test data
    encoded_test, _ = engineer_features(
        test_df,
        freq_map=freq_map,
        reference_columns=reference_columns
    )
    X_test = encoded_test
    y_test = test_df["selling_price"]

    return df, train_df, test_df, X_train, y_train, X_test, y_test, freq_map, reference_columns


def run_cross_validation(X_train, y_train):
    print("\nRunning 5-fold cross-validation on training partition...")
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    
    cv_maes = []
    cv_rmses = []
    cv_r2s = []
    cv_medaes = []

    for fold, (tr_idx, val_idx) in enumerate(kf.split(X_train), 1):
        X_tr, X_val = X_train.iloc[tr_idx], X_train.iloc[val_idx]
        y_tr, y_val = y_train.iloc[tr_idx], y_train.iloc[val_idx]

        fold_model = XGBRegressor(**HYPERPARAMETERS)
        fold_model.fit(X_tr, np.log1p(y_tr))

        preds = np.expm1(fold_model.predict(X_val))
        
        f_mae = mean_absolute_error(y_val, preds)
        f_rmse = root_mean_squared_error(y_val, preds)
        f_r2 = r2_score(y_val, preds)
        f_medae = median_absolute_error(y_val, preds)

        cv_maes.append(f_mae)
        cv_rmses.append(f_rmse)
        cv_r2s.append(f_r2)
        cv_medaes.append(f_medae)

        print(f"  Fold {fold}: MAE = ₹{f_mae:,.2f}, RMSE = ₹{f_rmse:,.2f}, R² = {f_r2:.4f}")

    cv_results = {
        "cv_mae_mean": round(float(np.mean(cv_maes)), 2),
        "cv_mae_std": round(float(np.std(cv_maes)), 2),
        "cv_rmse_mean": round(float(np.mean(cv_rmses)), 2),
        "cv_r2_mean": round(float(np.mean(cv_r2s)), 4),
        "cv_medae_mean": round(float(np.mean(cv_medaes)), 2)
    }

    print(f"-> 5-Fold Mean MAE: ₹{cv_results['cv_mae_mean']:,.2f} (± ₹{cv_results['cv_mae_std']:,.2f})")
    return cv_results


def train_final_model(X_train, y_train, X_test, y_test, total_rows, cv_results):
    print("\nTraining final XGBoost model on full training partition...")
    model = XGBRegressor(**HYPERPARAMETERS)
    model.fit(X_train, np.log1p(y_train))
    print("Training complete.")

    print("\nEvaluating final model on untouched 20% test partition...")
    test_preds_raw = model.predict(X_test)
    test_preds = np.expm1(test_preds_raw)

    mae = float(mean_absolute_error(y_test, test_preds))
    rmse = float(root_mean_squared_error(y_test, test_preds))
    r2 = float(r2_score(y_test, test_preds))
    medae = float(median_absolute_error(y_test, test_preds))
    mape = float(np.mean(np.abs((y_test - test_preds) / y_test)) * 100)

    print("=" * 60)
    print("TEST SET EVALUATION RESULTS")
    print("=" * 60)
    print(f"MAE                   : ₹{mae:,.2f}")
    print(f"RMSE                  : ₹{rmse:,.2f}")
    print(f"R² Score              : {r2:.6f} ({r2*100:.2f}%)")
    print(f"Median Absolute Error : ₹{medae:,.2f}")
    print(f"MAPE                  : {mape:.2f}%")
    print("=" * 60)

    metrics_payload = {
        "model_name": "XGBRegressor",
        "algorithm": "XGBoost",
        "dataset_rows": int(total_rows),
        "train_rows": int(len(X_train)),
        "validation_rows": 0,
        "test_rows": int(len(X_test)),
        "feature_count": int(X_train.shape[1]),
        "target": "selling_price",
        "target_transformation": "log1p",
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "r2": round(r2, 6),
        "median_absolute_error": round(medae, 2),
        "mape": round(mape, 2),
        "cv_mae_mean": cv_results["cv_mae_mean"],
        "cv_mae_std": cv_results["cv_mae_std"],
        "n_estimators": HYPERPARAMETERS["n_estimators"],
        "max_depth": HYPERPARAMETERS["max_depth"],
        "learning_rate": HYPERPARAMETERS["learning_rate"],
        "subsample": HYPERPARAMETERS["subsample"],
        "colsample_bytree": HYPERPARAMETERS["colsample_bytree"],
        "min_child_weight": HYPERPARAMETERS["min_child_weight"],
        "gamma": HYPERPARAMETERS["gamma"],
        "reg_alpha": HYPERPARAMETERS["reg_alpha"],
        "reg_lambda": HYPERPARAMETERS["reg_lambda"]
    }

    return model, metrics_payload


def save_artifacts(model, metrics, freq_map, reference_columns):
    print("\nSaving model artifacts...")
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    ML_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Model pickle
    joblib.dump(model, XGB_MODEL_PATH, compress=3)
    print("Saved model:", XGB_MODEL_PATH)

    # 2. Reference columns
    with open(REF_COLUMNS_PATH, "w") as f:
        json.dump(reference_columns, f, indent=4)
    print("Saved reference columns:", REF_COLUMNS_PATH)

    # 3. Frequency map
    with open(FREQ_MAP_PATH, "w") as f:
        json.dump(freq_map, f, indent=4)
    print("Saved frequency map:", FREQ_MAP_PATH)

    # 4. xgb_metrics.json in models directory
    with open(XGB_METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)
    print("Saved metrics:", XGB_METRICS_PATH)

    # 5. model_metrics.json in ml directory
    with open(ML_METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)
    print("Saved ML model metrics:", ML_METRICS_PATH)


def main():
    df, train_df, test_df, X_train, y_train, X_test, y_test, freq_map, reference_columns = (
        load_and_preprocess_data()
    )

    cv_results = run_cross_validation(X_train, y_train)

    model, metrics = train_final_model(
        X_train,
        y_train,
        X_test,
        y_test,
        total_rows=len(df),
        cv_results=cv_results
    )

    save_artifacts(model, metrics, freq_map, reference_columns)
    print("\nXGBoost training and artifact serialization complete.")


if __name__ == "__main__":
    main()
