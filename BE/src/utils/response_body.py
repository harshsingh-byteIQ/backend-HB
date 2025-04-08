from src.models.auth_modals import SuccessResponseModal , ErrorResponseModal
from typing import Any

def success_response(data: Any, message: str = "Request successful", status_code: int = 200):
    return SuccessResponseModal(status_code=status_code, message=message, data=data)

def error_response(error: Any, message: str = "An error occurred", status_code: int = 400):
    return ErrorResponseModal(status_code=status_code, message=message, error=error)
