# 🚗 Used Car Price Prediction Platform

An end-to-end, production-grade Machine Learning web application designed to deliver accurate used car market valuations across India. Built with **React + Vite**, **FastAPI**, and an optimized **XGBoost Regressor (`XGBRegressor`)**, the platform features fair market price ranges, multi-horizon depreciation forecasting, TreeSHAP feature attributions, real factory variant comparisons, and a comprehensive statistical model evaluation dashboard.

---

## 📋 Table of Contents
1. [Project Overview](#1-project-overview)
2. [Key Features](#2-key-features)
3. [Technology Stack](#3-technology-stack)
4. [Project Structure](#4-project-structure)
5. [Frontend Setup](#5-frontend-setup)
6. [Backend Setup](#6-backend-setup)
7. [How to Run the Project](#7-how-to-run-the-project)
8. [API Reference](#8-api-reference)
9. [Dataset Information](#9-dataset-information)
10. [XGBoost Model Architecture](#10-xgboost-model-architecture)
11. [Model Evaluation Metrics](#11-model-evaluation-metrics)
12. [SHAP Explainability](#12-shap-explainability)
13. [Future Depreciation Forecasting](#13-future-depreciation-forecasting)
14. [Compare Variants](#14-compare-variants)
15. [Deployment Guide](#15-deployment-guide)

---

## 1. Project Overview
Estimating the fair market price of a pre-owned vehicle requires balancing complex non-linear interactions across age, mileage, brand prestige, fuel efficiency, engine displacement, and transmission type. This project provides a transparent, data-driven pricing engine trained on 15,244 verified market transactions.

---

## 2. Key Features
- 🎯 **Instant Price Prediction**: Real-time valuation in Indian Rupees (INR) with sub-15ms inference.
- 📊 **Fair Market Price Range**: 95% confidence bounds providing realistic bargaining intervals.
- 🚗 **Factory Variant Comparison**: (Default Tab 1) Instant comparison with all available trims and specifications.
- 🔍 **TreeSHAP Explainability**: (Tab 2) Local feature contribution breakdown explaining positive/negative price drivers.
- 📈 **Depreciation Forecasting**: (Tab 3) Valuation curve over 0, 6, 12, and 24 months based on vehicle aging.
- ⏱️ **Timing Recommendation**: AI buying advisor ("Buy Now" vs "Wait" recommendation).

---

## 3. Technology Stack

### Frontend
- **Framework**: React 19 + Vite 8
- **Styling**: Vanilla CSS3 (Custom responsive design system)
- **HTTP Client**: Axios / Fetch API

### Backend
- **Framework**: FastAPI (Asynchronous Python REST API)
- **Server**: Uvicorn ASGI
- **Data Validation**: Pydantic v2

### Machine Learning & Data Processing
- **Regression Algorithm**: XGBoost (`XGBRegressor`)
- **Explainability**: SHAP (`shap.TreeExplainer`)
- **Data Processing**: Pandas, NumPy, Scikit-learn
- **Model Serialization**: Joblib

---

## 4. Project Structure

```
car-price-prediction/
│
├── README.md                          # Main project documentation
├── .gitignore                         # Git exclusion rules
├── .env.example                       # Environment template
│
├── frontend/                          # Frontend Application
│   └── vite-project/
│       ├── package.json               # Frontend dependencies
│       ├── vite.config.js             # Vite configuration
│       ├── index.html                 # Single page entry HTML
│       ├── src/
│       │   ├── components/            # Reusable UI components
│       │   ├── pages/                 # Dashboard & Evaluation views
│       │   ├── services/              # API communication layer
│       │   ├── styles/                # Component & page stylesheets
│       │   ├── App.jsx                # Root application
│       │   └── main.jsx               # React bootstrap
│       └── public/                    # Static favicon and vector assets
│
├── backend/                           # Backend Application
│   ├── api/
│   │   ├── main.py                    # FastAPI entry point & CORS
│   │   ├── schemas.py                 # Pydantic validation schemas
│   │   └── routers/                   # API routes (predict, explain, forecast, etc.)
│   ├── services/                      # Business logic & ML orchestrators
│   ├── ml/                            # Feature engineering, loaders & training scripts
│   ├── models/                        # Pre-trained models (.pkl) & JSON metadata
│   ├── data/                          # Raw & cleaned dataset archives
│   ├── utils/                         # Helper utilities & data loaders
│   └── requirements.txt               # Backend Python requirements
│
├── docs/                              # Detailed Documentation Suite
│   ├── SETUP.md                       # Local installation instructions
│   ├── DEPLOYMENT.md                  # Docker & cloud deployment guide
│   ├── API.md                         # REST API specification
│   ├── MODEL.md                       # XGBoost ML architecture & tuning
│   ├── DATASET.md                     # Data dictionary & cleaning pipeline
│   └── ARCHITECTURE.md                # System design & component interaction
│
└── notebooks/                         # Research & Analysis Notebooks
    ├── 01_eda.ipynb
    ├── 02_feature_engineering.ipynb
    ├── 03_model_training.ipynb
    └── 04_shap_explainalibility.ipynb
```

---

## 5. Frontend Setup

```bash
cd frontend/vite-project
npm install
```

---

## 6. Backend Setup

```bash
# From project root
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate

pip install -r backend/requirements.txt
```

---

## 7. How to Run the Project

### Start Backend API:
```powershell
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Start Frontend Client:
```powershell
cd frontend/vite-project
npm run dev
```

Visit `http://localhost:5173/` in your browser.

---

## 8. API Reference

| Method | Route | Description |
|---|---|---|
| `POST` | `/predict/` | Single car price prediction & price range |
| `POST` | `/predict/variants` | Batch variant price predictions for a model |
| `POST` | `/explain/` | Local SHAP feature attributions |
| `POST` | `/forecast/` | Depreciation forecast (0, 6, 12, 24 months) |
| `GET` | `/evaluation` | Real test-set performance metrics & analytics |
| `GET` | `/dropdown/brands` | List of 32 verified car brands |
| `GET` | `/dropdown/models` | Models filtered by selected brand |
| `GET` | `/health` | Server health check |

---

## 9. Dataset Information

- **Records**: 15,244 verified used car listings.
- **Features**: Brand (32), Model (119), Vehicle Age (0-29 yrs), KM Driven (100-3.8M km), Fuel Type (5), Transmission (2), Seller Type (3), Engine CC (624-6592), Max Power (34-626 bhp), Seats (2-14), Mileage (4-33.5 km/l).
- **Target**: Selling Price (₹40,000 to ₹3.95 Crore).

---

## 10. XGBoost Model Architecture

- **Algorithm**: Extreme Gradient Boosting (`XGBRegressor`)
- **Target Transformation**: `log1p(selling_price)` with `expm1()` target inversion.
- **Hyperparameters**:
  - `n_estimators`: 450
  - `max_depth`: 7
  - `learning_rate`: 0.025
  - `subsample`: 0.8
  - `colsample_bytree`: 0.75
  - `min_child_weight`: 3
  - `reg_alpha`: 0.2
  - `reg_lambda`: 1.5

---

## 11. Model Evaluation Metrics

Evaluated on the untouched 20% test partition (3,049 records):

| Metric | Value | Description |
|---|---|---|
| **$R^2$ Score** | **0.9388 (93.88%)** | Variance in price explained by the model |
| **MAE** | **₹92,608.39** | Mean absolute prediction error |
| **RMSE** | **₹192,899.86** | Root mean squared error |
| **Median Absolute Error** | **₹51,268.94** | 50% of predictions are within ₹51k |
| **MAPE** | **12.25%** | Mean absolute percentage error |
| **5-Fold CV MAE** | **₹96,890.43 (± ₹9,734.78)** | Cross-validation generalization error |

---

## 12. SHAP Explainability
The platform computes real-time TreeSHAP local attributions for each prediction, displaying the top factors raising or lowering the vehicle's market value compared to baseline.

---

## 13. Future Depreciation Forecasting
Projects depreciation over 6, 12, and 24 months factoring in age progression and an average accumulation of 12,000 km/year.

---

## 14. Compare Variants
Users can compare the selected car with other factory variants of the same brand and model, viewing specifications (engine CC, power, seats, transmission) alongside live estimated prices.

## 15. Deployment Guide

Refer to [`docs/DEPLOYMENT.md`](file:///c:/Users/Dell/OneDrive/Desktop/car%20price%20pridiction/docs/DEPLOYMENT.md) for full Docker, Docker Compose, and cloud hosting instructions.
