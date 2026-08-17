"""
Prepare the variant-aware car price dataset for model training.

Input:
    backend/data/processed/car_price_variant_dataset.csv

Output:
    backend/data/processed/car_price_variant_training.csv
"""

from pathlib import Path

import pandas as pd


# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

INPUT_FILE = (
    PROJECT_ROOT
    / "backend"
    / "data"
    / "processed"
    / "car_price_variant_dataset.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "backend"
    / "data"
    / "processed"
    / "car_price_variant_training.csv"
)


def prepare_dataset():

    print("=" * 60)
    print("PREPARING VARIANT TRAINING DATASET")
    print("=" * 60)

    # ------------------------------------------------------
    # Load dataset
    # ------------------------------------------------------

    df = pd.read_csv(INPUT_FILE)

    original_rows = len(df)

    print(f"\nOriginal rows: {original_rows:,}")

    # ------------------------------------------------------
    # Remove duplicate rows
    # ------------------------------------------------------

    df = df.drop_duplicates()

    # ------------------------------------------------------
    # Remove rows missing critical fields
    # ------------------------------------------------------

    required_columns = [
        "brand",
        "model",
        "variant",
        "year",
        "fuel_type",
        "transmission_type",
        "km_driven",
        "selling_price",
        "seats",
        "max_power",
        "vehicle_age",
    ]

    df = df.dropna(subset=required_columns)

    # ------------------------------------------------------
    # Fill missing engine type
    # ------------------------------------------------------

    df["engine_type"] = (
        df["engine_type"]
        .fillna("unknown")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # ------------------------------------------------------
    # Normalize categorical text
    # ------------------------------------------------------

    categorical_columns = [
        "brand",
        "model",
        "variant",
        "fuel_type",
        "transmission_type",
    ]

    for column in categorical_columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .str.lower()
        )

    # ------------------------------------------------------
    # Ensure numeric columns are numeric
    # ------------------------------------------------------

    numeric_columns = [
        "year",
        "km_driven",
        "selling_price",
        "seats",
        "max_power",
        "vehicle_age",
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df = df.dropna(subset=numeric_columns)

    # ------------------------------------------------------
    # Basic validity rules
    # ------------------------------------------------------

    df = df[
        (df["selling_price"] > 0)
        & (df["km_driven"] >= 0)
        & (df["max_power"] > 0)
        & (df["seats"] > 0)
        & (df["vehicle_age"] >= 0)
    ]

    # ------------------------------------------------------
    # Remove obvious price corruption
    #
    # We keep legitimate luxury vehicles.
    # The analysis showed one extreme Ford EcoSport value
    # around ₹550 million, which is clearly erroneous.
    # ------------------------------------------------------

    df = df[
        df["selling_price"] <= 100_000_000
    ]

    # ------------------------------------------------------
    # Remove extreme odometer errors
    #
    # Values above 500,000 km are treated as unreliable
    # odometer records for this training dataset.
    # ------------------------------------------------------

    df = df[
        df["km_driven"] <= 500_000
    ]

    # ------------------------------------------------------
    # Final duplicate check
    # ------------------------------------------------------

    df = df.drop_duplicates()

    # ------------------------------------------------------
    # Reset index
    # ------------------------------------------------------

    df = df.reset_index(drop=True)

    # ------------------------------------------------------
    # Save training dataset
    # ------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    removed_rows = original_rows - len(df)

    print(f"Final rows   : {len(df):,}")
    print(f"Removed rows : {removed_rows:,}")

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nUnique values:")
    print(f"Brands   : {df['brand'].nunique()}")
    print(f"Models   : {df['model'].nunique()}")
    print(f"Variants : {df['variant'].nunique()}")

    print("\nSelling price:")
    print(df["selling_price"].describe())

    print("\nKM driven:")
    print(df["km_driven"].describe())

    print("\nMax power:")
    print(df["max_power"].describe())

    print("\nOutput:")
    print(OUTPUT_FILE)

    print("\n" + "=" * 60)
    print("DATASET PREPARATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    prepare_dataset()