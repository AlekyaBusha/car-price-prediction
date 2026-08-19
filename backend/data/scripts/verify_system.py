import sys
import os
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from backend.api.main import app
from backend.ml.model_loader import loader

# Reload loader to ensure fresh artifacts in memory
loader.load()

client = TestClient(app)

print("--- Test 1: Price Prediction (Maruti Swift) ---")
car_swift = {
    "brand": "Maruti",
    "model": "Swift",
    "fuel_type": "Petrol",
    "transmission_type": "Manual",
    "seller_type": "Individual",
    "engine": 1197,
    "max_power": 81.86,
    "seats": 5,
    "vehicle_age": 3,
    "km_driven": 25000,
    "mileage": 21.21
}
r_pred = client.post("/predict/", json=car_swift)
assert r_pred.status_code == 200, f"Prediction API failed: {r_pred.text}"
p_json = r_pred.json()
print(f"Maruti Swift Predicted Price: ₹{p_json['predicted_price']:,.2f}")
print(f"Price Range: ₹{p_json['price_range']['low']:,.2f} - ₹{p_json['price_range']['high']:,.2f}")

print("\n--- Test 2: Price Prediction (Zero-Model Brand: BMW) ---")
car_bmw = {
    "brand": "BMW",
    "model": "",
    "fuel_type": "Petrol",
    "transmission_type": "Automatic",
    "seller_type": "Dealer",
    "vehicle_age": 2,
    "km_driven": 20000,
    "engine": 1998,
    "max_power": 189,
    "seats": 5,
    "mileage": 14.8
}
r_bmw = client.post("/predict/", json=car_bmw)
assert r_bmw.status_code == 200, f"BMW Prediction failed: {r_bmw.text}"
print(f"BMW Predicted Price: ₹{r_bmw.json()['predicted_price']:,.2f}")

print("\n--- Test 3: SHAP Explanation ---")
r_exp = client.post("/explain/", json=car_swift)
assert r_exp.status_code == 200, f"Explain API failed: {r_exp.text}"
exp_json = r_exp.json()
print(f"Predicted in SHAP: ₹{exp_json['prediction']:,.2f}")
print("SHAP Top Features:", exp_json["top_features"][:3])

print("\n--- Test 4: Forecast Engine ---")
r_fc = client.post("/forecast/", json=car_swift)
assert r_fc.status_code == 200, f"Forecast API failed: {r_fc.text}"
fc_json = r_fc.json()
print("Forecast depreciation curve:", fc_json["forecast"])

print("\n--- Test 5: Variant Prediction ---")
r_var = client.post("/predict/variants", json={"brand": "Maruti", "model": "Swift", "vehicle_age": 3, "km_driven": 25000})
assert r_var.status_code == 200, f"Variant API failed: {r_var.text}"
var_json = r_var.json()
print(f"Variant count: {var_json['count']}")
print("Top Variant:", var_json["variants"][0]["variant"], f"Price: ₹{var_json['variants'][0]['predicted_price']:,.2f}")

print("\n*** ALL INTEGRATION TESTS PASSED WITH 100% SUCCESS! ***")
