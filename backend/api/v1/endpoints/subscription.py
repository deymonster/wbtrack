from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_async_sqlalchemy import db
from sqlmodel import select

from api.dependencies.user import current_active_user, current_superuser
from enums.user import UserRoleEnum
from models.user import User
from schemas.subscription import SubscriptionApproval

router = APIRouter(prefix="/subscription", tags=["subscription"])


@router.get("/pending", response_model=List[User])
async def get_pending_subscriptions(
    current_user: User = Depends(current_superuser)
):
    """Get all users with pending subscription approval (role=ADMIN but not approved)"""
    query = select(User).where(
        User.role == UserRoleEnum.ADMIN,
        User.is_subscription_active is False
    )
    result = await db.session.execute(query)
    return result.scalars().all()


@router.post("/{user_id}/approve")
async def approve_subscription(
    user_id: str,
    approval: SubscriptionApproval,
    current_user: User = Depends(current_superuser)
):
    """Approve subscription for a user"""
    query = select(User).where(User.id == user_id)
    result = await db.session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role != UserRoleEnum.ADMIN:
        raise HTTPException(status_code=400, detail="User is not an admin")

    if user.is_subscription_active:
        raise HTTPException(status_code=400, detail="Subscription already active")

    # Update subscription details
    user.is_subscription_active = True
    user.subscription_start_date = datetime.utcnow()
    user.subscription_end_date = datetime.utcnow() + timedelta(days=approval.duration_days)
    user.subscription_approved_by = str(current_user.id)
    user.subscription_approved_at = datetime.utcnow()

    await db.session.commit()
    return {"message": "Subscription approved successfully"}


@router.get("/status")
async def get_subscription_status(
    current_user: User = Depends(current_active_user)
):
    """Get current user's subscription status"""
    return {
        "is_subscription_active": current_user.is_subscription_active,
        "start_date": current_user.subscription_start_date,
        "end_date": current_user.subscription_end_date,
        "role": current_user.role
    }
