#!/bin/bash
set -e

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

handle_error() {
    log "❌ Error: $1"
    exit 1
}

echo "🔄 Starting database initialization..."

# Wait for database
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
  echo "🕒 Waiting for PostgreSQL to become available..."
  sleep 2
done

echo "✅ Database is available"

# Create migrations directory
mkdir -p migrations/versions

# Check and create migrations
if [ -z "$(ls -A migrations/versions/)" ]; then
    log "📝 No migrations found. Creating initial migration..."
    alembic revision --autogenerate -m "Initial migration" || handle_error "Failed to create initial migration"
elif [ -n "$(alembic revision --autogenerate --sql 2>/dev/null)" ]; then
    log "📝 Model changes detected, creating new migration..."
    alembic revision --autogenerate -m "Auto migration $(date +%Y%m%d_%H%M)" || handle_error "Failed to create new migration"
else
    log "✅ No model changes detected"
fi

# Apply migrations
log "⚡ Applying migrations..."
alembic upgrade head || handle_error "Failed to apply migrations"

echo "✅ Database initialization completed!"

# Execute the main container command
exec "$@"