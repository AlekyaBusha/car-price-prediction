# 🚗 Car Price Prediction System

An end-to-end used-car price prediction application built with React, FastAPI, and XGBoost. The system predicts vehicle prices based on vehicle specifications and provides SHAP-based explanations and future price forecasts.

## 📋 Table of Contents

1. [Features](#features)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Quick Start](#quick-start)
6. [Environment Configuration](#environment-configuration)
7. [Backend Setup](#backend-setup)
8. [Frontend Setup](#frontend-setup)
9. [Running the Application](#running-the-application)
10. [API Endpoints](#api-endpoints)
11. [Machine Learning Model](#machine-learning-model)
12. [Deployment](#deployment)
13. [Troubleshooting](#troubleshooting)

## ✨ Features

- 🎯 **Price Prediction** - Predicts used-car prices with 94.8% accuracy
- 📊 **Price Range Estimation** - Provides realistic low-mid-high price ranges
- 📈 **SHAP Explanations** - Understand which features impact the prediction
- 🔮 **Future Price Forecasting** - Predict price trends over time
- 🔄 **Variant Comparison** - Compare different vehicle variants
- 🎨 **Responsive UI** - Mobile-friendly React interface
- 🔌 **REST API** - Production-ready FastAPI backend
- 📱 **Real-time Updates** - Instant predictions and insights

## 🛠 Technology Stack

### Frontend
- **React 19** - UI library
- **Vite 8** - Next-generation build tool
- **CSS3** - Styling
- **Fetch API** - HTTP client

### Backend
- **Python 3.8+** - Runtime
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### Machine Learning
- **XGBoost** - Primary prediction model
- **Scikit-learn** - ML utilities
- **Pandas & NumPy** - Data processing
- **SHAP** - Model explainability
- **Joblib** - Model serialization

## 📁 Project Structure

```
car-price-prediction/
│
├── backend/                           # Backend application
│   ├── api/                          # FastAPI application
│   │   ├── main.py                   # Application entry point
│   │   ├── schemas.py                # Pydantic models
│   │   ├── config.py                 # Configuration
│   │   └── routers/                  # API endpoints
│   │       ├── predict.py            # Price prediction
│   │       ├── dropdown.py           # Dropdown data
│   │       ├── explain.py            # SHAP explanations
│   │       ├── forecast.py           # Price forecasts
│   │       ├── suggestions.py        # Suggestions
│   │       └── health.py             # Health check
│   │
│   ├── services/                     # Business logic
│   │   ├── prediction_service.py
│   │   ├── variant_prediction_service.py
│   │   ├── dropdown_service.py
│   │   ├── explain_service.py
│   │   ├── forecast_service.py
│   │   └── ...
│   │
│   ├── ml/                           # Machine learning
│   │   ├── model_loader.py           # Load trained models
│   │   ├── feature_engineering.py    # Feature processing
│   │   ├── preprocessing.py
│   │   ├── forecast_engine.py
│   │   └── price_range.py            # Price range calculation
│   │
│   ├── utils/                        # Utility functions
│   │   ├── data_loader.py
│   │   ├── validators.py
│   │   ├── helpers.py
│   │   ├── constants.py
│   │   └── logger.py
│   │
│   ├── data/                         # Data files
│   │   ├── raw/                      # Raw datasets
│   │   └── processed/                # Processed/featured datasets
│   │
│   ├── models/                       # Trained models & artifacts
│   │   ├── xgb_model.pkl             # XGBoost model
│   │   ├── reference_columns.json    # Feature reference
│   │   ├── model_freq_map.json       # Frequency mapping
│   │   └── xgb_metrics.json          # Model metrics
│   │
│   ├── tests/                        # Unit tests
│   └── requirements.txt              # Python dependencies
│
├── frontend/vite-project/            # Frontend application
│   ├── src/
│   │   ├── components/               # React components
│   │   ├── pages/                    # Page components
│   │   ├── services/                 # API services
│   │   ├── assets/                   # Static assets
│   │   ├── App.jsx                   # Main component
│   │   └── main.jsx                  # Entry point
│   │
│   ├── public/                       # Static files
│   ├── package.json                  # NPM dependencies
│   ├── vite.config.js                # Vite configuration
│   ├── .env.example                  # Environment template
│   └── index.html
│
├── notebooks/                        # Jupyter notebooks
├── docs/                             # Documentation
├── .gitignore                        # Git configuration
├── .env.example                      # Backend environment template
└── README.md                         # This file
```

## 📦 Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 2GB free space

### Required Software
- **Node.js** v18+ (for frontend)
- **Python** 3.8+ (for backend)
- **npm** (comes with Node.js)
- **Git** (for cloning the repository)

### Verify Installation

```bash
# Check Node.js
node --version    # v18.0.0 or higher

# Check npm
npm --version     # 9.0.0 or higher

# Check Python
python --version  # 3.8 or higher
# or
python3 --version
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/AlekyaBusha/car-price-prediction.git
cd car-price-prediction
```

### 2. Setup Backend

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r backend/requirements.txt
```

### 3. Setup Frontend

```bash
cd frontend/vite-project

# Install npm dependencies
npm install

# Return to project root
cd ../..
```

### 4. Configure Environment

```bash
# Create environment files from examples
cp .env.example .env
cp frontend/vite-project/.env.example frontend/vite-project/.env.local
```

### 5. Run Application

**Terminal 1 - Backend:**
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend/vite-project
npm run dev
```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Environment Configuration

### Backend Environment (`.env`)

Create a `.env` file in the project root:

```env
# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Frontend Configuration
FRONTEND_URL=http://localhost:5173
```

### Frontend Environment (`.env.local` or `.env.production`)

Create a `.env.local` file in `frontend/vite-project/`:

```env
# Local Development
VITE_API_BASE_URL=http://localhost:8000

# Or for production:
# VITE_API_BASE_URL=https://your-production-api.com
```

## 📲 Backend Setup

### Installation

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r backend/requirements.txt
```

### Running the Backend

```bash
# Development (with auto-reload)
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000

# Production (without auto-reload)
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Verifying Backend

```bash
# Check if backend is running
curl http://localhost:8000/health

# View API documentation (auto-generated)
# Visit: http://localhost:8000/docs
```

## 🎨 Frontend Setup

### Installation

```bash
cd frontend/vite-project

# Install dependencies
npm install
```

### Development Server

```bash
npm run dev
```

Visit http://localhost:5173 in your browser.

### Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

The built files will be in `frontend/vite-project/dist/`

## ▶️ Running the Application

### Local Development (Two Terminals)

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend/vite-project
npm run dev
```

Open http://localhost:5173 in your browser.

## 🔌 API Endpoints

All endpoints are located at http://localhost:8000/

### Health Check
```
GET /health
Response: { "status": "ok" }
```

### Price Prediction
```
POST /predict/estimate
Body: {
  "brand": "Maruti",
  "model": "Swift",
  "vehicle_age": 5,
  "km_driven": 50000,
  "seller_type": "Individual",
  "fuel_type": "Petrol",
  "transmission": "Manual",
  "mileage": 18.5,
  "engine": 998,
  "max_power": 67.0,
  "seats": 5
}
```

### Full API Documentation

Access the interactive Swagger documentation at:
http://localhost:8000/docs

## 🤖 Machine Learning Model

### Model Information

| Property | Details |
|----------|---------|
| **Type** | XGBoost Regressor |
| **Purpose** | Used-car price prediction |
| **R² Score** | 0.9482 (94.82% variance explained) |
| **MAE** | ₹84,670.31 |
| **Model File** | `backend/models/xgb_model.pkl` (~363 KB) |

### Input Features (11 total)

1. **Brand** - Vehicle manufacturer
2. **Model** - Vehicle model
3. **Vehicle Age** - Years since manufacture
4. **KM Driven** - Total kilometers driven
5. **Seller Type** - Dealer/Individual
6. **Fuel Type** - Petrol/Diesel/CNG/LPG
7. **Transmission** - Manual/Automatic
8. **Mileage** - Average kilometers per liter
9. **Engine** - Engine displacement in CC
10. **Max Power** - Maximum power in bhp
11. **Seats** - Number of seats

### Target Variable
- **selling_price** - Predicted price in INR (₹)

### Model Files

Located in `backend/models/`:
- `xgb_model.pkl` - Trained XGBoost model
- `reference_columns.json` - Expected feature columns
- `model_freq_map.json` - Frequency mapping for categorical features
- `xgb_metrics.json` - Model performance metrics

## 🚀 Deployment

### Prerequisites for Deployment

1. Server with Python 3.8+ and Node.js v18+
2. Git installed
3. At least 2GB free disk space
4. 4GB+ RAM recommended

### Deployment Steps

#### 1. Clone Repository on Server

```bash
git clone https://github.com/AlekyaBusha/car-price-prediction.git
cd car-price-prediction
```

#### 2. Setup Backend

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

#### 3. Setup Frontend

```bash
cd frontend/vite-project
npm install
npm run build
cd ../..
```

#### 4. Configure Environment

```bash
# Edit .env with production settings
nano .env

# Example production .env:
# BACKEND_HOST=0.0.0.0
# BACKEND_PORT=8000
```

#### 5. Run Backend (Production)

```bash
source venv/bin/activate
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 6. Serve Frontend

Option A - Using Python:
```bash
cd frontend/vite-project/dist
python -m http.server 5173
```

Option B - Using Nginx (recommended):
```bash
cp -r frontend/vite-project/dist /var/www/car-price-prediction/
```

### Using Gunicorn (Production-Grade)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 backend.api.main:app
```

## 🆘 Troubleshooting

### Backend Issues

#### Python not found
```bash
# Use python3 explicitly
python3 -m venv venv
python3 -m pip install -r backend/requirements.txt
python3 -m uvicorn backend.api.main:app --reload
```

#### Port 8000 already in use
```bash
# Use a different port
uvicorn backend.api.main:app --port 8001
```

#### Models not loading
```bash
# Verify model files exist
ls -la backend/models/
# Should contain: xgb_model.pkl, xgb_metrics.json, reference_columns.json
```

### Frontend Issues

#### npm: command not found
- Install Node.js from https://nodejs.org
- Verify: `npm --version`

#### VITE_API_BASE_URL not working
- Ensure `.env.local` exists in `frontend/vite-project/`
- Check file contents: `cat frontend/vite-project/.env.local`

#### Port 5173 already in use
```bash
cd frontend/vite-project
npm run dev -- --port 5174
```

### General Issues

#### Cannot clone repository
```bash
# Check Git installation
git --version
```

#### CORS errors
- Ensure backend is running on correct host/port
- Check CORS configuration in `backend/api/main.py`
- Verify `VITE_API_BASE_URL` matches backend URL

## 📖 Additional Documentation

- [Setup Guide](SETUP.md)
- [Frontend Implementation](FRONTEND_IMPLEMENTATION.md)
- [Jupyter Notebooks](notebooks/)

## 📝 License

This project is provided for educational and commercial use.

---

**Version**: 1.0.0  
**Status**: Production Ready ✅  
**Last Updated**: August 2026
