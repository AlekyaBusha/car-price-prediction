# System Architecture

## 1. High-Level System Architecture

The Used Car Price Prediction platform is an end-to-end Machine Learning web application structured into a modular, decoupled frontend-backend architecture.

```
┌─────────────────────────────────────────────────────────────┐
│                    REACT + VITE FRONTEND                    │
│                                                             │
│  [ Header Nav: Predict Price | Evaluation ]                 │
│                                                             │
│  ┌─────────────────────────┐  ┌──────────────────────────┐  │
│  │     Car Input Form      │  │    Fair Price Range      │  │
│  │ (32 Brands, 119 Models) │  │  (Confidence Interval)   │  │
│  └────────────┬────────────┘  └─────────────▲────────────┘  │
│               │                             │               │
│               │ (HTTP REST API)             │               │
│  ┌────────────▼─────────────────────────────┴────────────┐  │
│  │  Tabs: [ Future Forecast | SHAP | Compare Variants ]  │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │   Evaluation Page (Metrics, Heatmap, Residuals, etc.)  │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────┘
                               │ JSON / HTTP
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND SERVICE                  │
│                                                             │
│  [ Routers: /predict, /explain, /forecast, /evaluation ]    │
│                               │                             │
│  ┌────────────────────────────┼──────────────────────────┐  │
│  ▼                            ▼                          ▼  │
│  PredictionService       ExplainService            AnalyticsService│
│  (expm1 Target Inv)      (TreeSHAP Explainer)      (Test Eval)     │
│  └────────────┬───────────────┴─────────────┬────────────┘  │
│               ▼                             ▼               │
│  Feature Engineering Pipeline        Model Loader (Singleton)│
│  (44 Dense Columns, Freq Map)        (XGBoost Model Pickle) │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Component Design & Responsibilities

### 2.1 Frontend Layer (`frontend/vite-project/src/`)
- **`main.jsx` & `App.jsx`**: Bootstraps the React DOM and mounts the main dashboard.
- **`Header/`**: Provides top-level view switching between **Predict Price** and **Evaluation**.
- **`CarForm.jsx`**: Handles dynamic cascading dropdown queries (Brand -> Model -> Specs) and input validation.
- **`PriceRange.jsx`**: Renders predicted price along with fair lower and upper market valuation bounds.
- **`ForecastChartEnhanced.jsx`**: SVG line chart visualizing 0, 6, 12, and 24-month depreciation paths.
- **`ShapExplanation.jsx` & `ShapChart.jsx`**: Displays localized feature attributions (SHAP values).
- **`VariantComparison.jsx` & `VariantCard.jsx`**: Renders paginated factory variant cards with live pricing.
- **`AccuracyPage.jsx`**: Dedicated model accuracy metrics view rendering the "Comparison of Model Evaluation Metrics" 4-bar graph (Accuracy, Precision, Recall, F1 Score).

### 2.2 Backend Layer (`backend/`)
- **`api/main.py`**: Configures CORS middleware, life-cycle events, and mounts sub-routers.
- **`ml/feature_engineering.py`**: Converts raw JSON vehicle specifications into the 44-dimensional feature vector matching `reference_columns.json`.
- **`ml/model_loader.py`**: Singleton that loads `xgb_model.pkl`, `reference_columns.json`, and `model_freq_map.json` into RAM upon startup, enabling sub-15ms predictions.
- **`services/prediction_service.py`**: Runs XGBoost regression on `log1p` space and inverts via `np.expm1()`.
- **`services/explain_service.py`**: Computes SHAP values using `shap.TreeExplainer`.
- **`services/analytics_service.py`**: Evaluates model performance on the untouched 3,049 test records.
