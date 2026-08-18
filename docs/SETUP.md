# Setup & Installation Guide

This guide provides step-by-step instructions to set up, configure, and run the Used Car Price Prediction application locally.

---

## 1. Prerequisites

Ensure you have the following software installed:
- **Python**: 3.9 or higher (Python 3.10–3.12 recommended)
- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher
- **Git**: For version control

---

## 2. Repository Setup

Clone the repository and enter the project root directory:

```bash
cd "car price pridiction"
```

---

## 3. Backend Setup

### Step 3.1: Create & Activate a Python Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3.2: Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

### Step 3.3: Verify Model Artifacts

Ensure the following pre-trained model artifacts are present in `backend/models/`:
- `xgb_model.pkl` (Production XGBoost Regressor)
- `reference_columns.json` (44 feature schema)
- `model_freq_map.json` (Model frequency encoding map)
- `xgb_metrics.json` (Trained model metrics)

*(Optional: To retrain the XGBoost model from scratch, run `python backend/ml/train_xgboost.py`)*

### Step 3.4: Start the FastAPI Backend Server

```powershell
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be available at:
- **API Root**: `http://localhost:8000/`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## 4. Frontend Setup

### Step 4.1: Navigate to Frontend Directory

Open a new terminal window:

```bash
cd frontend/vite-project
```

### Step 4.2: Install Node Dependencies

```bash
npm install
```

### Step 4.3: Configure Environment Variables

Create a `.env` file in `frontend/vite-project/` (or use defaults from `.env.example`):

```env
VITE_API_URL=http://localhost:8000
```

### Step 4.4: Start the Vite Development Server

```bash
npm run dev
```

The frontend application will open at:
`http://localhost:5173/`

---

## 5. Verification & Testing

### Backend Full Suite Verification:
```powershell
python backend/data/scripts/verify_system.py
```

### Frontend Production Build:
```powershell
cd frontend/vite-project
npm run build
```
