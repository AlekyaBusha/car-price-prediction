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

# Check for corrupted records
print("=== Data Quality & Outlier Check ===")
print(f"Total rows: {len(df):,}")
print("Min engine:", df["engine"].min(), "Max engine:", df["engine"].max())
print("Min max_power:", df["max_power"].min(), "Max max_power:", df["max_power"].max())
print("Min mileage:", df["mileage"].min(), "Max mileage:", df["mileage"].max())
print("Min vehicle_age:", df["vehicle_age"].min(), "Max vehicle_age:", df["vehicle_age"].max())
print("Min km_driven:", df["km_driven"].min(), "Max km_driven:", df["km_driven"].max())
print("Min price:", df["selling_price"].min(), "Max price:", df["selling_price"].max())

# Split 80/20 train/test
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

def compute_oof_target_encoding(train_data, val_data, cols, target_col, smoothing=15):
    tr = train_data.copy()
    val = val_data.copy()
    global_mean = tr[target_col].mean()
    
    for col in cols:
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        oof = pd.Series(index=tr.index, dtype=float)
        
        for tr_idx, h_idx in kf.split(tr):
            t_fold = tr.iloc[tr_idx]
            h_fold = tr.iloc[h_idx]
            stats = t_fold.groupby(col)[target_col].agg(["count", "mean"])
            sm = (stats["count"] * stats["mean"] + smoothing * global_mean) / (stats["count"] + smoothing)
            oof.iloc[h_idx] = h_fold[col].map(sm).fillna(global_mean)
            
        tr[f"{col}_te"] = oof
        
        # Validation encoding using full training stats
        full_stats = tr.groupby(col)[target_col].agg(["count", "mean"])
        full_sm = (full_stats["count"] * full_stats["mean"] + smoothing * global_mean) / (full_stats["count"] + smoothing)
        val[f"{col}_te"] = val[col].map(full_sm).fillna(global_mean)
        
    return tr, val

def create_features(d):
    res = d.copy()
    res["km_per_year"] = res["km_driven"] / (res["vehicle_age"] + 0.5)
    res["power_per_liter"] = res["max_power"] / (res["engine"] / 1000.0 + 0.05)
    res["power_per_seat"] = res["max_power"] / (res["seats"] + 0.1)
    res["log_km_driven"] = np.log1p(res["km_driven"])
    res["age_squared"] = res["vehicle_age"] ** 2
    res["is_luxury_brand"] = res["brand"].isin([
        "BMW", "Mercedes-Benz", "Audi", "Jaguar", "Land Rover", "Porsche",
        "Volvo", "Lexus", "Bentley", "Ferrari", "Rolls-Royce", "Maserati", "Mini"
    ]).astype(int)
    
    # One-hot encode brand, fuel_type, transmission_type, seller_type
    res = pd.get_dummies(res, columns=["brand", "fuel_type", "transmission_type", "seller_type"], drop_first=True)
    return res

print("\n" + "=" * 70)
print("HYPERPARAMETER TUNING OVER 5-FOLD CV")
print("=" * 70)

param_grid = [
    {"n_estimators": 350, "max_depth": 6, "learning_rate": 0.04, "subsample": 0.8, "colsample_bytree": 0.8, "min_child_weight": 2, "reg_alpha": 0.1, "reg_lambda": 1.0},
    {"n_estimators": 450, "max_depth": 6, "learning_rate": 0.035, "subsample": 0.85, "colsample_bytree": 0.75, "min_child_weight": 2, "reg_alpha": 0.5, "reg_lambda": 1.5},
    {"n_estimators": 500, "max_depth": 7, "learning_rate": 0.03, "subsample": 0.8, "colsample_bytree": 0.7, "min_child_weight": 3, "reg_alpha": 1.0, "reg_lambda": 2.0},
    {"n_estimators": 400, "max_depth": 5, "learning_rate": 0.05, "subsample": 0.85, "colsample_bytree": 0.85, "min_child_weight": 1, "reg_alpha": 0.1, "reg_lambda": 1.0},
    {"n_estimators": 600, "max_depth": 6, "learning_rate": 0.025, "subsample": 0.8, "colsample_bytree": 0.8, "min_child_weight": 2, "reg_alpha": 0.2, "reg_lambda": 1.0},
]

kf = KFold(n_splits=5, shuffle=True, random_state=42)

for i, params in enumerate(param_grid):
    maes, rmses, r2s, medaes = [], [], [], []
    
    for tr_idx, val_idx in kf.split(train_df):
        tr_raw = train_df.iloc[tr_idx].copy()
        val_raw = train_df.iloc[val_idx].copy()
        
        tr_te, val_te = compute_oof_target_encoding(tr_raw, val_raw, ["model", "brand"], "selling_price", smoothing=15)
        
        tr_feat = create_features(tr_te)
        val_feat = create_features(val_te)
        
        feature_cols = [c for c in tr_feat.columns if c not in ["selling_price", "model"]]
        val_feat = val_feat.reindex(columns=tr_feat.columns, fill_value=0)
        
        X_tr = tr_feat[feature_cols].astype(float)
        y_tr = tr_feat["selling_price"]
        X_val = val_feat[feature_cols].astype(float)
        y_val = val_feat["selling_price"]
        
        model = XGBRegressor(**params, random_state=42, n_jobs=-1, objective="reg:squarederror")
        model.fit(X_tr, y_tr)
        
        preds = model.predict(X_val)
        
        maes.append(mean_absolute_error(y_val, preds))
        rmses.append(root_mean_squared_error(y_val, preds))
        r2s.append(r2_score(y_val, preds))
        medaes.append(median_absolute_error(y_val, preds))
        
    print(f"Config {i+1}: {params}")
    print(f"  -> CV MAE: ₹{np.mean(maes):,.2f} (+/- ₹{np.std(maes):,.2f}) | RMSE: ₹{np.mean(rmses):,.2f} | R2: {np.mean(r2s):.4f} | MedAE: ₹{np.mean(medaes):,.2f}\n")
