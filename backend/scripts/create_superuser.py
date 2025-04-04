#!/usr/bin/env python
import asyncio
import os
import sys
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import settings
from core.db import get_async_session
from core.security import get_password_hash
from enums.user import UserRoleEnum
from models.user import User


async def create_superuser():
    """Create a superuser with SUPER_ADMIN role"""
    # Default superuser credentials
    email = os.environ.get("SUPERUSER_EMAIL", "admin@wbtrack.app")
    password = os.environ.get("SUPERUSER_PASSWORD", "admin123")
    first_name = os.environ.get("SUPERUSER_FIRST_NAME", "Super")
    last_name = os.environ.get("SUPERUSER_LAST_NAME", "Admin")
    
    # Get database session
    async for session in get_async_session():
        # Check if superuser already exists
        result = await session.execute(select(User).where(User.email == email))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print(f"Superuser with email {email} already exists.")
            return
        
        # Create new superuser
        hashed_password = get_password_hash(password)
        
        # Set subscription dates for a year
        now = datetime.utcnow()
        one_year_later = now + timedelta(days=365)
        
        superuser = User(
            email=email,
            hashed_password=hashed_password,
            is_active=True,
            is_verified=True,
            is_superuser=True,
            first_name=first_name,
            last_name=last_name,
            role=UserRoleEnum.SUPER_ADMIN,
            is_subscription_active=True,
            subscription_start_date=now,
            subscription_end_date=one_year_later,
            created_at=now
        )
        
        session.add(superuser)
        await session.commit()
        await session.refresh(superuser)
        
        print(f"Superuser created successfully with email: {email}")
        print(f"User ID: {superuser.id}")
        print("Please change the default password after first login!")


if __name__ == "__main__":
    asyncio.run(create_superuser())