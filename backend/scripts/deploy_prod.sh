#!/bin/bash

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "Ошибка: Файл .env не найден. Создайте его перед запуском."
    exit 1
fi

# Загружаем переменные из .env файла
source .env

# Создаем необходимые директории
mkdir -p .docker/postgres .docker/redis .docker/portainer-data

# Генерируем SSL-сертификаты, если их нет
if [ ! -f nginx/ssl/server.crt ]; then
    echo "Генерация SSL-сертификатов..."
    ./scripts/generate_ssl.sh
fi

# Останавливаем и удаляем существующие контейнеры
echo "Останавливаем существующие контейнеры..."
docker-compose -f docker-compose.prod.yml down

# Собираем и запускаем контейнеры
echo "Запускаем контейнеры..."
docker-compose -f docker-compose.prod.yml up -d

echo "Проверяем статус контейнеров..."
docker-compose -f docker-compose.prod.yml ps

# Получаем IP-адрес сервера
SERVER_IP=$(curl -s ifconfig.me)

echo "Deployment завершен!"
echo "============================================================"
echo "Доступ к сервисам через веб-интерфейс:"
echo "Основное приложение: http://$SERVER_IP/"
echo "Portainer: http://$SERVER_IP/portainer/"
echo ""
echo "Учетные данные для доступа к Portainer через веб-интерфейс:"
if [ -f nginx/auth/.htpasswd ]; then
    NGINX_USER=$(cat nginx/auth/.htpasswd | cut -d: -f1)
    echo "Пользователь: $NGINX_USER"
    echo "Пароль: [Был показан при установке]"
else
    echo "Файл с учетными данными не найден. Запустите скрипт clone_and_deploy.sh заново."
fi
echo ""
echo "============================================================"
echo "Для подключения к сервисам через SSH-туннель используйте:"
echo "PostgreSQL: ssh -L 5433:localhost:$POSTGRES_PORT user@$SERVER_IP"
echo "Redis: ssh -L 6380:localhost:6379 user@$SERVER_IP"
echo "Portainer (прямой доступ): ssh -L 9001:localhost:9000 user@$SERVER_IP"
echo "Приложение (прямой доступ): ssh -L 8001:localhost:$APP_PORT user@$SERVER_IP"
echo ""
echo "После создания SSH-туннеля сервисы будут доступны на вашем компьютере:"
echo "PostgreSQL: localhost:5433"
echo "Redis: localhost:6380"
echo "Portainer: http://localhost:9001"
echo "Приложение: http://localhost:8001"
echo "============================================================" 