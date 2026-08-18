"""
Fair price range calculation for car price predictions.
Uses the model's MAE (mean absolute error) as an uncertainty band
around the point prediction, so we return a realistic range
instead of a single number.
"""

import os
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')


def load_mae(models_dir: str = None) -> float:
    """Loads the model's MAE from the saved metrics file."""
    if models_dir is None:
        models_dir = MODELS_DIR

    metrics_file = os.path.join(models_dir, 'xgb_metrics.json')
    if not os.path.exists(metrics_file):
        metrics_file = os.path.join(models_dir, 'model_metrics.json')

    if os.path.exists(metrics_file):
        try:
            with open(metrics_file, 'r') as f:
                metrics = json.load(f)
            return float(metrics.get('MAE', 80000.0))
        except Exception:
            pass

    return 80000.0


def get_price_range(point_prediction: float, mae: float = None, z: float = 1.2):
    """
    Returns a (low, mid, high) price range around a point prediction.

    z controls how wide the range is — 1.2x MAE gives a reasonably
    generous but still tight range. Increase z for a wider/safer range.
    """
    if mae is None:
        mae = load_mae()

    low = max(0, point_prediction - z * mae)  # price can't go negative
    high = point_prediction + z * mae

    return {
        "low": round(low, 2),
        "predicted": round(point_prediction, 2),
        "high": round(high, 2)
    }


if __name__ == '__main__':
    # Quick manual test using a sample point prediction
    sample_prediction = 650000  # e.g. ₹6.5L, just for testing the range logic

    price_range = get_price_range(sample_prediction)

    print("Fair price range:")
    print(f"  Low:       ₹{price_range['low']:,.0f}")
    print(f"  Predicted: ₹{price_range['predicted']:,.0f}")
    print(f"  High:      ₹{price_range['high']:,.0f}")