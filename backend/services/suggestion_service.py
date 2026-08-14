"""
backend/services/suggestion_service.py

Smart AI Suggestions based on Brand + Model.
"""

import pandas as pd

from backend.ml.feature_engineering import engineer_features
from backend.ml.model_loader import loader
from backend.utils.data_loader import data_loader


class SuggestionService:

    def __init__(self):
        self.df = data_loader.df

    def _predict_price(self, car):

        df = pd.DataFrame([car])

        encoded, _ = engineer_features(
            df,
            freq_map=loader.freq_map,
            reference_columns=loader.reference_columns
        )

        return round(float(loader.model.predict(encoded)[0]), 2)

    def _filter_dataset(self, car):

        df = self.df

        if car.get("brand"):
            df = df[df["brand"] == car["brand"]]

        if car.get("model"):
            df = df[df["model"] == car["model"]]

        return df

    def generate(self, car):

        suggestions = []

        filtered = self._filter_dataset(car)

        if filtered.empty:
            filtered = self.df

        # ==========================================
        # Seats
        # ==========================================

        if car.get("seats") is None:

            seat_predictions = []

            values = sorted(filtered["seats"].dropna().unique())

            for value in values:

                temp = car.copy()
                temp["seats"] = int(value)

                try:

                    seat_predictions.append({
                        "value": int(value),
                        "predicted_price": self._predict_price(temp)
                    })

                except:
                    pass

            suggestions.append({
                "field": "Seats",
                "message": "Seats were not provided.",
                "recommendations": seat_predictions
            })

        # ==========================================
        # Engine
        # ==========================================

        if car.get("engine") is None:

            engine_predictions = []

            values = sorted(filtered["engine"].dropna().unique())

            for value in values:

                temp = car.copy()
                temp["engine"] = float(value)

                try:

                    engine_predictions.append({
                        "value": float(value),
                        "predicted_price": self._predict_price(temp)
                    })

                except:
                    pass

            suggestions.append({
                "field": "Engine",
                "message": "Engine was not provided.",
                "recommendations": engine_predictions
            })

        # ==========================================
        # Max Power
        # ==========================================

        if car.get("max_power") is None:

            power_predictions = []

            values = sorted(filtered["max_power"].dropna().unique())

            for value in values:

                temp = car.copy()
                temp["max_power"] = float(value)

                try:

                    power_predictions.append({
                        "value": float(value),
                        "predicted_price": self._predict_price(temp)
                    })

                except:
                    pass

            suggestions.append({
                "field": "Max Power",
                "message": "Max Power was not provided.",
                "recommendations": power_predictions
            })

        # ==========================================
        # Seller Type
        # ==========================================

        if car.get("seller_type") is None:

            seller_predictions = []

            values = sorted(filtered["seller_type"].dropna().unique())

            for value in values:

                temp = car.copy()
                temp["seller_type"] = value

                try:

                    seller_predictions.append({
                        "value": value,
                        "predicted_price": self._predict_price(temp)
                    })

                except:
                    pass

            suggestions.append({
                "field": "Seller Type",
                "message": "Seller Type was not provided.",
                "recommendations": seller_predictions
            })

        return suggestions


suggestion_service = SuggestionService()