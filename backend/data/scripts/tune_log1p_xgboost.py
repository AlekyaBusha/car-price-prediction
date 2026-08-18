import sys
import os
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score, median_absolute_error
from xgboost import XGBRegressor

PROJECT_ROOT = Path("c:/Users/Dell/OneDrive/Desktop/car price pridiction")
df = pd.read_csv(PROJECT_ROOT / "backend/data/processed/cleaned_car_data.csv")

sys.path.append(str(PROJECT_ROOT))
from backend.ml.feature_engineering import engineer_features

# Split 80/20
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

encoded_train, freq_map = engineer_features(train_df)
X_train = encoded_train.drop(columns=["selling_price"])
y_train = encoded_train["selling_price"]

encoded_test, _ = engineer_features(test_df, freq_map=freq_map, reference_columns=X_train.columns.tolist())
X_test = encoded_test
y_test = test_df["selling_price"]

configs = [
    {"n_estimators": 350, "max_depth": 6, "learning_rate": 0.04, "subsample": 0.85, "colsample_bytree": 0.8, "min_child_weight": 2, "reg_alpha": 0.05, "reg_lambda": 1.0},
    {"n_estimators": 400, "max_depth": 6, "learning_rate": 0.035, "subsample": 0.85, "colsample_bytree": 0.8, "min_child_weight": 2, "reg_alpha": 0.1, "reg_lambda": 1.0},
    {"n_estimators": 450, "max_depth": 6, "learning_rate": 0.03, "subsample": 0.85, "colsample_bytree": 0.8, "min_child_weight": 2, "reg_alpha": 0.1, "reg_lambda": 1.0},
    {"n_estimators": 500, "max_depth": 6, "learning_rate": 0.03, "subsample": 0.85, "colsample_bytree": 0.85, "min_child_weight": 1, "reg_alpha": 0.05, "reg_lambda": 0.8},
    {"n_estimators": 450, "max_depth": 7, "learning_rate": 0.025, "subsample": 0.8, "colsample_bytree": 0.75, "min_child_weight": 3, "reg_alpha": 0.2, "reg_lambda": 1.5},
    {"n_estimators": 350, "max_depth": 5, "learning_rate": 0.045, "subsample": 0.85, "colsample_bytree": 0.85, "min_child_weight": 2, "reg_alpha": 0.1, "reg_lambda": 1.0},
]

print("=" * 70)
print("LOG1P TARGET: 5-FOLD CV & TEST SET EVALUATION")
print("=" * 70)

kf = KFold(n_splits=5, shuffle=True, random_state=42)

for i, cfg in enumerate(configs):
    cv_maes = []
    cv_rmses = []
    cv_r2s = []
    
    for tr_idx, val_idx in kf.split(X_train):
        X_tr, X_val = X_train.iloc[tr_idx], X_train.iloc[val_idx]
        y_tr, y_val = y_train.iloc[tr_idx], y_train.iloc[val_idx]
        
        m = XGBRegressor(**cfg, random_state=42, n_jobs=-1)
        m.fit(X_tr, np.log1p(y_tr))
        
        preds = np.expm1(m.predict(X_val))
        cv_maes.append(mean_absolute_error(y_val, preds))
        cv_rmses.append(root_mean_squared_error(y_val, preds))
        cv_r2s.append(r2_score(y_val, preds))
        
    # Fit on full training set and evaluate on test set
    final_m = XGBRegressor(**cfg, random_state=42, n_jobs=-1)
    final_m.fit(X_train, np.log1p(y_train))
    test_preds = np.expm1(final_m.predict(X_test))
    
    test_mae = mean_absolute_error(y_test, test_preds)
    test_rmse = root_mean_squared_error(y_test, test_preds)
    test_r2 = r2_score(y_test, test_preds)
    test_medae = median_absolute_error(y_test, test_preds)
    test_mape = np.mean(np.abs((y_test - test_preds) / y_test)) * 100
    
    print(f"Config {i+1}: {cfg}")
    print(f"  -> CV MAE: ₹{np.mean(cv_maes):,.2f} (+/- ₹{np.std(cv_maes):,.2f}) | CV R2: {np.mean(cv_r2s):.4f}")
    print(f"  -> TEST MAE: ₹{test_mae:,.2f} | RMSE: ₹{test_rmse:,.2f} | R2: {test_r2:.6f} | MedAE: ₹{test_medae:,.2f} | MAPE: {test_mape:.2f}%\n")
