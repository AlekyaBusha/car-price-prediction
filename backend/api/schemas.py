"""
backend/api/schemas.py

Defines request and response models for the FastAPI backend.
"""

from typing import Optional, List, Union
from pydantic import BaseModel, Field


# ==========================================================
# Input Schema
# ==========================================================

class CarInput(BaseModel):
    """
    User input required for car price prediction.
    """

    # ------------------------------------------------------
    # Required Fields
    # ------------------------------------------------------

    brand: str = Field(
        ...,
        description="Car Brand"
    )

    model: Optional[str] = Field(
        default="",
        description="Car Model"
    )


    fuel_type: str = Field(
        ...,
        description="Fuel Type"
    )

    transmission_type: str = Field(
        ...,
        description="Transmission Type"
    )

    seller_type: str = Field(
        ...,
        description="Seller Type"
    )

    # ------------------------------------------------------
    # Optional Numeric Fields
    # ------------------------------------------------------

    engine: Optional[float] = Field(
        default=None,
        description="Engine CC"
    )

    max_power: Optional[float] = Field(
        default=None,
        description="Maximum Power in bhp"
    )

    seats: Optional[int] = Field(
        default=None,
        description="Number of Seats"
    )

    vehicle_age: Optional[float] = Field(
        default=0.0,
        description="Vehicle Age in Years"
    )

    km_driven: Optional[float] = Field(
        default=0.0,
        description="Kilometers Driven"
    )

    mileage: Optional[float] = Field(
        default=5.0,
        description="Mileage in km/l"
    )


# ==========================================================
# Price Range
# ==========================================================

class PriceRange(BaseModel):

    low: float

    predicted: float

    high: float


# ==========================================================
# Prediction Response
# ==========================================================

class PredictionResponse(BaseModel):

    success: bool

    predicted_price: float

    price_range: PriceRange

    currency: str = "INR"


# ==========================================================
# AI Suggestion Models
# ==========================================================

class Recommendation(BaseModel):

    value: Union[str, int, float]

    predicted_price: float


class Suggestion(BaseModel):

    field: str

    message: str

    recommendations: List[Recommendation]


class SuggestionResponse(BaseModel):

    success: bool

    suggestions: List[Suggestion]


# ==========================================================
# Variant Prediction Input
# ==========================================================

class VariantPredictionInput(BaseModel):
    brand: str
    model: str
    vehicle_age: float = 0.0
    km_driven: float = 0.0
    mileage: float = 5.0
    engine: Optional[float] = None
    seats: Optional[float] = None