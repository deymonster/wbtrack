from fastapi import APIRouter

from .endpoints import (
    auth,
    checkpoint,
    # company,
    employee,
    office_expenses,
    pvz,
    subscription,
    user,
    user_management,
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

# api_router.include_router(
#     company.router,
#     prefix="/company",
#     tags=["company"],
# )


api_router.include_router(
    employee.router,
    prefix="/employee",
    tags=["employee"],
)

api_router.include_router(
    pvz.router,
    prefix="/pvz",
    tags=["pvz"],
)

api_router.include_router(
    checkpoint.router,
    prefix="/checkpoint",
    tags=["checkpoint"],
)


api_router.include_router(
    subscription.router,
    prefix="/subscription",
    tags=["subscription"],
)

api_router.include_router(
    user_management.router,
    prefix="/user-management",
    tags=["user-management"],
)

api_router.include_router(
    office_expenses.router,
    prefix="/office-expenses",
    tags=["office-expenses"]
)


