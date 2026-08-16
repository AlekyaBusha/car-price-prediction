"""
Merge the existing car dataset and the variant dataset
into one unified training dataset.

The original datasets are never modified.
"""

from pathlib import Path

import pandas as pd


# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

CURRENT_DATASET = (
    PROJECT_ROOT
    / "backend"
    / "data"
    / "processed"
    / "cleaned_car_data.csv"
)

VARIANT_DATASET = (
    PROJECT_ROOT
    / "backend"
    / "data"
    / "processed"
    / "car_price_variant_training.csv"
)

OUTPUT_DATASET = (
    PROJECT_ROOT
    / "backend"
    / "data"
    / "processed"
    / "unified_car_price_dataset.csv"
)


# ==========================================================
# Common Schema
# ==========================================================

FINAL_COLUMNS = [
    "brand",
    "model",
    "variant",
    "fuel_type",
    "transmission_type",
    "year",
    "vehicle_age",
    "km_driven",
    "seats",
    "max_power",
    "engine_type",
    "selling_price",
]


# ==========================================================
# Helper
# ==========================================================

def normalize_text(df, columns):

    for column in columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .fillna("unknown")
                .astype(str)
                .str.strip()
                .str.lower()
            )

    return df


def normalize_numeric(df, columns):

    for column in columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


# ==========================================================
# Load Current Dataset
# ==========================================================

print("=" * 70)
print("MERGING CAR PRICE DATASETS")
print("=" * 70)

print("\nLoading current dataset...")

current = pd.read_csv(
    CURRENT_DATASET
)

print(
    f"Current dataset rows: {len(current):,}"
)

print(
    "Current columns:"
)

print(
    current.columns.tolist()
)


# ==========================================================
# Load Variant Dataset
# ==========================================================

print("\nLoading variant dataset...")

variant = pd.read_csv(
    VARIANT_DATASET
)

print(
    f"Variant dataset rows: {len(variant):,}"
)

print(
    "Variant columns:"
)

print(
    variant.columns.tolist()
)


# ==========================================================
# Normalize Current Dataset
# ==========================================================

print("\nPreparing current dataset...")


# ----------------------------------------------------------
# Rename possible existing column names
# ----------------------------------------------------------

rename_map = {

    "selling_price": "selling_price",
    "price": "selling_price",

    "fuel": "fuel_type",
    "fuelType": "fuel_type",

    "transmission": "transmission_type",

    "km": "km_driven",

    "myear": "year",

    "Seats": "seats",

    "Max Power Delivered": "max_power",

    "Engine Type": "engine_type",
}


current = current.rename(
    columns=rename_map
)


# ----------------------------------------------------------
# Add missing variant
# ----------------------------------------------------------

if "variant" not in current.columns:

    current["variant"] = "unknown"


# ----------------------------------------------------------
# Add missing engine type
# ----------------------------------------------------------

if "engine_type" not in current.columns:

    current["engine_type"] = "unknown"


# ----------------------------------------------------------
# Calculate vehicle age if necessary
# ----------------------------------------------------------

if (
    "vehicle_age" not in current.columns
    and "year" in current.columns
):

    current["vehicle_age"] = (
        2026 - pd.to_numeric(
            current["year"],
            errors="coerce"
        )
    )


# ==========================================================
# Normalize Variant Dataset
# ==========================================================

print("\nPreparing variant dataset...")


# The variant dataset already uses our normalized names.

if "variant" not in variant.columns:

    variant["variant"] = "unknown"


if "engine_type" not in variant.columns:

    variant["engine_type"] = "unknown"


# ==========================================================
# Ensure Required Columns Exist
# ==========================================================

for column in FINAL_COLUMNS:

    if column not in current.columns:

        current[column] = pd.NA

    if column not in variant.columns:

        variant[column] = pd.NA


# ==========================================================
# Select Common Schema
# ==========================================================

current = current[
    FINAL_COLUMNS
].copy()

variant = variant[
    FINAL_COLUMNS
].copy()


# ==========================================================
# Normalize Text
# ==========================================================

text_columns = [
    "brand",
    "model",
    "variant",
    "fuel_type",
    "transmission_type",
    "engine_type",
]


current = normalize_text(
    current,
    text_columns
)

variant = normalize_text(
    variant,
    text_columns
)


# ==========================================================
# Normalize Numeric Columns
# ==========================================================

numeric_columns = [
    "year",
    "vehicle_age",
    "km_driven",
    "seats",
    "max_power",
    "selling_price",
]


current = normalize_numeric(
    current,
    numeric_columns
)

variant = normalize_numeric(
    variant,
    numeric_columns
)


# ==========================================================
# Remove Invalid Rows
# ==========================================================

current = current[
    current["selling_price"].notna()
    & (current["selling_price"] > 0)
]

variant = variant[
    variant["selling_price"].notna()
    & (variant["selling_price"] > 0)
]


# ==========================================================
# Combine
# ==========================================================

print("\nCombining datasets...")

unified = pd.concat(
    [
        current,
        variant
    ],
    ignore_index=True
)


# ==========================================================
# Remove Duplicates
# ==========================================================

before_duplicates = len(unified)

unified = unified.drop_duplicates()

duplicates_removed = (
    before_duplicates - len(unified)
)


# ==========================================================
# Final Cleanup
# ==========================================================

unified = unified.reset_index(
    drop=True
)


# ==========================================================
# Save
# ==========================================================

OUTPUT_DATASET.parent.mkdir(
    parents=True,
    exist_ok=True
)

unified.to_csv(
    OUTPUT_DATASET,
    index=False
)


# ==========================================================
# Summary
# ==========================================================

print("\n" + "=" * 70)
print("UNIFIED DATASET CREATED")
print("=" * 70)

print(
    f"\nCurrent dataset rows : {len(current):,}"
)

print(
    f"Variant dataset rows : {len(variant):,}"
)

print(
    f"Duplicates removed   : {duplicates_removed:,}"
)

print(
    f"Final rows            : {len(unified):,}"
)

print(
    f"Final columns         : {len(unified.columns)}"
)

print("\nColumns:")

for column in unified.columns:

    print(
        f" - {column}"
    )


print("\nMissing values:")

print(
    unified.isnull().sum()
)


print("\nUnique values:")

print(
    f"Brands   : {unified['brand'].nunique()}"
)

print(
    f"Models   : {unified['model'].nunique()}"
)

print(
    f"Variants : {unified['variant'].nunique()}"
)


print("\nPrice statistics:")

print(
    unified["selling_price"].describe()
)


print("\nOutput:")

print(
    OUTPUT_DATASET
)

print(
    "\n" + "=" * 70
)
print("MERGE COMPLETE")
print("=" * 70)