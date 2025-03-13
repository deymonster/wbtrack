#!/bin/bash

# Создаем директорию для SSL-сертификатов, если она не существует
mkdir -p nginx/ssl

# Генерируем приватный ключ
openssl genrsa -out nginx/ssl/server.key 2048

# Генерируем CSR (Certificate Signing Request)
openssl req -new -key nginx/ssl/server.key -out nginx/ssl/server.csr -subj "/C=RU/ST=State/L=City/O=Organization/CN=wbtrack.local"

# Генерируем самоподписанный сертификат
openssl x509 -req -days 365 -in nginx/ssl/server.csr -signkey nginx/ssl/server.key -out nginx/ssl/server.crt

# Устанавливаем правильные разрешения
chmod 600 nginx/ssl/server.key
chmod 644 nginx/ssl/server.crt

echo "SSL-сертификаты успешно сгенерированы в директории nginx/ssl/"
echo "Для использования HTTPS раскомментируйте соответствующие секции в nginx/conf.d/default.conf" 