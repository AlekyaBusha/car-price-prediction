"""
backend/api/schemas.py

Defines request and response models for the FastAPI backend.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


# ==========================================================
# Input Schema
# ==========================================================

class CarInput(BaseModel):
    """
    User input for prediction.
    """

    # ----------------------------
    # Mandatory Fields
    # ----------------------------

    brand: str = Field(..., description="Car Brand")

    model: str = Field(..., description="Car Model")

    fuel_type: str = Field(..., description="Fuel Type")

    transmission_type: str = Field(..., description="Transmission Type")

    # ----------------------------
    # Optional Fields
    # ----------------------------

    seller_type: Optional[str] = Field(
        default=None,
        description="Seller Type"
    )

    engine: Optional[float] = Field(
        default=None,
        description="Engine CC"
    )

    max_power: Optional[float] = Field(
        default=None,
        description="Max Power"
    )

    seats: Optional[int] = Field(
        default=None,
        description="Number of Seats"
    )

    vehicle_age: Optional[float] = Field(
        default=None,
        description="Vehicle Age"
    )

    km_driven: Optional[float] = Field(
        default=None,
        description="Kilometers Driven"
    )

    mileage: Optional[float] = Field(
        default=None,
        description="Mileage"
    )


# ==========================================================
# Prediction Response
# ==========================================================

class PredictionResponse(BaseModel):

    success: bool

    predicted_price: float

    currency: str = "INR"


# ==========================================================
# AI Suggestion Models
# ==========================================================

class Recommendation(BaseModel):

    value: str | int | float

    predicted_price: float


class Suggestion(BaseModel):

    field: str

    message: str

    recommendations: List[Recommendation]


class SuggestionResponse(BaseModel):

    success: bool

    suggestions: List[Suggestion]