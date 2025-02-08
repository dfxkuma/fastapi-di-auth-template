from typing import Generic, TypeVar

from pydantic import Field, BaseModel

from app.common.server.schema import BaseSchema

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    message: str | None
    data: T | None = None


class SuccessfulEntityResponse(BaseSchema):
    entity_id: str = Field(..., examples=["673c114c-e920-4b6c-bc16-f5666c8d1e60"])
