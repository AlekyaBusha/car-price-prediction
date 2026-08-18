"""
backend/ml/model_loader.py

Loads all machine learning artifacts once when the FastAPI server starts.

Current production model:
    XGBoost Regressor

SHAP:
    Created in memory from the loaded XGBoost model.
"""

import json
import joblib
import shap
from pathlib import Path


# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODELS_DIR = BASE_DIR / "models"

MODEL_PATH = MODELS_DIR / "xgb_model.pkl"

FREQ_MAP_PATH = MODELS_DIR / "model_freq_map.json"

REFERENCE_COLUMNS_PATH = (
    MODELS_DIR / "reference_columns.json"
)

METRICS_PATH = MODELS_DIR / "xgb_metrics.json"


# ==========================================================
# Model Loader
# ==========================================================

class ModelLoader:
    """
    Loads and stores all ML artifacts.

    The trained XGBoost model is loaded from xgb_model.pkl.

    SHAP TreeExplainer is created from the loaded model
    and kept in memory while the FastAPI application runs.
    """

    def __init__(self):
        self.model = None
        self.shap_explainer = None
        self.freq_map = None
        self.reference_columns = None
        self.metrics = None

    # ======================================================
    # Load all artifacts
    # ======================================================

    def load(self):
        print("=" * 60)
        print("Loading ML artifacts...")
        print("=" * 60)

        # --------------------------------------------------
        # Load XGBoost model
        # --------------------------------------------------
        print("Loading XGBoost model...")

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"XGBoost model not found: {MODEL_PATH}"
            )

        self.model = joblib.load(MODEL_PATH)
        print("[OK] XGBoost model loaded successfully.")
        print(f"Model type: {type(self.model)}")

        # --------------------------------------------------
        # Create SHAP TreeExplainer
        # --------------------------------------------------
        print("Creating SHAP TreeExplainer...")

        try:
            self.shap_explainer = shap.TreeExplainer(self.model)
            print("[OK] SHAP TreeExplainer created successfully.")
            print(f"SHAP type: {type(self.shap_explainer)}")
        except Exception as e:
            self.shap_explainer = None
            print("[WARN] SHAP TreeExplainer could not be created.")
            print(f"Reason: {e}")

        # --------------------------------------------------
        # Load frequency map
        # --------------------------------------------------
        print("Loading frequency map...")

        if not FREQ_MAP_PATH.exists():
            raise FileNotFoundError(
                f"Frequency map not found: {FREQ_MAP_PATH}"
            )

        with open(FREQ_MAP_PATH, "r") as file:
            self.freq_map = json.load(file)

        print("[OK] Frequency map loaded.")

        # --------------------------------------------------
        # Load reference columns
        # --------------------------------------------------
        print("Loading reference columns...")

        if not REFERENCE_COLUMNS_PATH.exists():
            raise FileNotFoundError(
                f"Reference columns not found: {REFERENCE_COLUMNS_PATH}"
            )

        with open(REFERENCE_COLUMNS_PATH, "r") as file:
            self.reference_columns = json.load(file)

        print("[OK] Reference columns loaded.")

        # --------------------------------------------------
        # Load XGBoost metrics
        # --------------------------------------------------
        print("Loading XGBoost metrics...")

        if not METRICS_PATH.exists():
            print("[WARN] XGBoost metrics file not found.")
            self.metrics = {}
        else:
            with open(METRICS_PATH, "r") as file:
                self.metrics = json.load(file)
            print("[OK] XGBoost metrics loaded.")

        # --------------------------------------------------
        # Final status
        # --------------------------------------------------
        print()
        print("=" * 60)
        print("ML ARTIFACTS LOADED")
        print("=" * 60)
        print(f"Model: {type(self.model).__name__}")
        print(f"SHAP available: {self.shap_explainer is not None}")
        print(f"Frequency map: {len(self.freq_map)} entries")
        print(f"Reference columns: {len(self.reference_columns)} columns")
        print(f"Metrics: {self.metrics}")
        print("=" * 60)

        return self


# ==========================================================
# Global Loader Instance
# ==========================================================

loader = ModelLoader()
# Auto-load artifacts so loader is always ready
try:
    loader.load()
except Exception as _e:
    pass


def initialize():
    if loader.model is None:
        loader.load()
    return loader