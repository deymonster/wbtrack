from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_async_sqlalchemy import db
from sqlmodel import select

from api.dependencies.user import current_active_user, current_admin_user
from core.user_management import get_user_service
from enums.user import UserRoleEnum
from models.user import User
from schemas.user import IUserCreate, UserResponse

router = APIRouter(prefix="/user-management", tags=["user-management"])


async def check_admin_permissions(current_user: User):
    """Check if user is admin with active subscription"""
    if current_user.role != UserRoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can manage users")
    if not current_user.is_subscription_active:
        raise HTTPException(status_code=403, detail="Admin subscription is not active")


@router.post("/create-manager", response_model=UserResponse)
async def create_manager(
    user_data: IUserCreate,
    current_user: User = Depends(current_admin_user),
    user_service=Depends(get_user_service),
):
    """Create a new manager user (only for admins with active subscription)"""
    await check_admin_permissions(current_user)

    # Create user with manager role
    user = await user_service.create(
        user_data,
        safe=True,
        request=None
    )

    # Update user fields
    user.role = UserRoleEnum.MANAGER
    user.created_by_id = str(current_user.id)
    user.parent_admin_id = str(current_user.id)

    await db.session.commit()
    return user


@router.post("/create-checker", response_model=UserResponse)
async def create_checker(
    user_data: IUserCreate,
    current_user: User = Depends(current_admin_user),
    user_service=Depends(get_user_service),
):
    """Create a new checker user (only for admins with active subscription)"""
    await check_admin_permissions(current_user)

    # Create user with checker role
    user = await user_service.create(
        user_data,
        safe=True,
        request=None
    )

    # Update user fields
    user.role = UserRoleEnum.CHECKER
    user.created_by_id = str(current_user.id)
    user.parent_admin_id = str(current_user.id)

    await db.session.commit()
    return user


@router.get("/my-users", response_model=List[UserResponse])
async def get_my_users(
    current_user: User = Depends(current_active_user)
):
    """Get all users created by current admin"""
    if current_user.role not in [UserRoleEnum.ADMIN, UserRoleEnum.SUPER_ADMIN]:
        raise HTTPException(status_code=403, detail="Only admins can view their users")

    # SUPER_ADMIN видит всех пользователей
    if current_user.role == UserRoleEnum.SUPER_ADMIN:
        query = select(User)
    else:
        # ADMIN видит только созданных им пользователей
        query = select(User).where(User.created_by_id == str(current_user.id))

    result = await db.session.execute(query)
    return result.scalars().all()


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(current_admin_user)
):
    """Delete a user (only their creator admin can do this)"""
    await check_admin_permissions(current_user)

    query = select(User).where(User.id == user_id)
    result = await db.session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.created_by_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="You can only delete users you created")

    if user.role not in [UserRoleEnum.MANAGER, UserRoleEnum.CHECKER]:
        raise HTTPException(status_code=403, detail="You can only delete manager or checker users")

    await db.session.delete(user)
    await db.session.commit()
    return {"message": "User deleted successfully"}
