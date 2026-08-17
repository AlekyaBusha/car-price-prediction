# Car Price Prediction Dashboard - Setup & Running Guide

## Overview

This is a comprehensive, production-ready Used Car Price Prediction application built with:
- **Frontend**: React + Vite (Light theme, fully responsive)
- **Backend**: FastAPI with XGBoost machine learning
- **Features**: Price prediction, variant comparison, SHAP explainability, price forecasting

## Prerequisites

- **Node.js** (v18+) - For frontend
- **Python** (3.8+) - For backend
- **npm** - Package manager for Node.js

## Quick Start

### Option 1: Running Both Backend & Frontend Locally

#### Step 1: Install Backend Dependencies

```bash
cd /home/pavan/Documents/car-price-prediction

# Install Python requirements
pip install -r backend/requirements.txt --break-system-packages
```

#### Step 2: Start Backend Server

```bash
cd /home/pavan/Documents/car-price-prediction

# Start FastAPI server (will run on http://127.0.0.1:8000)
uvicorn backend.api.main:app --reload
```

The backend will initialize models and load data on startup. You should see:
```
Backend Started Successfully
Uvicorn running on http://127.0.0.1:8000
```

#### Step 3: Start Frontend Development Server (New Terminal)

```bash
cd /home/pavan/Documents/car-price-prediction/frontend/vite-project

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

The frontend will start on `http://localhost:5173/`

#### Step 4: Access the Application

Open your browser and navigate to:
```
http://localhost:5173
```

You should see the Car Price Prediction dashboard with:
- Car form on the left (~35% width)
- Results area on the right (~65% width)
- Tab navigation for Variants | Explanation | Forecast

---

## Application Features

### 1. **Price Prediction**
- Select brand, model, fuel type, transmission, and seller type
- Optionally specify engine, max power, and seats
- Get instant price prediction with range estimate

### 2. **Variant Comparison**
- Compare different variants of the same car model
- See 8 variants per page with sorting options
- Sort by Price, Type, or Engine
- Filter by engine and seats specifications

### 3. **SHAP Explainability**
- Understand which features most influence the predicted price
- See positive (price-increasing) and negative (price-decreasing) factors
- Green bars show price increases, red bars show decreases

### 4. **Price Forecasting**
- View predicted price changes over 2 years
- See monthly depreciation estimates
- Get market timing recommendations

### 5. **Responsive Design**
- Works on desktop (two-column layout)
- Works on tablet (adjusted layout)
- Works on mobile (single-column stack)

---

## API Endpoints

The backend provides these endpoints (all at `http://127.0.0.1:8000`):

### Dropdowns
- `GET /dropdown/brands` - Get all car brands
- `GET /dropdown/models/{brand}` - Get models for brand
- `GET /dropdown/fuel-types/{brand}/{model}` - Fuel types
- `GET /dropdown/transmissions/{brand}/{model}` - Transmission types
- `GET /dropdown/seller-types/{brand}/{model}` - Seller types
- `GET /dropdown/engines/{brand}/{model}` - Engine sizes
- `GET /dropdown/max-powers/{brand}/{model}` - Max power values
- `GET /dropdown/seats/{brand}/{model}` - Seat count options

### Predictions
- `POST /predict/` - Predict price for single car
- `POST /predict/variants` - Predict prices for all variants
- `POST /predict/options/` - Get suggestions for optional fields
- `POST /explain/` - Get SHAP feature importance
- `POST /forecast/` - Get price forecast
- `GET /health` - Check backend status

---

## Building for Production

### Frontend Build

```bash
cd frontend/vite-project

# Create optimized production build
npm run build

# Output goes to: frontend/vite-project/dist/
```

### Backend Deployment

For production deployment, use a production ASGI server:

