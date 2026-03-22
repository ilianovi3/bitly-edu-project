from pydantic import BaseModel
from datetime import datetime
from typing import Generic, TypeVar


T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T | None = None

class PaginationMeta(BaseModel):
    total: int
    offset: int
    limit: int
    has_next: bool

class PaginatedApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: list[T]
    meta: PaginationMeta

class ErrorDetail(BaseModel):
    code: str
    message: str

class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail


class ORMBase(BaseModel):
    model_config = {"from_attributes": True}

class CreatedAtSchema(ORMBase):
    created_at: datetime

class TimestampSchema(CreatedAtSchema):
    updated_at: datetime
