"""
backend/api/routers/dropdown.py

APIs for dynamic dependent dropdowns.
"""

from fastapi import APIRouter

from backend.services.dropdown_service import dropdown_service


router = APIRouter(
    prefix="/dropdown",
    tags=["Dropdown"]
)


# ==========================================================
# Brands
# ==========================================================

@router.get("/brands")
def get_brands():

    return {
        "brands": dropdown_service.get_brands()
    }


# ==========================================================
# Models
# ==========================================================

@router.get("/models/{brand}")
def get_models(brand: str):

    return {
        "models": dropdown_service.get_models(brand)
    }


# ==========================================================
# Fuel Types
# ==========================================================

@router.get("/fuel-types/{brand}/{model}")
def get_fuel_types(
    brand: str,
    model: str
):

    return {
        "fuel_types":
            dropdown_service.get_fuel_types(
                brand,
                model
            )
    }


# ==========================================================
# Transmissions
# ==========================================================

@router.get("/transmissions/{brand}/{model}")
def get_transmissions(
    brand: str,
    model: str
):

    return {
        "transmission_types":
            dropdown_service.get_transmission_types(
                brand,
                model
            )
    }


# ==========================================================
# Seller Types
# ==========================================================

@router.get("/seller-types/{brand}/{model}")
def get_seller_types(
    brand: str,
    model: str
):

    return {
        "seller_types":
            dropdown_service.get_seller_types(
                brand,
                model
            )
    }


# ==========================================================
# Engines
# ==========================================================

@router.get("/engines/{brand}/{model}")
def get_engines(
    brand: str,
    model: str
):

    return {
        "engines":
            dropdown_service.get_engines(
                brand,
                model
            )
    }


# ==========================================================
# Max Powers
# ==========================================================

@router.get("/max-powers/{brand}/{model}")
def get_max_powers(
    brand: str,
    model: str
):

    return {
        "max_powers":
            dropdown_service.get_max_powers(
                brand,
                model
            )
    }


# ==========================================================
# Seats
# ==========================================================

@router.get("/seats/{brand}/{model}")
def get_seats(
    brand: str,
    model: str
):

    return {
        "seats":
            dropdown_service.get_seats(
                brand,
                model
            )
    }