# Machine Learning Model Documentation

## 1. Algorithm Overview

The valuation engine is powered exclusively by **Extreme Gradient Boosting (`XGBRegressor`)**. XGBoost is chosen for its superior gradient tree-boosting performance on tabular regression datasets with non-linear feature interactions and skewed price targets.

---

## 2. Target Transformation

Used car prices exhibit strong positive skewness with high-value luxury outliers. To stabilize variance and penalize relative rather than unweighted absolute errors:
- **Training Target**: $y_{\text{train}} = \log(1 + \text{selling\_price})$ (`log1p`)
- **Inference Inversion**: $\hat{y}_{\text{pred}} = \exp(\hat{y}_{\text{raw}}) - 1$ (`expm1`)

### Impact of Target Transformation:
| Target Strategy | 5-Fold CV MAE | Test MAE | Test RMSE | Test R² | Test MedAE | Test MAPE |
|---|---|---|---|---|---|---|
| Raw Price Target | ₹98,014.53 | ₹95,397.71 | ₹197,477.38 | 0.9358 | ₹54,456.97 | 13.30% |
| **Log1p Price Target** | **₹96,890.43** | **₹92,608.39** | **₹192,899.86** | **0.9388** | **₹51,268.94** | **12.25%** |

---

## 3. Production Model Architecture & Hyperparameters

```python
XGBRegressor(
    n_estimators=450,
    max_depth=7,
    learning_rate=0.025,
    subsample=0.8,
    colsample_bytree=0.75,
    min_child_weight=3,
    gamma=0.0,
    reg_alpha=0.2,
    reg_lambda=1.5,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1
)
```

---

## 4. Feature Space & Dimensionality

The model utilizes **44 dense encoded features**:
- **Continuous Physical Specs (6)**: `vehicle_age`, `km_driven`, `mileage`, `engine`, `max_power`, `seats`
- **Model Frequency Encoding (1)**: `model_freq` (Frequency mapping across 119 car models to prevent high-dimensional sparse dilution)
- **One-Hot Categorical Encodings (37)**:
  - `brand_*`: 32 dummy columns
  - `fuel_type_*`: 5 dummy columns
  - `transmission_type_*`: 2 dummy columns
  - `seller_type_*`: 3 dummy columns

---

## 5. Verified Performance Metrics

Evaluated on the untouched 20% test partition (3,049 records):

- **Mean Absolute Error (MAE)**: **₹92,608.39**
- **Root Mean Squared Error (RMSE)**: **₹192,899.86**
- **$R^2$ Score (Variance Explained)**: **0.938801 (93.88%)**
- **Median Absolute Error (MedAE)**: **₹51,268.94**
- **Mean Absolute Percentage Error (MAPE)**: **12.25%**
- **5-Fold Cross-Validation MAE**: **₹96,890.43 (± ₹9,734.78)**

---

## 6. Training Pipeline

The official pipeline is located at [`backend/ml/train_xgboost.py`](file:///c:/Users/Dell/OneDrive/Desktop/car%20price%20pridiction/backend/ml/train_xgboost.py).
To retrain:
```powershell
python backend/ml/train_xgboost.py
```
This script splits the data, runs 5-fold cross-validation, fits the final model, computes test metrics, and serializes the model to `backend/models/xgb_model.pkl` along with `reference_columns.json`, `model_freq_map.json`, and `model_metrics.json`.
