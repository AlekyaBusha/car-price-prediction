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
# Known Canonical Categories for Normalization
# ==========================================================

CANONICAL_BRANDS = {
    "bmw": "BMW",
    "bentley": "Bentley",
    "datsun": "Datsun",
    "ferrari": "Ferrari",
    "force": "Force",
    "ford": "Ford",
    "honda": "Honda",
    "hyundai": "Hyundai",
    "isuzu": "Isuzu",
    "jaguar": "Jaguar",
    "jeep": "Jeep",
    "kia": "Kia",
    "land rover": "Land Rover",
    "lexus": "Lexus",
    "mg": "MG",
    "mahindra": "Mahindra",
    "maruti": "Maruti",
    "maserati": "Maserati",
    "mercedes-amg": "Mercedes-AMG",
    "mercedes-benz": "Mercedes-Benz",
    "mercedes benz": "Mercedes-Benz",
    "mini": "Mini",
    "nissan": "Nissan",
    "porsche": "Porsche",
    "renault": "Renault",
    "rolls-royce": "Rolls-Royce",
    "rolls royce": "Rolls-Royce",
    "skoda": "Skoda",
    "tata": "Tata",
    "toyota": "Toyota",
    "volkswagen": "Volkswagen",
    "volvo": "Volvo"
}

CANONICAL_FUEL_TYPES = {
    "petrol": "Petrol",
    "diesel": "Diesel",
    "cng": "CNG",
    "lpg": "LPG",
    "electric": "Electric"
}

CANONICAL_TRANSMISSIONS = {
    "manual": "Manual",
    "automatic": "Automatic"
}

CANONICAL_SELLER_TYPES = {
    "individual": "Individual",
    "dealer": "Dealer",
    "trustmark dealer": "Trustmark Dealer"
}

# Dataset medians/modes for fallback imputation of optional fields
DEFAULT_NUMERIC_IMPUTATION = {
    "engine": 1248.0,
    "max_power": 88.5,
    "seats": 5.0,
    "vehicle_age": 0.0,
    "km_driven": 0.0,
    "mileage": 19.67,
    "model_freq": 0.0
}


# ==========================================================
# Normalize Input Categories
# ==========================================================

def normalize_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalizes categorical inputs to match canonical dataset casing
    while safely preserving unseen category values.
    """
    df = df.copy()

    if "brand" in df.columns:
        df["brand"] = df["brand"].apply(
            lambda v: CANONICAL_BRANDS.get(str(v).strip().lower(), str(v).strip()) if pd.notna(v) else ""
        )

    if "fuel_type" in df.columns:
        df["fuel_type"] = df["fuel_type"].apply(
            lambda v: CANONICAL_FUEL_TYPES.get(str(v).strip().lower(), str(v).strip()) if pd.notna(v) else "Petrol"
        )

    if "transmission_type" in df.columns:
        df["transmission_type"] = df["transmission_type"].apply(
            lambda v: CANONICAL_TRANSMISSIONS.get(str(v).strip().lower(), str(v).strip()) if pd.notna(v) else "Manual"
        )

    if "seller_type" in df.columns:
        df["seller_type"] = df["seller_type"].apply(
            lambda v: CANONICAL_SELLER_TYPES.get(str(v).strip().lower(), str(v).strip()) if pd.notna(v) else "Individual"
        )

    return df


# ==========================================================
# Model Frequency Encoding
# ==========================================================

def add_model_frequency(
    df: pd.DataFrame,
    freq_map: dict = None
) -> pd.DataFrame:
    """
    Adds a model frequency encoded column.

    If freq_map is provided, performs case-insensitive lookup.
    Unseen models, empty models, or 'No models' safely receive model_freq = 0.0.
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
            .fillna(0.0)
        )
    else:
        # Create case-insensitive frequency map
        freq_map_lower = {
            str(k).strip().lower(): float(v)
            for k, v in freq_map.items()
        }

        def get_freq(model_val):
            if pd.isna(model_val):
                return 0.0
            clean_m = str(model_val).strip().lower()
            if clean_m in ["", "no models", "unknown", "none"]:
                return 0.0
            return freq_map_lower.get(clean_m, 0.0)

        df["model_freq"] = df[HIGH_CARDINALITY_COL].apply(get_freq)

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

    During inference (when reference_columns is provided):
    - Uses drop_first=False to generate one-hot flags for the present categories
    - Reindexes against reference_columns with fill_value=0 to match exact training schema
    - Unseen categories or dropped base levels cleanly map to 0 across reference columns
    """
    df = df.copy()

    # Ensure categorical columns exist
    for column in CATEGORICAL_COLS:
        if column not in df.columns:
            df[column] = ""

    # One-hot encoding
    is_inference = reference_columns is not None
    df = pd.get_dummies(
        df,
        columns=CATEGORICAL_COLS,
        drop_first=(not is_inference)
    )

    # Convert boolean columns to integers
    bool_cols = df.select_dtypes(include="bool").columns
    if len(bool_cols) > 0:
        df[bool_cols] = df[bool_cols].astype(int)

    # Match training feature columns
    if reference_columns is not None:
        df = df.reindex(
            columns=reference_columns,
            fill_value=0
        )

    return df


# ==========================================================
# Convert & Impute Numeric Columns
# ==========================================================

def ensure_numeric_columns(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Ensures all numeric model features are numeric and free of NaNs.
    Imputes safe defaults for optional missing numeric features.
    """
    df = df.copy()

    for column in NUMERIC_COLS:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )
            # Impute missing or invalid numeric values with default
            default_val = DEFAULT_NUMERIC_IMPUTATION.get(column, 0.0)
            df[column] = df[column].fillna(default_val)
        else:
            default_val = DEFAULT_NUMERIC_IMPUTATION.get(column, 0.0)
            df[column] = default_val

    if "model_freq" in df.columns:
        df["model_freq"] = pd.to_numeric(
            df["model_freq"],
            errors="coerce"
        ).fillna(0.0)

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
    1. Categorical normalization (case-insensitive canonical mapping)
    2. Model frequency encoding (unseen models -> 0.0)
    3. Remove original high-cardinality model column
    4. One-hot encode categorical columns (aligned to reference_columns)
    5. Convert and impute numeric columns
    6. Ensure exact training column order and data types

    Returns:
        encoded_df : pd.DataFrame
        freq_map   : dict
    """
    df = df.copy()

    # Step 1: Normalize categories
    df = normalize_categories(df)

    # Step 2: Model frequency encoding
    df, freq_map = add_model_frequency(
        df,
        freq_map=freq_map
    )

    # Step 3: Remove original model column if present
    if HIGH_CARDINALITY_COL in df.columns:
        df = df.drop(columns=[HIGH_CARDINALITY_COL])

    # Step 4: Encode categorical columns
    df = encode_categoricals(
        df,
        reference_columns=reference_columns
    )

    # Step 5: Ensure numeric columns and impute missing optional values
    df = ensure_numeric_columns(df)

    # Step 6: Convert all columns to float numeric
    df = df.apply(pd.to_numeric, errors="coerce").fillna(0.0)

    # Step 7: Final schema and column order check
    if reference_columns is not None:
        df = df[reference_columns]

    object_cols = df.select_dtypes(include="object").columns
    if len(object_cols) > 0:
        raise ValueError(
            f"Object dtype columns remain after feature engineering: {list(object_cols)}"
        )

    return df, freq_map