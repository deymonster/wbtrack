#!/bin/bash

# Проверяем, установлен ли Git
if ! command -v git &> /dev/null; then
    echo "Git не установлен. Устанавливаем..."
    apt-get update && apt-get install -y git
fi

# Проверяем, установлен ли Docker
if ! command -v docker &> /dev/null; then
    echo "Docker не установлен. Устанавливаем..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

# Проверяем, установлен ли Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose не установлен. Устанавливаем..."
    curl -L "https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Запрашиваем URL репозитория
read -p "Введите URL Git-репозитория: " GIT_REPO_URL

# Запрашиваем директорию для клонирования
read -p "Введите директорию для клонирования (по умолчанию: /opt/wbtrack): " INSTALL_DIR
INSTALL_DIR=${INSTALL_DIR:-/opt/wbtrack}

# Создаем директорию, если она не существует
mkdir -p $INSTALL_DIR

# Клонируем репозиторий
echo "Клонирование репозитория в $INSTALL_DIR..."
git clone $GIT_REPO_URL $INSTALL_DIR

# Переходим в директорию backend проекта
cd $INSTALL_DIR/backend

# Проверяем наличие .env.example
if [ ! -f .env.example ]; then
    echo "Ошибка: Файл .env.example не найден в директории backend."
    exit 1
fi

# Создаем .env файл, если он не существует
if [ ! -f .env ]; then
    echo "Создаем .env файл на основе .env.example..."
    cp .env.example .env
    
    # Генерируем случайные пароли
    APP_SECRET_KEY=$(openssl rand -hex 32)
    REDIS_PASSWORD=$(openssl rand -hex 16)
    POSTGRES_PASSWORD=$(openssl rand -hex 16)
    POSTGRES_NON_ROOT_PASSWORD=$(openssl rand -hex 16)
    
    # Заменяем значения в .env файле
    sed -i "s/your_secret_key_here/$APP_SECRET_KEY/g" .env
    sed -i "s/your_strong_redis_password_here/$REDIS_PASSWORD/g" .env
    sed -i "s/your_strong_postgres_password_here/$POSTGRES_PASSWORD/g" .env
    sed -i "s/your_strong_non_root_password_here/$POSTGRES_NON_ROOT_PASSWORD/g" .env
    
    echo "Файл .env создан с случайными паролями."
    echo "ВАЖНО: Отредактируйте файл .env и установите правильные значения для токенов и других настроек."
    read -p "Нажмите Enter, чтобы продолжить после редактирования .env файла..."
fi

# Создаем пароль для Nginx Basic Auth (для защиты Portainer)
echo "Создание учетных данных для доступа к Portainer через Nginx..."
NGINX_USER="admin"
NGINX_PASSWORD=$(openssl rand -base64 12)
NGINX_AUTH_DIR="./nginx/auth"

mkdir -p $NGINX_AUTH_DIR
echo "$NGINX_USER:$(openssl passwd -apr1 $NGINX_PASSWORD)" > $NGINX_AUTH_DIR/.htpasswd

echo "Созданы учетные данные для доступа к Portainer:"
echo "Пользователь: $NGINX_USER"
echo "Пароль: $NGINX_PASSWORD"
echo "Сохраните эти данные в надежном месте!"

# Запускаем скрипт деплоя
echo "Запускаем деплой..."
chmod +x scripts/deploy_prod.sh
./scripts/deploy_prod.sh 