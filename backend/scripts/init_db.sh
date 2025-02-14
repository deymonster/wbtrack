#!/bin/bash

echo "Starting database initialization..."

# Check if this is Celery container
if [[ "$@" == *"celery"* ]]; then
    echo "Celery container detected, applying existing migrations only..."
    alembic upgrade head
else
    # Create migrations directory
    mkdir -p migrations/versions

    # Check and create migrations
    if [ -z "$(ls -A migrations/versions/)" ]; then
        echo "No migrations found. Creating initial migration..."
        alembic revision --autogenerate -m "Initial migration"
    else
        # Check if there are actual model changes before creating new migration
        CHANGES=$(alembic revision --autogenerate --sql 2>/dev/null)
        if [ -n "$CHANGES" ]; then
            echo "Model changes detected, creating new migration..."
            alembic revision --autogenerate -m "Auto migration $(date +%Y%m%d_%H%M)"
        else
            echo "No model changes detected, skipping migration creation"
        fi
    fi

    # Apply migrations
    echo "Applying migrations..."
    alembic upgrade head
fi

echo "✅ Database initialization completed!"

# Execute the main container command
exec "$@"