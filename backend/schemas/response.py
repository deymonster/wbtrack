from typing import Any, Generic, List, Optional, TypeVar

from fastapi_pagination import (
    LimitOffsetPage,
)
from pydantic import BaseModel

T = TypeVar("T")


class INextCursor(BaseModel):
    offset: int
    limit: int


class IResponsePaginated(LimitOffsetPage[T], Generic[T]):
    next: Optional[INextCursor] = None


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class PVZRequestCodeResponse(BaseModel):
    message: str
    code_length: int


class PVZValidateCodeResponse(BaseModel):
    access_token: str


class TaskResponse(BaseModel):
    status: str
    message: str
    task_ids: List[str]

class TaskStatusResponse(BaseModel):
    status: str
    progress: int | None
    current_status: str | None
    result: Any | None
    error: str | None
