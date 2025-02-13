# Этап 1: Базовый образ для зависимостей
FROM python:3.11-slim as python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.4.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Этап 2: Билдер для установки зависимостей
FROM python-base as builder
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

# Установка poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Копируем только файлы для установки зависимостей
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# Установка зависимостей
RUN poetry install --only main --no-root

# Этап 3: Финальный образ
FROM python-base as production
ENV FASTAPI_ENV=production
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

# Копируем код приложения
COPY . /app/
WORKDIR /app

# Создаем пользователя без root прав
RUN addgroup --system app && adduser --system --group app
RUN chown -R app:app /app
USER app

# Запуск приложения
CMD ["uvicorn", "asgi:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--proxy-headers"]