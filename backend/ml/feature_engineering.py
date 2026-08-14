"""
Feature engineering pipeline for car price prediction.
Converts raw/cleaned car data into the encoded feature set used for model training and inference.
"""

import pandas as pd


# Columns one-hot encoded during training — used to keep train/inference schema consistent
CATEGORICAL_COLS = ['brand', 'seller_type', 'fuel_type', 'transmission_type']

# Column that gets frequency-encoded instead of one-hot (too high cardinality)
HIGH_CARDINALITY_COL = 'model'


def add_model_frequency(df: pd.DataFrame, freq_map: dict = None) -> pd.DataFrame:
    """
    Adds a 'model_freq' column based on frequency of each car model.
    If freq_map is provided (e.g. from training data), uses it for consistent encoding
    at inference time. Otherwise computes frequency from the given df itself.
    """
    df = df.copy()
    if freq_map is None:
        freq_map = df[HIGH_CARDINALITY_COL].value_counts().to_dict()
    df['model_freq'] = df[HIGH_CARDINALITY_COL].map(freq_map).fillna(0)
    return df, freq_map


def encode_categoricals(df: pd.DataFrame, reference_columns: list = None) -> pd.DataFrame:
    """
    One-hot encodes brand, seller_type, fuel_type, transmission_type.
    If reference_columns is provided (i.e. the training feature columns),
    aligns the output to match exactly — adding missing dummy columns as 0
    and dropping any extras. This is essential at inference time so a single
    row doesn't produce a mismatched column set.
    """
    df = pd.get_dummies(df, columns=CATEGORICAL_COLS, drop_first=True)

    if reference_columns is not None:
        df = df.reindex(columns=reference_columns, fill_value=0)

    return df


def engineer_features(df: pd.DataFrame, freq_map: dict = None, reference_columns: list = None):
    """
    Full feature engineering pipeline.
    - df: cleaned raw dataframe (must contain 'model', 'brand', 'seller_type',
          'fuel_type', 'transmission_type', plus numeric columns)
    - freq_map: precomputed model->frequency dict (pass this at inference time,
          built from training data, so unseen/rare models get a sane fallback)
    - reference_columns: the exact training feature column list (pass at inference
          time to guarantee schema consistency)

    Returns: (encoded_df, freq_map) — freq_map is returned so it can be reused/saved.
    """
    df = df.copy()

    df, freq_map = add_model_frequency(df, freq_map=freq_map)
    df = df.drop(columns=[HIGH_CARDINALITY_COL])

    df = encode_categoricals(df, reference_columns=reference_columns)

    # Ensure any remaining bool columns (from get_dummies) are int
    bool_cols = df.select_dtypes(include='bool').columns
    df[bool_cols] = df[bool_cols].astype(int)

    return df, freq_map