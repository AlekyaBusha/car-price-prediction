"""
backend/services/dropdown_service.py

Provides dynamic dropdown values from the canonical dataset.

Dropdown dependency:
Brand
   ↓
Model
   ↓
Fuel Type
Transmission
Seller Type
Engine
Max Power
Seats
"""

from backend.utils.data_loader import data_loader


class DropdownService:

    def __init__(self):
        self.df = data_loader.df

    def reload_data(self):
        """Reload dataset from data_loader if underlying data changed."""
        data_loader.reload()
        self.df = data_loader.df

    # ==========================================================
    # Brand
    # ==========================================================

    def get_brands(self):
        return sorted(
            self.df["brand"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

    # ==========================================================
    # Model based on Brand
    # ==========================================================

    def get_models(self, brand):
        brand_clean = str(brand).strip().lower()
        df = self.df[
            self.df["brand"].astype(str).str.strip().str.lower() == brand_clean
        ]

        return sorted(
            df["model"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

    # ==========================================================
    # Brand + Model filtering
    # ==========================================================

    def get_model_data(self, brand, model=None):
        brand_clean = str(brand).strip().lower()
        b_df = self.df[
            self.df["brand"].astype(str).str.strip().str.lower() == brand_clean
        ]

        if not model or str(model).strip() == "":
            return b_df

        model_clean = str(model).strip().lower()
        m_df = b_df[
            b_df["model"].astype(str).str.strip().str.lower() == model_clean
        ]

        return m_df if not m_df.empty else b_df


    # ==========================================================
    # Fuel Types
    # ==========================================================

    def get_fuel_types(self, brand, model):
        df = self.get_model_data(brand, model)

        return sorted(
            df["fuel_type"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

    # ==========================================================
    # Transmission Types
    # ==========================================================

    def get_transmission_types(self, brand, model):
        df = self.get_model_data(brand, model)

        return sorted(
            df["transmission_type"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

    # ==========================================================
    # Seller Types
    # ==========================================================

    def get_seller_types(self, brand, model):
        df = self.get_model_data(brand, model)

        return sorted(
            df["seller_type"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

    # ==========================================================
    # Engines
    # ==========================================================

    def get_engines(self, brand, model):
        df = self.get_model_data(brand, model)

        return sorted(
            df["engine"]
            .dropna()
            .astype(int)
            .unique()
            .tolist()
        )

    # ==========================================================
    # Max Power
    # ==========================================================

    def get_max_powers(self, brand, model):
        df = self.get_model_data(brand, model)

        return sorted(
            df["max_power"]
            .dropna()
            .astype(float)
            .unique()
            .tolist()
        )

    # ==========================================================
    # Seats
    # ==========================================================

    def get_seats(self, brand, model):
        df = self.get_model_data(brand, model)

        return sorted(
            df["seats"]
            .dropna()
            .astype(int)
            .unique()
            .tolist()
        )

    # ==========================================================
    # Valid Engine + Max Power + Seats combinations
    # ==========================================================

    def get_vehicle_spec_combinations(self, brand, model):
        df = self.get_model_data(brand, model)

        columns = [
            "engine",
            "max_power",
            "seats"
        ]

        combinations = (
            df[columns]
            .dropna()
            .drop_duplicates()
            .sort_values(by=columns)
        )

        return combinations.to_dict(orient="records")


# ==========================================================
# Global Service Instance
# ==========================================================

dropdown_service = DropdownService()