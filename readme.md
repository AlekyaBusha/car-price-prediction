
# Car Price Prediction

An end-to-end used-car price prediction application built with React, FastAPI, and XGBoost. The system predicts vehicle prices based on vehicle specifications and provides SHAP-based explanations and future price forecasts.

## Features

- Used-car price prediction
- Price range estimation
- SHAP-based prediction explanations
- Future price forecasting
- Dynamic vehicle selection
- REST API with FastAPI
- React-based web interface

## Tech Stack

**Frontend**
- React
- Vite
- JavaScript
- CSS

**Backend**
- Python
- FastAPI
- Uvicorn
- Pydantic

**Machine Learning**
- XGBoost
- Scikit-learn
- Pandas
- NumPy
- SHAP
- SciPy
- Joblib

## Model

The current model is an XGBoost Regressor trained for used-car price prediction.

| Metric | Value |
|---|---:|
| R² Score | 0.9482 |
| MAE | ₹84,670.31 |
| Model Size | ~363 KB |

### Input Features

- Brand
- Model
- Vehicle Age
- Kilometers Driven
- Seller Type
- Fuel Type
- Transmission
- Mileage
- Engine
- Maximum Power
- Seats

### Target

`selling_price`

## Architecture

```text
React Frontend
      |
      | REST API
      v
FastAPI Backend
      |
      +---- Prediction
      |
      +---- SHAP Explanation
      |
      +---- Price Forecast
      |
      v
XGBoost Model
````

## Project Structure

```text
car-price-prediction/
├── backend/
│   ├── api/
│   ├── ml/
│   ├── models/
│   ├── services/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   └── vite-project/
│
├── docs/
├── notebooks/
├── .gitignore
├── run.sh
└── README.md
```

## Installation

### Clone

```bash
git clone https://github.com/AlekyaBusha/car-price-prediction.git
cd car-price-prediction
```

### Backend

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

Start the backend:

```bash
uvicorn backend.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend/vite-project
npm install
npm run dev
```

## Model Training

Train the XGBoost model using:

```bash
python backend/ml/train_xgboost.py
```

The trained model is saved as:

```text
backend/models/xgb_model.pkl
```

## API Endpoints

```text
POST /predict/
POST /explain/
POST /forecast/
```

The API also provides endpoints for dynamically loading vehicle-related options.

## Dataset

The project uses used-car data containing vehicle specifications, usage information, seller information, and selling prices.

Additional compatible datasets are being evaluated to increase the training data and improve model performance.

## Development Status

Current status:

* XGBoost model implemented
* FastAPI backend implemented
* React frontend implemented
* SHAP explainability implemented
* Price forecasting implemented
* Dynamic vehicle selection implemented
* Larger dataset integration in progress

## License

This project is intended for educational and development purposes.

