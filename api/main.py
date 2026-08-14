"""
FastAPI backend for the car valuation advisor.

This is a simple, student-friendly version:
- Clear step-by-step comments
- Try/except blocks so errors show up clearly instead of failing silently
- No extra complexity, just the 3 core endpoints
"""

import os
import sys
import traceback

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Step 1: Let Python find our src/ folder so we can import our own files
current_folder = os.path.dirname(os.path.abspath(__file__))
src_folder = os.path.join(current_folder, '..', 'src')
sys.path.append(src_folder)

# Step 2: Import our own functions from src/
from explainability import load_model, explain_as_dict
from price_range import get_price_range, load_mae
from forecast_engine import load_artifacts, build_car_row, forecast_price
from timing_advisor import get_timing_advice
from feature_engineering import engineer_features


# Step 3: Create the FastAPI app
app = FastAPI(title="Car Valuation Advisor API")

# Step 3b: Allow the React frontend (running on a different port) to call this API.
# Without this, the browser blocks requests from localhost:5173 to localhost:8000.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Step 4: Define what a "car" input looks like
class CarInput(BaseModel):
    brand: str
    model: str
    vehicle_age: float
    km_driven: float
    seller_type: str
    fuel_type: str
    transmission_type: str
    mileage: float
    engine: float
    max_power: float
    seats: int


# Step 5: Load the model ONCE when the server starts (not every request)
print("Loading model and artifacts...")
model, freq_map, reference_columns = load_artifacts()
mae = load_mae()
print("Model loaded successfully!")


@app.get("/")
def home():
    """Simple health check - visit this to confirm the API is running."""
    return {"status": "Car Valuation Advisor API is running"}


@app.post("/predict")
def predict(car: CarInput):
    """Takes car details, returns predicted price + fair range."""
    try:
        # Convert the car input into the format our model expects
        car_dict = car.dict()
        row_df = build_car_row(car_dict)
        encoded_df, _ = engineer_features(row_df, freq_map=freq_map, reference_columns=reference_columns)

        # Make the prediction
        point_prediction = float(model.predict(encoded_df)[0])

        # Get the fair price range
        result = get_price_range(point_prediction, mae=mae)

        return result

    except Exception as e:
        # If anything goes wrong, print the full error in the terminal
        # AND send a readable error message back to the browser
        print("ERROR in /predict:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/explain")
def explain(car: CarInput):
    """Takes car details, returns why the model predicted that price."""
    try:
        car_dict = car.dict()
        row_df = build_car_row(car_dict)
        encoded_df, _ = engineer_features(row_df, freq_map=freq_map, reference_columns=reference_columns)

        contributions = explain_as_dict(model, encoded_df, top_n=5)

        return {"contributions": contributions}

    except Exception as e:
        print("ERROR in /explain:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/forecast")
def forecast(car: CarInput):
    """Takes car details, returns future price forecast + buy/wait advice."""
    try:
        car_dict = car.dict()
        forecast_result = forecast_price(car_dict)
        advice = get_timing_advice(forecast_result)

        return {
            "forecast": forecast_result,
            "advice": advice
        }

    except Exception as e:
        print("ERROR in /forecast:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))