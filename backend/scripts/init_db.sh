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

# Настройка переменных для wait
export WAIT_HOSTS=${POSTGRES_HOST}:${POSTGRES_PORT}
export WAIT_TIMEOUT=300
export WAIT_SLEEP_INTERVAL=2
export WAIT_HOST_CONNECT_TIMEOUT=30

# Wait for database
echo "🕒 Waiting for PostgreSQL to become available..."
/wait

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