```bash
# Using gunicorn with uvicorn workers
pip install gunicorn
gunicorn backend.api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

---

## Project Structure

```
car-price-prediction/
├── backend/
│   ├── api/
│   │   ├── main.py          # FastAPI application
│   │   ├── schemas.py       # Request/response models
│   │   └── routers/         # API route definitions
│   ├── ml/                  # Machine learning code
│   ├── models/              # Trained models & metadata
│   ├── services/            # Business logic
│   ├── data/                # Data processing
│   ├── utils/               # Helper utilities
│   ├── tests/               # Unit tests
│   └── requirements.txt
│
├── frontend/
│   └── vite-project/
│       ├── src/
│       │   ├── components/  # React components
│       │   ├── styles/      # Component CSS files
│       │   ├── services/    # API communication layer
│       │   ├── pages/       # Page components
│       │   ├── App.jsx
│       │   └── index.css    # Global styles
│       ├── public/
│       ├── package.json
│       └── vite.config.js
│
├── notebooks/               # Jupyter notebooks for analysis
├── docs/                    # Documentation
└── readme.md
```

---

## Troubleshooting

### Frontend Won't Start

**Issue**: `npm: command not found`
- Install Node.js from nodejs.org
- Verify: `node --version` and `npm --version`

**Issue**: Port 5173 already in use
```bash
# Use a different port
npm run dev -- --port 3000
```

### Backend Won't Start

**Issue**: `ModuleNotFoundError: No module named 'fastapi'`
```bash
pip install -r backend/requirements.txt --break-system-packages
```

**Issue**: Port 8000 already in use
```bash
# Use a different port
uvicorn backend.api.main:app --reload --port 8001
# Then update frontend API_URL in src/services/api.js
```

**Issue**: Models not loading
- Ensure you're in the correct directory: `/home/pavan/Documents/car-price-prediction`
- Check that `backend/models/` contains the model files

### API Connection Issues

**Frontend shows error: "Failed to fetch brands"**
- Ensure backend is running: `http://127.0.0.1:8000/health`
- Check that CORS is enabled (should be in main.py)
- Verify API_URL is correct in `frontend/vite-project/src/services/api.js`

---

## Testing the Application

### Manual Test Cases

1. **Brand Dropdown**
   - Form should load with brands from API
   - Select a brand

2. **Model Dropdown**
   - Models should update based on selected brand
   - Select a model

3. **Dependent Dropdowns**
   - After selecting brand + model, fuel type, transmission, seller type, engine, seats should populate

4. **Price Prediction**
   - Fill required fields (brand, model, fuel type, transmission, seller type)
   - Click "Predict Price"
   - Should display price range card with low/predicted/high prices

5. **Variant Comparison**
   - Prediction should show variants tab
   - Display 8 variants per page
   - Can sort by price, type, or engine
   - Pagination works correctly

6. **SHAP Explanation**
   - Shows feature importance
   - Positive bars (green) for price increases
   - Negative bars (red) for price decreases

7. **Price Forecast**
   - Shows bar chart with prices over time
   - Table shows monthly changes
   - Timing recommendation displayed

8. **Optional Fields**
   - Engine and seats can be left empty
   - Still get variants when empty
   - Still get predictions when empty

9. **Reset Button**
   - Clears entire form
   - Clears all results
   - Returns to empty state

10. **Responsive Design**
    - Desktop: Two-column layout
    - Mobile: Single-column layout
    - All features work on mobile

11. **Error Handling**
    - Missing required fields show error
    - API errors display gracefully
    - Error message dismissible

12. **Light Theme**
    - No dark theme elements
    - Professional light appearance
    - Good contrast ratios for accessibility

---

## Light Theme Colors

All components use the following professional light theme palette:

- **Background**: `#F8FAFC` (very light blue-gray)
- **Card Background**: `#FFFFFF` (pure white)
- **Primary Text**: `#111827` (dark charcoal)
- **Secondary Text**: `#6B7280` (medium gray)
- **Primary Color**: `#2563EB` (professional blue)
- **Success**: `#22C55E` (green)
- **Danger**: `#DC2626` (red)
- **Borders**: `#E5E7EB` (light gray)

---

## Performance Notes

- Frontend build: ~231 KB (gzip: ~69 KB)
- CSS: ~18.8 KB (gzip: ~3.9 KB)
- All assets optimized by Vite
- Lazy loading for heavy components
- Efficient API caching where applicable

---

## Support & Documentation

For more details, see:
- Backend: `backend/api/routers/` - Individual endpoint documentation
- Frontend: `frontend/vite-project/README.md`
- ML Models: `backend/ml/` - Model training and evaluation code
- Data: `backend/data/data_dictionary.md` - Feature descriptions

---

## Key Technologies

### Frontend Stack
- React 18+ with Hooks
- Vite (ultra-fast build tool)
- CSS3 with CSS Variables
- Responsive Grid/Flexbox

### Backend Stack
- FastAPI (modern, fast web framework)
- XGBoost (gradient boosting ML)
- SHAP (model explainability)
- Pydantic (data validation)
- Pandas/NumPy (data processing)

### ML/Data
- XGBoost models (trained on real car data)
- SHAP for feature importance
- Feature engineering pipeline
- Data preprocessing & validation

---

## Next Steps

1. **Install dependencies** (backend & frontend)
2. **Start backend server** (uvicorn)
3. **Start frontend dev server** (npm run dev)
4. **Open dashboard** (http://localhost:5173)
5. **Run test cases** (manual or automated)
6. **Deploy** (see production build section)

Enjoy using the Car Price Prediction Dashboard! 🚗
