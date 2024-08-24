import uvicorn

from app import create_app
from config import settings

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "asgi:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=True,
        reload_excludes=[
            ".docker/*"
        ],  # required for prevent crash by minio tmp in debug
    )
