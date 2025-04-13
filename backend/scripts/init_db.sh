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
    alembic upgrade head || handle_error "Failed to apply initial migration"
else
    log "📝 Checking and applying model changes..."
    # Создаем новую миграцию для изменений
    alembic revision --autogenerate -m "Auto migration $(date +%Y%m%d_%H%M)"
    # Применяем только новые миграции
    alembic upgrade head
fi

# Apply migrations
log "⚡ Applying migrations..."
if ! alembic upgrade head; then
    log "⚠️ Error applying migrations, trying with --sql option for debugging..."
    alembic upgrade head --sql > migration_sql.sql
    log "⚠️ SQL saved to migration_sql.sql for debugging"
    
    # Если миграции не применились, попробуем создать новую базовую миграцию
    log "⚠️ Trying to create a fresh migration..."
    rm -rf migrations/versions/*
    alembic revision --autogenerate -m "Fresh migration $(date +%Y%m%d_%H%M)" || handle_error "Failed to create fresh migration"
    alembic upgrade head || handle_error "Failed to apply fresh migration"
fi

# Create superuser if needed
log "🔑 Checking if superuser needs to be created..."
python /app/scripts/create_superuser.py || log "⚠️ Note: Superuser creation skipped (may already exist)"

echo "✅ Database initialization completed!"

# Execute the main container command
exec "$@"