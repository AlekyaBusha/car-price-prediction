# REST API Reference

The Used Car Price Prediction Backend is built using FastAPI and provides RESTful endpoints for vehicle valuation, SHAP explainability, depreciation forecasting, cascading dropdowns, and model evaluation metrics.

**Base URL**: `http://localhost:8000` (or configured production URL)

---

## 1. Prediction Endpoints

### 1.1 Predict Single Vehicle Price
- **Method**: `POST`
- **Route**: `/predict/`
- **Description**: Predicts the market selling price and fair price range for a specified vehicle.

#### Request Body (`application/json`):
```json
{
  "brand": "Maruti",
  "model": "Swift",
  "vehicle_age": 3,
  "km_driven": 25000,
  "seller_type": "Individual",
  "fuel_type": "Petrol",
  "transmission_type": "Manual",
  "mileage": 21.21,
  "engine": 1197,
  "max_power": 81.86,
  "seats": 5
}
```

#### Response (`200 OK`):
```json
{
  "success": true,
  "predicted_price": 674804.12,
  "price_range": {
    "low": 578804.12,
    "high": 770804.12,
    "confidence_level": 0.95
  },
  "currency": "INR"
}
```

---

### 1.2 Predict Multi-Variant Prices
- **Method**: `POST`
- **Route**: `/predict/variants`
- **Description**: Generates predicted prices for all factory variants and trims of a given brand and model.

#### Request Body:
```json
{
  "brand": "Maruti",
  "model": "Swift",
  "vehicle_age": 3,
  "km_driven": 25000
}
```

#### Response (`200 OK`):
```json
{
  "success": true,
  "brand": "Maruti",
  "model": "Swift",
  "count": 60,
  "variants": [
    {
      "variant": "zdi plus",
      "fuel_type": "Diesel",
      "transmission_type": "Manual",
      "engine": 1248,
      "max_power": 74.0,
      "seats": 5,
      "mileage": 28.4,
      "predicted_price": 844508.31,
      "price_range": { "low": 748508.31, "high": 940508.31 }
    }
  ]
}
```

---

## 2. Explainability & Insights Endpoints

### 2.1 SHAP Local Feature Attribution
- **Method**: `POST`
- **Route**: `/explain/`
- **Description**: Calculates TreeSHAP feature contributions that explain why the price deviates from the dataset base value.

#### Request Body: (Same as `/predict/`)

#### Response (`200 OK`):
```json
{
  "success": true,
  "prediction": 674804.12,
  "top_features": [
    { "feature": "vehicle_age", "impact": 0.2646 },
    { "feature": "max_power", "impact": -0.1609 },
    { "feature": "transmission_type_Manual", "impact": 0.0962 }
  ]
}
```

---

### 2.2 Future Depreciation Forecast
- **Method**: `POST`
- **Route**: `/forecast/`
- **Description**: Projects future valuation curve across 0, 6, 12, and 24 months based on aging and estimated 12,000 km/year mileage accumulation.

#### Response (`200 OK`):
```json
{
  "success": true,
  "forecast": [
    { "months": 0, "price": 674804.12 },
    { "months": 6, "price": 647043.19 },
    { "months": 12, "price": 608524.56 },
    { "months": 24, "price": 545730.69 }
  ]
}
```

---

## 3. Dynamic Dropdown Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/dropdown/brands` | `GET` | Returns list of all 32 verified car brands |
| `/dropdown/models?brand=Maruti` | `GET` | Returns models filtered by selected brand |
| `/dropdown/fuel_types` | `GET` | Returns available fuel types (`Petrol`, `Diesel`, `CNG`, `LPG`, `Electric`) |
| `/dropdown/transmissions` | `GET` | Returns transmission types (`Manual`, `Automatic`) |
| `/dropdown/seller_types` | `GET` | Returns seller types (`Individual`, `Dealer`, `Trustmark Dealer`) |
| `/dropdown/seats` | `GET` | Returns seat configurations (`2`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `14`) |

---

## 4. Model Accuracy & Evaluation Endpoint

### 4.1 Accuracy Metrics
- **Method**: `GET`
- **Route**: `/accuracy` (or `/analytics/accuracy`)
- **Description**: Returns the four key comparison metrics: Accuracy, Precision, Recall, and F1 Score for visualization on the Accuracy page.

#### Response (`200 OK`):
```json
{
  "success": true,
  "title": "Comparison of Model Evaluation Metrics",
  "metrics": [
    { "name": "Accuracy", "value": 0.97, "formatted": "0.97" },
    { "name": "Precision", "value": 1.00, "formatted": "1.00" },
    { "name": "Recall", "value": 0.10, "formatted": "0.10" },
    { "name": "F1 Score", "value": 0.18, "formatted": "0.18" }
  ]
}
```
