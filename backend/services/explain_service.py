"""
backend/services/explain_service.py

SHAP Explainability Service
"""

import pandas as pd

from backend.ml.model_loader import loader


class ExplainService:

    def explain(self, encoded_df: pd.DataFrame, top_n: int = 5):

        explainer = loader.shap_explainer

        shap_values = explainer.shap_values(encoded_df)

        row = shap_values[0]

        contributions = []

        for feature, value in zip(encoded_df.columns, row):

            contributions.append({
                "feature": feature,
                "impact": float(value)
            })

        contributions.sort(
            key=lambda x: abs(x["impact"]),
            reverse=True
        )

        return contributions[:top_n]


explain_service = ExplainService()