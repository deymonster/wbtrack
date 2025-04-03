import asyncio

from sqlalchemy import text

from core.db import get_db_session_instance


async def test_db_connections():
    print("Testing database connections...")

    # Test core.db connection (used by Celery and Alembic)
    print("\n1. Testing core.db connection:")
    try:
        async with get_db_session_instance() as session:
            await session.execute(text("SELECT 1"))
            await session.commit()
            print("✅ core.db connection successful")
    except Exception as e:
        print(f"❌ core.db connection failed: {e}")

    print("\nEnvironment variables:")
    from config import settings
    print(f"DB URL: {settings.DB_ASYNC_CONNECTION_STR}")

if __name__ == "__main__":
    asyncio.run(test_db_connections())
