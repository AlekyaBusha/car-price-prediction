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

# Fixed 80/20 train/test split
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Baseline features
encoded_train, freq_map = engineer_features(train_df)
X_train_base = encoded_train.drop(columns=["selling_price"])
y_train_base = encoded_train["selling_price"]

encoded_test, _ = engineer_features(test_df, freq_map=freq_map, reference_columns=X_train_base.columns.tolist())
X_test_base = encoded_test
y_test_base = test_df["selling_price"]

print("=" * 70)
print("TEST SET EVALUATION COMPARISON")
print("=" * 70)

# 1. Baseline Model
m1 = XGBRegressor(n_estimators=300, max_depth=6, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, random_state=42, n_jobs=-1)
m1.fit(X_train_base, y_train_base)
p1 = m1.predict(X_test_base)
print("[1. Baseline XGBoost (Raw Target)]")
print(f"MAE: ₹{mean_absolute_error(y_test_base, p1):,.2f} | RMSE: ₹{root_mean_squared_error(y_test_base, p1):,.2f} | R2: {r2_score(y_test_base, p1):.6f} | MedAE: ₹{median_absolute_error(y_test_base, p1):,.2f} | MAPE: {np.mean(np.abs((y_test_base - p1)/y_test_base))*100:.2f}%")

# 2. Tuned Model (Raw Target)
m2 = XGBRegressor(n_estimators=400, max_depth=6, learning_rate=0.035, subsample=0.85, colsample_bytree=0.8, min_child_weight=2, reg_alpha=0.1, reg_lambda=1.0, random_state=42, n_jobs=-1)
m2.fit(X_train_base, y_train_base)
p2 = m2.predict(X_test_base)
print("\n[2. Tuned XGBoost (Raw Target)]")
print(f"MAE: ₹{mean_absolute_error(y_test_base, p2):,.2f} | RMSE: ₹{root_mean_squared_error(y_test_base, p2):,.2f} | R2: {r2_score(y_test_base, p2):.6f} | MedAE: ₹{median_absolute_error(y_test_base, p2):,.2f} | MAPE: {np.mean(np.abs((y_test_base - p2)/y_test_base))*100:.2f}%")

# 3. Tuned Model (Log1p Target)
m3 = XGBRegressor(n_estimators=450, max_depth=6, learning_rate=0.035, subsample=0.85, colsample_bytree=0.8, min_child_weight=2, reg_alpha=0.1, reg_lambda=1.0, random_state=42, n_jobs=-1)
m3.fit(X_train_base, np.log1p(y_train_base))
p3 = np.expm1(m3.predict(X_test_base))
print("\n[3. Tuned XGBoost (Log1p Target)]")
print(f"MAE: ₹{mean_absolute_error(y_test_base, p3):,.2f} | RMSE: ₹{root_mean_squared_error(y_test_base, p3):,.2f} | R2: {r2_score(y_test_base, p3):.6f} | MedAE: ₹{median_absolute_error(y_test_base, p3):,.2f} | MAPE: {np.mean(np.abs((y_test_base - p3)/y_test_base))*100:.2f}%")

# 4. Model with 500 estimators, max_depth=6, lr=0.03 (Raw target)
m4 = XGBRegressor(n_estimators=500, max_depth=6, learning_rate=0.03, subsample=0.85, colsample_bytree=0.8, min_child_weight=2, reg_alpha=0.2, reg_lambda=1.2, random_state=42, n_jobs=-1)
m4.fit(X_train_base, y_train_base)
p4 = m4.predict(X_test_base)
print("\n[4. Optimized Fine-Tuned XGBoost (Raw Target)]")
print(f"MAE: ₹{mean_absolute_error(y_test_base, p4):,.2f} | RMSE: ₹{root_mean_squared_error(y_test_base, p4):,.2f} | R2: {r2_score(y_test_base, p4):.6f} | MedAE: ₹{median_absolute_error(y_test_base, p4):,.2f} | MAPE: {np.mean(np.abs((y_test_base - p4)/y_test_base))*100:.2f}%")
