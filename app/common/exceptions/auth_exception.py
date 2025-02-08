from typing import Any
from app.common.exceptions.base import APIError
from fastapi import status


class AuthenticateFailed(APIError):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    ERROR_CODE = "AUTHENTICATE_FAILED"

    def __init__(
        self,
        message: str | None = None,
        error_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ):
        error_data = error_data or {}
        super().__init__(message=message, error_data=error_data, headers=headers)


class UserNotFound(APIError):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    ERROR_CODE = "AUTHENTICATE_FAILED"
