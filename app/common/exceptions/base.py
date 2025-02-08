from typing import Any, ClassVar
from app.common.server import BaseSchema

from fastapi import HTTPException, status


class ErrorResponse(BaseSchema):
    error_code: str
    message: str
    error_data: dict[str, Any] | None = None


class APIError(HTTPException):
    """기본 API 에러 클래스"""

    STATUS_CODE: ClassVar[int] = status.HTTP_500_INTERNAL_SERVER_ERROR
    ERROR_CODE: ClassVar[str] = "INTERNAL_SERVER_ERROR"

    def __init__(
        self,
        message: str | None = None,
        error_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ):
        self.error_response = ErrorResponse(
            error_code=self.ERROR_CODE,
            message=message or "Internal server error",
            error_data=error_data or {},
        )

        super().__init__(
            status_code=self.STATUS_CODE,
            detail=self.error_response.model_dump(exclude_none=True),
            headers=headers,
        )
