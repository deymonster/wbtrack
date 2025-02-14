import asyncio
from core.db import engine

async def test_connection():
    try:
        async with engine.connect() as conn:
            print('Connection successful')
    except Exception as e:
        print(f'Connection failed: {e}')

if __name__ == "__main__":
    asyncio.run(test_connection())