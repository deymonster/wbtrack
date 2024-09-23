from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users.exceptions import InvalidPasswordException, FastAPIUsersException, UserNotExists
from fastapi_users.authentication import JWTStrategy
from fastapi_users.jwt import decode_jwt

from config import settings
from core.exceptions import NotAuthenticated, NotFound, ValidationError
from core.user_management import access_backend, refresh_backend, fastapi_users, create_employee_jwt_access
from crud.employee import employee_crud
from schemas.response import LoginResponse
from schemas.user import IUserCreate, IUserRead, RefreshTokenRequest
from services.user import UserService
from pydantic import BaseModel

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(
        credentials: OAuth2PasswordRequestForm = Depends(),
        user_manager: UserService = Depends(fastapi_users.get_user_manager),
        access_strategy: JWTStrategy = Depends(access_backend.get_strategy),
        refresh_strategy: JWTStrategy = Depends(refresh_backend.get_strategy),
):
    """Endpoint to login"""
    try:
        user = await user_manager.get_by_email(credentials.username)
    except UserNotExists:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    try:
        await user_manager.validate_password(credentials.password, user)
    except InvalidPasswordException:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token = await access_strategy.write_token(user)
    refresh_token = await refresh_strategy.write_token(user)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

# router.include_router(
#     fastapi_users.get_auth_router(access_backend),
# )

router.include_router(
    fastapi_users.get_register_router(IUserRead, IUserCreate),
)

router.include_router(
    fastapi_users.get_reset_password_router(),
)

router.include_router(
    fastapi_users.get_verify_router(IUserRead),
)


@router.post("/refresh-token")
async def refresh_token(
        request: RefreshTokenRequest,
        user_manager: UserService = Depends(fastapi_users.get_user_manager),
        access_strategy: JWTStrategy = Depends(access_backend.get_strategy),
        refresh_strategy: JWTStrategy = Depends(refresh_backend.get_strategy)
):
    """Endpoint to refresh the token"""

    if request.is_employer:

        try:
            print("Begin employee token decode")
            payload = decode_jwt(
                request.refresh_token,
                settings.APP_SECRET_KEY,
                audience=["employee"],
                algorithms=["HS256"]
            )

            employee_id = payload["sub"]
            if not employee_id:
                raise NotAuthenticated(detail="Invalid refresh token")

            employee = await employee_crud.get(id=employee_id)
            if not employee or employee.is_deleted:
                raise NotFound(detail="Employee is deleted or not found")

            access_token = create_employee_jwt_access(employee)

            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Invalid refresh token - {e}")
    else:
        try:
            user = await refresh_strategy.read_token(request.refresh_token,  user_manager)
            if not user:
                raise ValidationError(detail="Invalid refresh token - None user")

            # user_id = await user_manager.get(user.id)
            if not user.is_active:
                raise HTTPException(status_code=401, detail="Inactive user")
            access_token = await access_strategy.write_token(user)
            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
        except FastAPIUsersException:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
