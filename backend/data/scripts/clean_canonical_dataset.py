"""
backend/data/scripts/clean_canonical_dataset.py

Cleans the raw cardekho_dataset.csv and generates the canonical
cleaned_car_data.csv with all 32 real brands and valid seat counts.
"""

from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DATA_PATH = PROJECT_ROOT / "backend" / "data" / "raw" / "car dataset" / "cardekho_dataset.csv"
OUTPUT_DATA_PATH = PROJECT_ROOT / "backend" / "data" / "processed" / "cleaned_car_data.csv"

def clean_data():
    print("=" * 70)
    print("CANONICAL DATA CLEANING")
    print("=" * 70)

    df = pd.read_csv(RAW_DATA_PATH)
    initial_rows = len(df)
    print(f"Raw rows loaded: {initial_rows:,}")

    # Drop index column if present
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # 1. Clean string columns: trim whitespace
    string_cols = ["brand", "model", "seller_type", "fuel_type", "transmission_type"]
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # 2. Standardize brand casing & names
    brand_mapping = {
        "ISUZU": "Isuzu",
    }
    df["brand"] = df["brand"].replace(brand_mapping)

    # 3. Clean numeric columns
    numeric_cols = ["vehicle_age", "km_driven", "mileage", "engine", "max_power", "seats", "selling_price"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 4. Handle invalid seats (seats == 0 or seats NaN)
    # Honda City is 5 seater, Nissan Kicks is 5 seater
    seats_zero_mask = (df["seats"] <= 0) | df["seats"].isna()
    if seats_zero_mask.sum() > 0:
        print(f"Fixing {seats_zero_mask.sum()} invalid seat records (setting to model mode/5)")
        df.loc[seats_zero_mask, "seats"] = 5

    df["seats"] = df["seats"].astype(int)

    # 5. Filter invalid numeric values
    df = df[
        (df["selling_price"] > 0) &
        (df["km_driven"] >= 0) &
        (df["vehicle_age"] >= 0) &
        (df["engine"] > 0) &
        (df["max_power"] > 0) &
        (df["seats"] > 0)
    ]

    # 6. Drop duplicates
    before_dedup = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before_dedup - len(df)
    print(f"Duplicates removed: {duplicates_removed:,}")

    # Ensure engine and vehicle_age are int where appropriate
    df["engine"] = df["engine"].astype(int)
    df["vehicle_age"] = df["vehicle_age"].astype(int)
    df["km_driven"] = df["km_driven"].astype(int)
    df["selling_price"] = df["selling_price"].astype(int)

    # Reorder columns to standard schema
    cols_order = [
        "brand", "model", "vehicle_age", "km_driven", "seller_type",
        "fuel_type", "transmission_type", "mileage", "engine",
        "max_power", "seats", "selling_price"
    ]
    df = df[[c for c in cols_order if c in df.columns]]

    print(f"\nFinal cleaned dataset rows: {len(df):,}")
    print(f"Brands count: {df['brand'].nunique()}")
    print(f"Unique Brands: {sorted(df['brand'].unique().tolist())}")
    print(f"Unique Seats: {sorted(df['seats'].unique().tolist())}")

    OUTPUT_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_DATA_PATH, index=False)
    print(f"Saved canonical dataset to: {OUTPUT_DATA_PATH}")
    print("=" * 70)

if __name__ == "__main__":
    clean_data()
