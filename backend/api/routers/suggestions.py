"""
backend/api/routers/suggestions.py

API for AI Suggestions.
"""

from fastapi import APIRouter

from backend.api.schemas import CarInput
from backend.services.suggestion_service import suggestion_service

router = APIRouter(
    prefix="/suggestions",
    tags=["AI Suggestions"]
)


@router.post("/")
def generate_suggestions(car: CarInput):

    car_data = car.model_dump(exclude_none=True)

    suggestions = suggestion_service.generate(car_data)

    return {
        "success": True,
        "suggestions": suggestions
    }