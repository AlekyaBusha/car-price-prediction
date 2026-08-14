"""
backend/utils/validators.py

Input validation helpers.
"""


def validate_prediction_input(car):

    required = [
        "brand",
        "model",
        "fuel_type",
        "transmission_type"
    ]

    missing = []

    for field in required:

        if field not in car or car[field] is None:
            missing.append(field)

    return missing