from fastapi import APIRouter

from api import (
    v1,
)

api_router = APIRouter(prefix="/api")
api_router.include_router(v1.api_router, prefix="/v1")

__all__ = [
    "api_router",
]
