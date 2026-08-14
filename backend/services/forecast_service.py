"""
backend/services/forecast_service.py

Forecast service.
Uses the existing forecast_engine.
"""

from backend.ml.forecast_engine import forecast_price


class ForecastService:
    """
    Wrapper around the forecast engine.
    """

    def forecast(self, car_data: dict):

        return forecast_price(car_data)


forecast_service = ForecastService()