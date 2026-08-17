"""
Feature engineering pipeline for the variant-aware car price model.

This pipeline is separate from the existing production model pipeline.
It preserves the vehicle variant as an important prediction feature.
"""

import pandas as pd


# ==========================================================
# Categorical Features
# ==========================================================

CATEGORICAL_COLUMNS = [
    "brand",
    "model",
    "variant",
    "fuel_type",
    "transmission_type",
    "engine_type",
]


# ==========================================================
# Numerical Features
# ==========================================================

NUMERICAL_COLUMNS = [
    "year",
    "vehicle_age",
    "km_driven",
    "mileage",
    "seats",
    "max_power",
]


# ==========================================================
# Feature Engineering
# ==========================================================

def engineer_variant_features(
    df: pd.DataFrame,
    reference_columns: list = None
):
    """
    Convert the cleaned variant dataset into
    model-ready numerical features.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned car dataset.

    reference_columns : list, optional
        Feature columns saved during training.
        Used during inference to guarantee
        identical train/inference schema.

    Returns
    -------
    encoded_df : pd.DataFrame
        Model-ready feature dataframe.

    reference_columns : list
        Final feature column list.
    """

    df = df.copy()

    # ======================================================
    # Ensure categorical columns exist
    # ======================================================

    for column in CATEGORICAL_COLUMNS:

        if column not in df.columns:
            df[column] = "unknown"

        df[column] = (
            df[column]
            .fillna("unknown")
            .astype(str)
            .str.strip()
            .str.lower()
        )

    # ======================================================
    # Ensure numerical columns are numeric
    # ======================================================

    for column in NUMERICAL_COLUMNS:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # ======================================================
    # One-hot encode categorical features
    # ======================================================

    encoded_df = pd.get_dummies(
        df,
        columns=CATEGORICAL_COLUMNS,
        drop_first=False
    )

    # ======================================================
    # Convert boolean columns to integers
    # ======================================================

    bool_columns = encoded_df.select_dtypes(
        include="bool"
    ).columns

    if len(bool_columns) > 0:

        encoded_df[bool_columns] = (
            encoded_df[bool_columns]
            .astype(int)
        )

    # ======================================================
    # Match training columns during inference
    # ======================================================

    if reference_columns is not None:

        encoded_df = encoded_df.reindex(
            columns=reference_columns,
            fill_value=0
        )

    # ======================================================
    # Final numeric conversion
    # ======================================================

    encoded_df = encoded_df.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # ======================================================
    # Handle remaining missing numeric values
    # ======================================================

    encoded_df = encoded_df.fillna(0)

    # ======================================================
    # Validate object columns
    # ======================================================

    object_columns = encoded_df.select_dtypes(
        include="object"
    ).columns

    if len(object_columns) > 0:

        raise ValueError(
            "Object dtype columns remain: "
            f"{list(object_columns)}"
        )

    # ======================================================
    # Save reference columns
    # ======================================================

    if reference_columns is None:

        reference_columns = encoded_df.columns.tolist()

    return encoded_df, reference_columns