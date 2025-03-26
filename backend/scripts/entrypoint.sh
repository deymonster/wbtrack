#!/bin/bash

echo "🚀 Starting application..."

# Wait for PostgreSQL
echo "⏳ Waiting for PostgreSQL..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done
echo "✅ PostgreSQL is ready!"

# Apply migrations (only apply, don't create new ones)
echo "⏳ Applying database migrations..."
alembic upgrade head
echo "✅ Migrations applied!"

# Execute main command
echo "🚀 Starting main application..."
exec "$@" 