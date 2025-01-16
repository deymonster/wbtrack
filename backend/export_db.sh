#!/bin/bash

# Загружаем переменные окружения из .env файла
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo ".env file not found"
    exit 1
fi

# Создаем директорию для экспорта если её нет
EXPORT_DIR="db_export"
mkdir -p $EXPORT_DIR

echo "Starting database export..."

# Экспортируем структуру каждой таблицы
echo "Exporting table structures..."
docker exec postgres-wbtrack psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\d+" > "$EXPORT_DIR/tables_structure.txt"

# Получаем список всех таблиц и экспортируем каждую в CSV
echo "Exporting table data to CSV..."
docker exec postgres-wbtrack psql -U $POSTGRES_USER -d $POSTGRES_DB -t -c "SELECT tablename FROM pg_tables WHERE schemaname='public'" | while read table; do
    table=$(echo $table | xargs)  # Убираем лишние пробелы
    if [ ! -z "$table" ]; then
        echo "Exporting table: $table"
        docker exec postgres-wbtrack psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\COPY (SELECT * FROM $table) TO STDOUT WITH CSV HEADER" > "$EXPORT_DIR/${table}.csv"
    fi
done

echo "Export completed! Files are saved in the $EXPORT_DIR directory"
echo "Table structure: $EXPORT_DIR/tables_structure.txt"
echo "Table data: $EXPORT_DIR/*.csv"