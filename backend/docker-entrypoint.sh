#!/bin/sh
set -e

echo "Applying database migrations..."
alembic upgrade head --verbose

echo "Starting FastAPI application..."
exec uvicorn asgi:app --host 0.0.0.0 --port 8000 --workers 4 --proxy-headers