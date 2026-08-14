"""
Basic tests for the car valuation model pipeline.

These aren't exhaustive - just practical checks to catch
obvious breakage before a demo: does the model load, does it
predict sensible numbers, does the forecast/timing logic work.
"""

import os
import sys

# Make sure Python can find our src/ folder
current_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_folder)
src_folder = os.path.join(project_root, 'src')
sys.path.append(src_folder)

from explainability import load_model, explain_as_dict
from price_range import get_price_range, load_mae
from forecast_engine import load_artifacts, build_car_row, forecast_price
from timing_advisor import get_timing_advice
from feature_engineering import engineer_features


# A sample car used across all tests
SAMPLE_CAR = {
    "brand": "Maruti",
    "model": "Swift",
    "vehicle_age": 3,
    "km_driven": 40000,
    "seller_type": "Individual",
    "fuel_type": "Petrol",
    "transmission_type": "Manual",
    "mileage": 21.0,
    "engine": 1197,
    "max_power": 82.0,
    "seats": 5
}


def test_model_loads():
    """Check the saved model file loads without errors."""
    model = load_model()
    assert model is not None


def test_prediction_is_positive_number():
    """A car's predicted price should be a positive number, not zero or negative."""
    model, freq_map, reference_columns = load_artifacts()
    row_df = build_car_row(SAMPLE_CAR)
    encoded_df, _ = engineer_features(row_df, freq_map=freq_map, reference_columns=reference_columns)

    prediction = model.predict(encoded_df)[0]

    assert prediction > 0


def test_price_range_has_low_mid_high():
    """The price range should return low < predicted < high."""
    mae = load_mae()
    price_range = get_price_range(650000, mae=mae)

    assert price_range["low"] < price_range["predicted"] < price_range["high"]


def test_explain_returns_top_features():
    """SHAP explanation should return a non-empty list of contributing features."""
    model, freq_map, reference_columns = load_artifacts()
    row_df = build_car_row(SAMPLE_CAR)
    encoded_df, _ = engineer_features(row_df, freq_map=freq_map, reference_columns=reference_columns)

    contributions = explain_as_dict(model, encoded_df, top_n=5)

    assert len(contributions) > 0
    assert "feature" in contributions[0]
    assert "impact" in contributions[0]


def test_forecast_returns_four_time_points():
    """Forecast should return exactly 4 points: 0, 6, 12, 24 months."""
    forecast = forecast_price(SAMPLE_CAR)

    months_returned = [f["months"] for f in forecast]

    assert months_returned == [0, 6, 12, 24]


def test_forecast_prices_are_positive():
    """All forecasted prices should be positive numbers."""
    forecast = forecast_price(SAMPLE_CAR)

    for point in forecast:
        assert point["price"] > 0


def test_timing_advice_has_valid_recommendation():
    """Timing advisor should return one of the three expected recommendations."""
    forecast = forecast_price(SAMPLE_CAR)
    advice = get_timing_advice(forecast)

    assert advice["recommendation"] in ["wait", "buy_now", "neutral"]
    assert len(advice["message"]) > 0


if __name__ == '__main__':
    # Run all tests manually and print results, without needing pytest installed
    tests = [
        test_model_loads,
        test_prediction_is_positive_number,
        test_price_range_has_low_mid_high,
        test_explain_returns_top_features,
        test_forecast_returns_four_time_points,
        test_forecast_prices_are_positive,
        test_timing_advice_has_valid_recommendation,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            print(f"PASSED: {test_func.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAILED: {test_func.__name__} - {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {test_func.__name__} - {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed out of {len(tests)} tests")