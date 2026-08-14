"""
backend/ml/model_loader.py

Loads all machine learning artifacts once when the FastAPI server starts.
Other modules can import `loader` to access the model and related files.
"""

import json
import joblib
from pathlib import Path


# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

MODEL_PATH = MODELS_DIR / "best_model.pkl"
SHAP_EXPLAINER_PATH = MODELS_DIR / "shap_explainer.pkl"
FREQ_MAP_PATH = MODELS_DIR / "model_freq_map.json"
REFERENCE_COLUMNS_PATH = MODELS_DIR / "reference_columns.json"
METRICS_PATH = MODELS_DIR / "model_metrics.json"


# ==========================================================
# Model Loader
# ==========================================================

class ModelLoader:
    """
    Loads and stores all ML artifacts.
    These are loaded only once when the backend starts.
    """

    def __init__(self):
        self.model = None
        self.shap_explainer = None
        self.freq_map = None
        self.reference_columns = None
        self.metrics = None

    def load(self):
        """Load all required artifacts."""

        # -----------------------------
        # Load trained model
        # -----------------------------
        print("Loading trained model...")
        self.model = joblib.load(MODEL_PATH)

        # -----------------------------
        # Load SHAP explainer (optional)
        # -----------------------------
        print("Loading SHAP explainer...")

        try:
            self.shap_explainer = joblib.load(SHAP_EXPLAINER_PATH)
            print("✓ SHAP explainer loaded successfully.")

        except Exception as e:
            self.shap_explainer = None
            print("⚠ SHAP explainer not found or corrupted.")
            print(f"Reason: {e}")
            print("Continuing without SHAP support.")

        # -----------------------------
        # Load frequency map
        # -----------------------------
        print("Loading frequency map...")

        with open(FREQ_MAP_PATH, "r") as file:
            self.freq_map = json.load(file)

        # -----------------------------
        # Load reference columns
        # -----------------------------
        print("Loading reference columns...")

        with open(REFERENCE_COLUMNS_PATH, "r") as file:
            self.reference_columns = json.load(file)

        # -----------------------------
        # Load metrics
        # -----------------------------
        print("Loading model metrics...")

        with open(METRICS_PATH, "r") as file:
            self.metrics = json.load(file)

        print("✓ All available ML artifacts loaded successfully.")

        return self


# ==========================================================
# Global Loader Instance
# ==========================================================

loader = ModelLoader()


def initialize():
    """
    Call this once when FastAPI starts.
    """
    loader.load()
    return loader