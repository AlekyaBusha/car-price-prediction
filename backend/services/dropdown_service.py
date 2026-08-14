"""
backend/services/dropdown_service.py

Provides dynamic dropdown values from the dataset.
"""
from backend.utils.data_loader import data_loader

class DropdownService:

    def __init__(self):

        self.df = data_loader.df

    # -----------------------------------
    # Brand
    # -----------------------------------

    def get_brands(self):

        return sorted(
            self.df["brand"].dropna().unique().tolist()
        )

    # -----------------------------------
    # Model (Based on Brand)
    # -----------------------------------

    def get_models(self, brand):

        df = self.df[self.df["brand"] == brand]

        return sorted(
            df["model"].dropna().unique().tolist()
        )

    # -----------------------------------
    # Fuel Type
    # -----------------------------------

    def get_fuel_types(self):

        return sorted(
            self.df["fuel_type"].dropna().unique().tolist()
        )

    # -----------------------------------
    # Transmission
    # -----------------------------------

    def get_transmission_types(self):

        return sorted(
            self.df["transmission_type"].dropna().unique().tolist()
        )

    # -----------------------------------
    # Seller Type
    # -----------------------------------

    def get_seller_types(self):

        return sorted(
            self.df["seller_type"].dropna().unique().tolist()
        )

    # -----------------------------------
    # Engine
    # -----------------------------------

    def get_engines(self):

        return sorted(
            self.df["engine"].dropna().unique().tolist()
        )

    # -----------------------------------
    # Seats
    # -----------------------------------

    def get_seats(self):

        return sorted(
            self.df["seats"].dropna().unique().tolist()
        )

    # -----------------------------------
    # Max Power
    # -----------------------------------

    def get_max_powers(self):

        return sorted(
            self.df["max_power"].dropna().unique().tolist()
        )


dropdown_service = DropdownService()