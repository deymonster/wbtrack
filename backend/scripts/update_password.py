#!/usr/bin/env python
import asyncio
import os
import sys
from fastapi_users.password import get_password_hash
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.db import get_db_session_instance
from sqlmodel import select
from models.user import User

async def update_superuser_password():
    new_password = os.environ.get("SUPERUSER_PASSWORD")
    
    async with get_db_session_instance() as session:
        result = await session.execute(
            select(User).where(User.email == "admin@wbtrack.app")
        )
        superuser = result.scalar_one_or_none()
        
        if not superuser:
            print("❌ Superuser not found!")
            return
            
        superuser.hashed_password = get_password_hash(new_password)
        await session.commit()
        print("✅ Password updated successfully!")

if __name__ == "__main__":
    asyncio.run(update_superuser_password())