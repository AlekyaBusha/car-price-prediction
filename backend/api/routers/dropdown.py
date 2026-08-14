"""
backend/api/routers/dropdown.py

APIs for loading dropdown values.
"""

from fastapi import APIRouter

from backend.services.dropdown_service import dropdown_service

router = APIRouter(
    prefix="/dropdown",
    tags=["Dropdown"]
)


@router.get("/brands")
def get_brands():
    return {
        "brands": dropdown_service.get_brands()
    }


@router.get("/models/{brand}")
def get_models(brand: str):
    return {
        "models": dropdown_service.get_models(brand)
    }


@router.get("/fuel-types")
def get_fuel_types():
    return {
        "fuel_types": dropdown_service.get_fuel_types()
    }


@router.get("/transmissions")
def get_transmissions():
    return {
        "transmission_types": dropdown_service.get_transmission_types()
    }


@router.get("/seller-types")
def get_seller_types():
    return {
        "seller_types": dropdown_service.get_seller_types()
    }


@router.get("/engines")
def get_engines():
    return {
        "engines": dropdown_service.get_engines()
    }


@router.get("/seats")
def get_seats():
    return {
        "seats": dropdown_service.get_seats()
    }


@router.get("/max-powers")
def get_max_powers():
    return {
        "max_powers": dropdown_service.get_max_powers()
    }