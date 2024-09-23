from fastapi import APIRouter

from .endpoints import (
    auth,
    user,
    company,
    employee
)

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)

api_router.include_router(
    user.router,
    prefix="/user",
    tags=["user"],
)

api_router.include_router(
    company.router,
    prefix="/company",
    tags=["company"],
)


api_router.include_router(
    employee.router,
    prefix="/employee",
    tags=["employee"],
)


