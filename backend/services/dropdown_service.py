"""
backend/services/dropdown_service.py

Provides dynamic dropdown values from the dataset.

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

    # ==========================================================
    # Brand
    # ==========================================================

    def get_brands(self):

        return sorted(
            self.df["brand"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    # ==========================================================
    # Model based on Brand
    # ==========================================================

    def get_models(self, brand):

        df = self.df[
            self.df["brand"].astype(str) == str(brand)
        ]

        return sorted(
            df["model"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    # ==========================================================
    # Brand + Model filtering
    # ==========================================================

    def get_model_data(self, brand, model):

        return self.df[
            (self.df["brand"].astype(str) == str(brand))
            &
            (self.df["model"].astype(str) == str(model))
        ]

    # ==========================================================
    # Fuel Types
    # ==========================================================

    def get_fuel_types(self, brand, model):

        df = self.get_model_data(
            brand,
            model
        )

        return sorted(
            df["fuel_type"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    # ==========================================================
    # Transmission Types
    # ==========================================================

    def get_transmission_types(
        self,
        brand,
        model
    ):

        df = self.get_model_data(
            brand,
            model
        )

        return sorted(
            df["transmission_type"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    # ==========================================================
    # Seller Types
    # ==========================================================

    def get_seller_types(
        self,
        brand,
        model
    ):

        df = self.get_model_data(
            brand,
            model
        )

        return sorted(
            df["seller_type"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    # ==========================================================
    # Engines
    # ==========================================================

    def get_engines(
        self,
        brand,
        model
    ):

        df = self.get_model_data(
            brand,
            model
        )

        return sorted(
            df["engine"]
            .dropna()
            .unique()
            .tolist()
        )

    # ==========================================================
    # Max Power
    # ==========================================================

    def get_max_powers(
        self,
        brand,
        model
    ):

        df = self.get_model_data(
            brand,
            model
        )

        return sorted(
            df["max_power"]
            .dropna()
            .unique()
            .tolist()
        )

    # ==========================================================
    # Seats
    # ==========================================================

    def get_seats(
        self,
        brand,
        model
    ):

        df = self.get_model_data(
            brand,
            model
        )

        return sorted(
            df["seats"]
            .dropna()
            .unique()
            .tolist()
        )

    # ==========================================================
    # Valid Engine + Max Power + Seats combinations
    # ==========================================================

    def get_vehicle_spec_combinations(
        self,
        brand,
        model
    ):

        df = self.get_model_data(
            brand,
            model
        )

        columns = [
            "engine",
            "max_power",
            "seats"
        ]

        # Keep only rows where all three values exist
        combinations = (
            df[columns]
            .dropna()
            .drop_duplicates()
            .sort_values(
                by=columns
            )
        )

        return combinations.to_dict(
            orient="records"
        )


# ==========================================================
# Global Service Instance
# ==========================================================

dropdown_service = DropdownService()