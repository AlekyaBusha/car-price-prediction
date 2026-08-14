"""
backend/utils/helpers.py

Common API response helper.
"""


def success_response(message: str, data):

    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(message: str):

    return {
        "success": False,
        "message": message,
        "data": None
    }