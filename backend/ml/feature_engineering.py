"""
Feature engineering pipeline for car price prediction.

Converts raw/cleaned car data into the encoded feature set
used by model training and inference.
"""

import pandas as pd


# ==========================================================
# Categorical Columns
# ==========================================================

CATEGORICAL_COLS = [
    "brand",
    "seller_type",
    "fuel_type",
    "transmission_type"
]


# ==========================================================
# High Cardinality Column
# ==========================================================

HIGH_CARDINALITY_COL = "model"


# ==========================================================
# Numeric Columns
# ==========================================================

NUMERIC_COLS = [
    "engine",
    "max_power",
    "seats",
    "vehicle_age",
    "km_driven",
    "mileage"
]


# ==========================================================
# Model Frequency Encoding
# ==========================================================

def add_model_frequency(
    df: pd.DataFrame,
    freq_map: dict = None
) -> pd.DataFrame:

    """
    Adds a model frequency encoded column.

    If freq_map is provided, it is used for consistent
    inference-time encoding.
    """

    df = df.copy()

    if freq_map is None:

        freq_map = (
            df[HIGH_CARDINALITY_COL]
            .value_counts()
            .to_dict()
        )

    df["model_freq"] = (
        df[HIGH_CARDINALITY_COL]
        .map(freq_map)
        .fillna(0)
    )

    return df, freq_map


# ==========================================================
# Encode Categorical Columns
# ==========================================================

def encode_categoricals(
    df: pd.DataFrame,
    reference_columns: list = None
) -> pd.DataFrame:

    """
    One-hot encodes categorical columns.

    Ensures the final dataframe has the same
    feature columns as the training data.
    """

    df = df.copy()

    # ------------------------------------------------------
    # Make sure categorical columns exist
    # ------------------------------------------------------

    for column in CATEGORICAL_COLS:

        if column not in df.columns:

            df[column] = ""

    # ------------------------------------------------------
    # One-hot encoding
    # ------------------------------------------------------

    df = pd.get_dummies(
        df,
        columns=CATEGORICAL_COLS,
        drop_first=True
    )

    # ------------------------------------------------------
    # Convert boolean columns to integers
    # ------------------------------------------------------

    bool_cols = df.select_dtypes(
        include="bool"
    ).columns

    if len(bool_cols) > 0:

        df[bool_cols] = (
            df[bool_cols]
            .astype(int)
        )

    # ------------------------------------------------------
    # Match training feature columns
    # ------------------------------------------------------

    if reference_columns is not None:

        df = df.reindex(
            columns=reference_columns,
            fill_value=0
        )

    return df


# ==========================================================
# Convert Numeric Columns
# ==========================================================

def ensure_numeric_columns(
    df: pd.DataFrame
) -> pd.DataFrame:

    """
    Ensures all numeric model features are actually numeric.

    This prevents XGBoost errors caused by pandas object dtype.
    """

    df = df.copy()

    for column in NUMERIC_COLS:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


# ==========================================================
# Full Feature Engineering Pipeline
# ==========================================================

def engineer_features(
    df: pd.DataFrame,
    freq_map: dict = None,
    reference_columns: list = None
):

    """
    Full feature engineering pipeline.

    Steps:

    1. Model frequency encoding
    2. Remove original model column
    3. One-hot encode categorical columns
    4. Match training feature schema
    5. Convert numeric columns to numeric dtype

    Returns:
        encoded_df
        freq_map
    """

    df = df.copy()

    # ------------------------------------------------------
    # Step 1: Model frequency encoding
    # ------------------------------------------------------

    df, freq_map = add_model_frequency(
        df,
        freq_map=freq_map
    )

    # ------------------------------------------------------
    # Step 2: Remove original model column
    # ------------------------------------------------------

    df = df.drop(
        columns=[HIGH_CARDINALITY_COL]
    )

    # ------------------------------------------------------
    # Step 3: Encode categorical columns
    # ------------------------------------------------------

    df = encode_categoricals(
        df,
        reference_columns=reference_columns
    )

    # ------------------------------------------------------
    # Step 4: Ensure numeric columns
    # ------------------------------------------------------

    df = ensure_numeric_columns(
        df
    )

    # ------------------------------------------------------
    # Step 5: Ensure remaining boolean columns are integers
    # ------------------------------------------------------

    bool_cols = df.select_dtypes(
        include="bool"
    ).columns

    if len(bool_cols) > 0:

        df[bool_cols] = (
            df[bool_cols]
            .astype(int)
        )

    # ------------------------------------------------------
    # Step 6: Final dtype safety check
    # ------------------------------------------------------

    object_cols = df.select_dtypes(
        include="object"
    ).columns

    if len(object_cols) > 0:

        raise ValueError(
            "Object dtype columns remain after "
            "feature engineering: "
            f"{list(object_cols)}"
        )

    return df, freq_map