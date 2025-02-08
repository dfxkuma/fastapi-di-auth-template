from typing import Any
from app.common.exceptions.base import APIError
from fastapi import status


class UserNotFound(APIError):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    ERROR_CODE = "RESOURCE_NOT_FOUND"

    def __init__(
        self,
        resource_id: str | None = None,
        message: str | None = None,
        error_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ):
        error_data = error_data or {}
        if resource_id:
            error_data["resource_id"] = resource_id
            message = message or f"Resource {resource_id} not found"

        super().__init__(message=message, error_data=error_data, headers=headers)
