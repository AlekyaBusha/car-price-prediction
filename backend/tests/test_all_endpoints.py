"""
backend/tests/test_all_endpoints.py

Comprehensive End-to-End Test Suite for all FastAPI routes, schemas, and prediction services.
Directly exercises router functions and backend services to ensure complete test coverage and speed.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# Set UTF-8 encoding for standard streams
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from backend.ml.model_loader import initialize, loader
from backend.services.dropdown_service import dropdown_service
from backend.api.schemas import CarInput, VariantPredictionInput
from backend.api.routers.predict import predict_price, predict_variants
from backend.api.routers.explain import explain
from backend.api.routers.forecast import forecast
from backend.api.routers.health import health
from backend.api.routers.dropdown import (
    get_brands,
    get_models,
    get_fuel_types,
    get_transmissions,
    get_seller_types,
    get_engines,
    get_max_powers,
    get_seats,
)



def test_complete_system():
    print("=" * 70, flush=True)
    print("PHASE 30: COMPLETE FASTAPI ENDPOINT TESTS", flush=True)
    print("=" * 70, flush=True)

    # Initialize models & dropdowns
    initialize()
    dropdown_service.reload_data()

    # 1. Health check
    health_res = health()
    print(f"GET /health/ -> Status: {health_res['status']}, Model Loaded: {health_res['model_loaded']}, SHAP Loaded: {health_res['shap_loaded']}", flush=True)
    assert health_res["status"] == "Healthy"
    assert health_res["model_loaded"] is True
    assert health_res["shap_loaded"] is True

    # 2. Dropdown Brands
    brands_res = get_brands()
    brands = brands_res.get("brands", [])
    print(f"GET /dropdown/brands -> Count: {len(brands)}, Sample: {brands[:8]}", flush=True)
    assert len(brands) >= 30, f"Expected at least 30 brands, got {len(brands)}"
    assert "Toyota" in brands and "Maruti" in brands and "Mahindra" in brands

    # Test vehicle scenarios across multiple brands & seat configurations
    vehicles_to_test = [
        {"brand": "Toyota", "model": "Fortuner", "expected_seats": [7]},
        {"brand": "Toyota", "model": "Innova", "expected_seats": [7, 8]},
        {"brand": "Maruti", "model": "Ertiga", "expected_seats": [7]},
        {"brand": "Mahindra", "model": "XUV500", "expected_seats": [7]},
        {"brand": "Hyundai", "model": "Creta", "expected_seats": [5]},
        {"brand": "Honda", "model": "City", "expected_seats": [5]},
    ]

    for v in vehicles_to_test:
        brand = v["brand"]
        model = v["model"]
        print(f"\n--- Testing Endpoints for: {brand} {model} ---", flush=True)

        # Models
        models_res = get_models(brand)
        models = models_res.get("models", [])
        assert model in models, f"Model {model} not found in brand {brand}"

        # Fuel types
        fuels_res = get_fuel_types(brand, model)
        fuels = fuels_res.get("fuel_types", [])
        assert len(fuels) > 0, f"No fuel types for {brand} {model}"

        # Transmissions
        trans_res = get_transmissions(brand, model)
        trans = trans_res.get("transmission_types", [])
        assert len(trans) > 0, f"No transmissions for {brand} {model}"

        # Seller types
        sellers_res = get_seller_types(brand, model)
        sellers = sellers_res.get("seller_types", [])
        assert len(sellers) > 0, f"No sellers for {brand} {model}"

        # Engines
        engines_res = get_engines(brand, model)
        engines = engines_res.get("engines", [])
        assert len(engines) > 0, f"No engines for {brand} {model}"

        # Max Powers
        powers_res = get_max_powers(brand, model)
        powers = powers_res.get("max_powers", [])
        assert len(powers) > 0, f"No max powers for {brand} {model}"

        # Seats
        seats_res = get_seats(brand, model)
        seats = seats_res.get("seats", [])
        assert seats == v["expected_seats"], f"Seats mismatch for {brand} {model}: got {seats}, expected {v['expected_seats']}"
        print(f"   Dropdowns verified: Fuels={fuels}, Trans={trans}, Seats={seats}", flush=True)

        # POST /predict/
        predict_input = CarInput(
            brand=brand,
            model=model,
            fuel_type=fuels[0],
            transmission_type=trans[0],
            seller_type=sellers[0],
            engine=engines[0],
            max_power=powers[0],
            seats=seats[0],
            vehicle_age=3.0,
            km_driven=35000.0,
            mileage=16.0
        )
        pred_res = predict_price(predict_input)
        assert pred_res["success"] is True
        price = pred_res["predicted_price"]
        price_range = pred_res["price_range"]
        print(f"   POST /predict/ -> Predicted Price: INR {price:,.2f} | Range: [{price_range['low']:,.0f} - {price_range['high']:,.0f}]", flush=True)

        # POST /predict/variants (with engine & seats specified)
        var_input_filtered = VariantPredictionInput(
            brand=brand,
            model=model,
            vehicle_age=3.0,
            km_driven=35000.0,
            mileage=16.0,
            engine=engines[0],
            seats=seats[0]
        )
        var_filtered_res = predict_variants(var_input_filtered)
        assert var_filtered_res["success"] is True
        print(f"   POST /predict/variants (filtered) -> Variants Count: {var_filtered_res.get('count')}", flush=True)

        # POST /predict/variants (with engine=null, seats=null)
        var_input_all = VariantPredictionInput(
            brand=brand,
            model=model,
            vehicle_age=3.0,
            km_driven=35000.0,
            mileage=16.0,
            engine=None,
            seats=None
        )
        var_all_res = predict_variants(var_input_all)
        assert var_all_res["success"] is True
        print(f"   POST /predict/variants (all trims) -> Total Variants Count: {var_all_res.get('count')}", flush=True)
        if var_all_res.get("variants"):
            v_sample = var_all_res["variants"][0]
            print(f"      Top Trim: {v_sample['variant']} | Price: INR {v_sample['predicted_price']:,.2f} | Seats: {v_sample['seats']}", flush=True)

        # POST /explain/
        explain_res = explain(predict_input)
        assert "top_features" in explain_res
        print(f"   POST /explain/ -> Top Features Count: {len(explain_res['top_features'])}", flush=True)

        # POST /forecast/
        forecast_res = forecast(predict_input)
        assert "forecast" in forecast_res
        forecast_list = forecast_res["forecast"]
        print(f"   POST /forecast/ -> Forecast Periods Count: {len(forecast_list)}", flush=True)

    print("\n" + "=" * 70, flush=True)
    print("ALL FASTAPI ENDPOINT TESTS PASSED SUCCESSFULLY (100%)", flush=True)
    print("=" * 70, flush=True)

    return True


if __name__ == "__main__":
    success = test_complete_system()
    if not success:
        sys.exit(1)
