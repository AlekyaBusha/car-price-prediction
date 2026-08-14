"""
Model training pipeline for car price prediction.
Trains, tunes, and saves a Random Forest Regressor.
"""

import json
import joblib
import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Make paths work regardless of where this script is run from
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # so 'feature_engineering' imports correctly

from feature_engineering import engineer_features


PARAM_GRID = {
    'n_estimators': [200, 300, 500],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2', None]
}


def load_and_prepare_data(cleaned_csv_path: str = None):
    """
    Loads cleaned raw data and applies feature engineering.
    Returns X, y, freq_map, reference_columns.
    """
    if cleaned_csv_path is None:
        cleaned_csv_path = os.path.join(PROJECT_ROOT, 'data', 'processed', 'cleaned_car_data.csv')

    df_raw = pd.read_csv(cleaned_csv_path)
    df_encoded, freq_map = engineer_features(df_raw)

    X = df_encoded.drop(columns=['selling_price'])
    y = df_encoded['selling_price']
    reference_columns = X.columns.tolist()

    return X, y, freq_map, reference_columns


def train_and_tune(X, y, n_iter=20, cv=3, random_state=42):
    """
    Splits data, runs RandomizedSearchCV over a Random Forest, and returns
    the best fitted model plus test set + metrics.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )

    rf = RandomForestRegressor(random_state=random_state, n_jobs=-1)
    search = RandomizedSearchCV(
        rf, param_distributions=PARAM_GRID,
        n_iter=n_iter, cv=cv, scoring='r2',
        random_state=random_state, n_jobs=-1, verbose=1
    )
    search.fit(X_train, y_train)

    best_model = search.best_estimator_
    preds = best_model.predict(X_test)

    metrics = {
        'model': 'RandomForestRegressor',
        'best_params': search.best_params_,
        'MAE': mean_absolute_error(y_test, preds),
        'R2': r2_score(y_test, preds)
    }

    return best_model, metrics


def save_artifacts(model, metrics, freq_map, reference_columns, models_dir='../models'):
    """
    Saves model, metrics, freq_map, and reference_columns to disk.
    """
    joblib.dump(model, f'{models_dir}/best_model.pkl')

    with open(f'{models_dir}/model_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)

    with open(f'{models_dir}/model_freq_map.json', 'w') as f:
        json.dump(freq_map, f, indent=4)

    with open(f'{models_dir}/reference_columns.json', 'w') as f:
        json.dump(reference_columns, f, indent=4)


def run_pipeline(cleaned_csv_path=None, models_dir=None):
    """
    Full end-to-end pipeline: load data -> engineer features -> train/tune -> save.
    Call this to retrain the model from scratch.
    """
    if models_dir is None:
        models_dir = os.path.join(PROJECT_ROOT, 'models')

    X, y, freq_map, reference_columns = load_and_prepare_data(cleaned_csv_path)
    model, metrics = train_and_tune(X, y)
    save_artifacts(model, metrics, freq_map, reference_columns, models_dir=models_dir)

    print('Training complete.')
    print('MAE:', metrics['MAE'])
    print('R2:', metrics['R2'])

    return model, metrics



if __name__ == '__main__':
    run_pipeline()
    