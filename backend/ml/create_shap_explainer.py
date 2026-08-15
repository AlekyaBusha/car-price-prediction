import os
import joblib
import shap


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODELS_DIR = os.path.join(
    PROJECT_ROOT,
    "models"
)


MODEL_PATH = os.path.join(
    MODELS_DIR,
    "best_model.pkl"
)

EXPLAINER_PATH = os.path.join(
    MODELS_DIR,
    "shap_explainer.pkl"
)


print("Loading trained model...")

model = joblib.load(MODEL_PATH)

print("Model loaded:")
print(type(model))


print("Creating SHAP TreeExplainer...")

explainer = shap.TreeExplainer(model)

print("SHAP explainer created:")
print(type(explainer))


print("Saving SHAP explainer...")

joblib.dump(
    explainer,
    EXPLAINER_PATH
)


print("SHAP explainer saved successfully.")

print(
    "File:",
    EXPLAINER_PATH
)

print(
    "Size:",
    os.path.getsize(EXPLAINER_PATH),
    "bytes"
)
