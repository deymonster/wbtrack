# Этап 1: Базовый образ для зависимостей
FROM python:3.11-slim as python-base
ENV PYTHONUNBUFFERED=1\
    PYTHONDONTWRITEBYTECODE=1\
    PIP_NO_CACHE_DIR=off\
    PIP_DISABLE_PIP_VERSION_CHECK=on\
    PIP_DEFAULT_TIMEOUT=100
    

# Этап 2: Билдер для установки зависимостей
FROM python-base as builder
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Копируем только файлы для установки зависимостей
WORKDIR /app
COPY requirements.txt .
COPY sqlmodel_dist/sqlmodel-0.0.22-py3-none-any.whl ./sqlmodel_dist/

# Установка зависимостей через uv
RUN /root/.cargo/bin/uv pip install --system -r requirements.txt

# Этап 3: Финальный образ
FROM python-base as production
ENV FASTAPI_ENV=production
ENV PYTHONPATH=/app

# Копируем установленные пакеты и зависимости
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Копируем код приложения
COPY . /app/
WORKDIR /app

# Создаем пользователя без root прав
RUN addgroup --system app && adduser --system --group app

# Add and configure entrypoint script
COPY scripts/init_db.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && \
    chown app:app /entrypoint.sh

RUN chown -R app:app /app
USER app

# Запуск приложения
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "asgi:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--proxy-headers", "--log-level", "debug"]