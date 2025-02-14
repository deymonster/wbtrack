#!/bin/bash

echo "Starting database initialization..."

# Create migrations directory
mkdir -p migrations/versions

# Check and create migrations
if [ -z "$(ls -A migrations/versions/)" ]; then
    echo "No migrations found. Creating initial migration..."
    alembic revision --autogenerate -m "Initial migration"
else
    echo "Checking for model changes..."
    alembic revision --autogenerate -m "Auto migration $(date +%Y%m%d_%H%M)"
fi

# Apply migrations
echo "Applying migrations..."
alembic upgrade head

echo "✅ Database initialization completed!"

# Execute the main container command
exec "$@"