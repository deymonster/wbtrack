from typing import Generic, Optional, TypeVar
from fastapi import Query
from fastapi_pagination import (
    LimitOffsetPage,
    LimitOffsetParams as LimitOffsetParamsBase,
)
from pydantic import BaseModel

T = TypeVar("T")


class INextCursor(BaseModel):
    offset: int
    limit: int


class IResponsePaginated(LimitOffsetPage[T], Generic[T]):
    next: Optional[INextCursor] = None
