"""
backend/tests/validate_dropdowns.py

Automated Dropdown Validation Test
Iterates over every real Brand + Model combination and compares:
DATASET VALUES vs API/DropdownService VALUES
for:
- Fuel Type
- Transmission
- Seller Type
- Engine
- Max Power
- Seats
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from backend.services.dropdown_service import dropdown_service

def validate_all_dropdowns():
    print("=" * 70)
    print("PHASE 9: AUTOMATED DROPDOWN VALIDATION")
    print("=" * 70)

    dropdown_service.reload_data()
    df = dropdown_service.df
    brands = dropdown_service.get_brands()

    print(f"Total Brands in Canonical Dataset: {len(brands)}")
    print(f"Brands: {brands}")

    total_combinations = 0
    mismatches = []
    seat_audit_models_gt_5 = []

    for brand in brands:
        models = dropdown_service.get_models(brand)
        if not models:
            mismatches.append({
                "brand": brand,
                "model": "N/A",
                "field": "models",
                "dataset": "non-empty",
                "service": "empty"
            })
            continue

        for model in models:
            total_combinations += 1
            df_sub = df[
                (df["brand"].astype(str).str.strip().str.lower() == str(brand).strip().lower())
                &
                (df["model"].astype(str).str.strip().str.lower() == str(model).strip().lower())
            ]

            # 1. Fuel Type
            expected_fuels = sorted(df_sub["fuel_type"].dropna().astype(str).str.strip().unique().tolist())
            actual_fuels = dropdown_service.get_fuel_types(brand, model)
            if expected_fuels != actual_fuels:
                mismatches.append({
                    "brand": brand, "model": model, "field": "Fuel Type",
                    "dataset": expected_fuels, "service": actual_fuels
                })

            # 2. Transmission
            expected_trans = sorted(df_sub["transmission_type"].dropna().astype(str).str.strip().unique().tolist())
            actual_trans = dropdown_service.get_transmission_types(brand, model)
            if expected_trans != actual_trans:
                mismatches.append({
                    "brand": brand, "model": model, "field": "Transmission",
                    "dataset": expected_trans, "service": actual_trans
                })

            # 3. Seller Type
            expected_sellers = sorted(df_sub["seller_type"].dropna().astype(str).str.strip().unique().tolist())
            actual_sellers = dropdown_service.get_seller_types(brand, model)
            if expected_sellers != actual_sellers:
                mismatches.append({
                    "brand": brand, "model": model, "field": "Seller Type",
                    "dataset": expected_sellers, "service": actual_sellers
                })

            # 4. Engine
            expected_engines = sorted(df_sub["engine"].dropna().astype(int).unique().tolist())
            actual_engines = dropdown_service.get_engines(brand, model)
            if expected_engines != actual_engines:
                mismatches.append({
                    "brand": brand, "model": model, "field": "Engine",
                    "dataset": expected_engines, "service": actual_engines
                })

            # 5. Max Power
            expected_powers = sorted(df_sub["max_power"].dropna().astype(float).unique().tolist())
            actual_powers = dropdown_service.get_max_powers(brand, model)
            if expected_powers != actual_powers:
                mismatches.append({
                    "brand": brand, "model": model, "field": "Max Power",
                    "dataset": expected_powers, "service": actual_powers
                })

            # 6. Seats
            expected_seats = sorted(df_sub["seats"].dropna().astype(int).unique().tolist())
            actual_seats = dropdown_service.get_seats(brand, model)
            if expected_seats != actual_seats:
                mismatches.append({
                    "brand": brand, "model": model, "field": "Seats",
                    "dataset": expected_seats, "service": actual_seats
                })

            if any(s > 5 for s in expected_seats):
                seat_audit_models_gt_5.append({
                    "brand": brand,
                    "model": model,
                    "seats": expected_seats
                })

    print(f"\nTotal Brand + Model Combinations Validated: {total_combinations}")
    print(f"Total Mismatches Found: {len(mismatches)}")

    print("\n" + "=" * 70)
    print("SEAT AUDIT: MODELS WITH > 5 SEATS")
    print("=" * 70)
    for item in seat_audit_models_gt_5:
        print(f"Brand: {item['brand']:<15} | Model: {item['model']:<20} | Seats: {item['seats']}")

    print("\n" + "=" * 70)
    if not mismatches:
        print("RESULT: ALL DROPDOWN VALIDATIONS PASSED (100% MATCH)")
        print("=" * 70)
        return True
    else:
        print(f"RESULT: {len(mismatches)} MISMATCHES DETECTED!")
        for m in mismatches[:10]:
            print(f"FAIL: {m['brand']} {m['model']} [{m['field']}] Expected: {m['dataset']} != Service: {m['service']}")
        print("=" * 70)
        return False

if __name__ == "__main__":
    success = validate_all_dropdowns()
    if not success:
        sys.exit(1)
