"""
backend/utils/data_loader.py

Loads the cleaned dataset once.
"""

from pathlib import Path
import pandas as pd


class DataLoader:

    def __init__(self):

        data_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "processed"
            / "cleaned_car_data.csv"
        )

        self.df = pd.read_csv(data_path)


data_loader = DataLoader()