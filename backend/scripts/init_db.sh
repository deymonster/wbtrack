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

# Проверяем и очищаем  таблицу alembic_version при необходимости
python -c "
import os, sys, asyncio
import asyncpg

async def check_and_clean():
    try:
        conn = await asyncpg.connect(
            host=os.environ.get('POSTGRES_HOST'),
            port=int(os.environ.get('POSTGRES_PORT', 5432)),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            database=os.environ.get('POSTGRES_DB')
        )
        
        # Проверяем существование таблицы alembic_version
        exists = await conn.fetchval(\"\"\"
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'alembic_version'
            )
        \"\"\")
        
        if exists:
            print('⚠️ Found existing alembic_version table, cleaning it...')
            await conn.execute('DELETE FROM alembic_version')
            print('✅ alembic_version table cleaned')
        
        await conn.close()
    except Exception as e:
        print(f'❌ Error checking/cleaning alembic_version: {e}')

asyncio.run(check_and_clean())
"

# Create migrations directory
mkdir -p migrations/versions

# Check and create migrations
if [ -z "$(ls -A migrations/versions/)" ]; then
    log "📝 No migrations found. Creating initial migration..."
    alembic revision --autogenerate -m "Initial migration" || handle_error "Failed to create initial migration"
else
    log "📝 Checking for model changes..."
    # Пытаемся создать миграцию, но игнорируем ошибки
    alembic revision --autogenerate -m "Auto migration $(date +%Y%m%d_%H%M)" || log "⚠️ Warning: Could not create migration, continuing anyway"
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