"""
Timing advisor for car purchase decisions.

Takes a depreciation forecast (from forecast_engine.py) and turns it
into a plain-English recommendation: buy now, or wait.
"""

import os
import sys

try:
    from backend.ml.forecast_engine import forecast_price
except ImportError:
    try:
        from forecast_engine import forecast_price
    except ImportError:
        pass


# Thresholds for classifying depreciation speed over the next 6 months
FAST_DROP_THRESHOLD = 8.0   # % drop that suggests waiting
SLOW_DROP_THRESHOLD = 3.0   # % drop that suggests price is stable


def calculate_drop_percentage(forecast: list, from_months: int = 0, to_months: int = 6) -> float:
    """
    Calculates the percentage price drop between two points in the forecast.
    """
    price_from = next(f['price'] for f in forecast if f['months'] == from_months)
    price_to = next(f['price'] for f in forecast if f['months'] == to_months)

    if price_from == 0:
        return 0.0

    drop_pct = (price_from - price_to) / price_from * 100
    return round(drop_pct, 2)


def get_timing_advice(forecast: list) -> dict:
    """
    Returns a recommendation dict based on how fast the car is expected
    to depreciate over the next 6 months.

    Returns:
      {
        "drop_pct_6mo": float,
        "recommendation": "wait" | "buy_now" | "neutral",
        "message": str
      }
    """
    drop_pct = calculate_drop_percentage(forecast, from_months=0, to_months=6)

    price_now = next(f['price'] for f in forecast if f['months'] == 0)
    price_6mo = next(f['price'] for f in forecast if f['months'] == 6)
    savings = round(price_now - price_6mo, 2)

    if drop_pct > FAST_DROP_THRESHOLD:
        recommendation = "wait"
        message = (
            f"Price is likely to drop about {drop_pct}% (₹{savings:,.0f}) "
            f"over the next 6 months. If you're not in a hurry, waiting could save you money."
        )
    elif drop_pct < SLOW_DROP_THRESHOLD:
        recommendation = "buy_now"
        message = (
            f"Price is expected to stay fairly stable (only {drop_pct}% drop over 6 months). "
            f"This is a reasonable time to buy."
        )
    else:
        recommendation = "neutral"
        message = (
            f"Moderate depreciation expected ({drop_pct}% over 6 months). "
            f"Buying now is reasonable, though modest savings are possible by waiting."
        )

    return {
        "drop_pct_6mo": drop_pct,
        "savings_6mo": savings,
        "recommendation": recommendation,
        "message": message
    }


if __name__ == '__main__':
    # Quick manual test using the same sample car as forecast_engine.py
    sample_car = {
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

    forecast = forecast_price(sample_car)
    advice = get_timing_advice(forecast)

    print("Forecast:")
    for f in forecast:
        print(f"  +{f['months']:>2} months: ₹{f['price']:,.0f}")

    print("\nTiming advice:")
    print(f"  Recommendation: {advice['recommendation']}")
    print(f"  {advice['message']}")