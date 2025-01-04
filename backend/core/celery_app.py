from celery import Celery
from config import settings


celery_app = Celery(
    "celery_worker_wb_track",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Настройки Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Yekaterinburg",
    enable_utc=True,
    broker_connection_retry_on_startup=True
)

# Импортируем задачи
celery_app.autodiscover_tasks(['tasks'])
