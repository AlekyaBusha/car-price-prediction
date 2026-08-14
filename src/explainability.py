"""
SHAP explainability for car price predictions.
Given a trained model and a car's features, returns the top
contributing factors behind the predicted price.
"""

import os
import joblib
import shap
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')


def load_model(models_dir: str = None):
    """Loads the saved trained model from disk."""
    if models_dir is None:
        models_dir = MODELS_DIR
    return joblib.load(os.path.join(models_dir, 'best_model.pkl'))


def get_explainer(model):
    """Creates a SHAP TreeExplainer for the given model."""
    return shap.TreeExplainer(model)


def explain_prediction(model, features_df: pd.DataFrame, top_n: int = 5):
    """
    Returns the top_n features that most influenced the prediction,
    as a list of (feature_name, contribution_value) tuples,
    sorted by absolute impact, largest first.

    features_df must be a single-row DataFrame matching the model's
    training columns exactly (same order, same one-hot encoded columns).
    """
    explainer = get_explainer(model)
    shap_values = explainer.shap_values(features_df)

    # shap_values is a 2D array (rows x features) for tree models on regression
    row_values = shap_values[0]
    contributions = dict(zip(features_df.columns, row_values))

    top_features = sorted(
        contributions.items(),
        key=lambda item: abs(item[1]),
        reverse=True
    )[:top_n]

    return top_features


def explain_as_dict(model, features_df: pd.DataFrame, top_n: int = 5):
    """
    Same as explain_prediction, but returns a list of dicts
    for easier JSON serialization in the API layer.
    e.g. [{"feature": "vehicle_age", "impact": -85000.0}, ...]
    """
    top_features = explain_prediction(model, features_df, top_n=top_n)
    return [{"feature": name, "impact": float(value)} for name, value in top_features]


if __name__ == '__main__':
    # Quick manual test — loads the model and explains a single row
    # from your processed dataset just to confirm this works end to end.
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from feature_engineering import engineer_features

    cleaned_csv_path = os.path.join(PROJECT_ROOT, 'data', 'processed', 'cleaned_car_data.csv')
    df_raw = pd.read_csv(cleaned_csv_path)
    df_encoded, freq_map = engineer_features(df_raw)

    X = df_encoded.drop(columns=['selling_price'])
    sample_row = X.iloc[[0]]  # first car as a test case

    model = load_model()
    result = explain_as_dict(model, sample_row, top_n=5)

    print("Top contributing features for this prediction:")
    for item in result:
        print(f"  {item['feature']}: {item['impact']:+.2f}")