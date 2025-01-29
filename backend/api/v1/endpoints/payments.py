from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Request, Depends, Query, HTTPException, status
from fastapi_pagination import LimitOffsetParams, Page, add_pagination
from api.dependencies.user import current_active_user
from core.exceptions import NotFound, ValidationError

from models.user import User

from schemas.response import IResponsePaginated
from enums.common import ListOrderEnum
from core.redis import redis_client
from services.pvz_service import PVZService
from api.v1.endpoints.pvz import get_pvz_service
from crud.payments_weekly import weekly_payments_crud
import logging
from typing import Annotated
from celery.result import AsyncResult
from tasks.weekly_payments import process_weekly_payments
from schemas.response import TaskResponse, TaskStatusResponse
from core.celery_app import celery_app


logger = logging.getLogger(__name__)



router = APIRouter(
    generate_unique_id_function=lambda route: f"payments_{route.name}",
)
@router.get(
    "/",
    description="Получение всех недельных платежей с вложенными данными",
    responses={
        200: {"description": "Список недельных платежей успешно получен"},
        401: {"description": "Ошибка авторизации"},
        400: {"description": "Ошибка в запросе"},
    },
)
async def get_weekly_payments(
    pvz_service: Annotated[PVZService, Depends(get_pvz_service)],
    current_user: User = Depends(current_active_user)):
    """
    Возвращает список всех недельных платежей с вложенными данными.

    Требуется заголовок `X-Phone-Number` с номером телефона.
    """
    try:
        return await pvz_service.get_all_weekly_payments()
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/",
    response_model=TaskResponse,
    description="Создание недельных выплат с вложенными данными",
    responses={
        202: {"description": "Задача на создание выплат запущена"},
        400: {"description": "Ошибка в запросе"},
        401: {"description": "Ошибка авторизации"},
    },
)
async def create_weekly_payments(
    pvz_service: Annotated[PVZService, Depends(get_pvz_service)],
    current_user: User = Depends(current_active_user)):
    """Get and create weeklypayments with nested data"""
    try:
        all_weekly_data = await pvz_service.get_all_weekly_payments()
        
        # created_payments = []
        task_ids = []
        for weekly_data in all_weekly_data:
            # Start Celery task for each week
            weekly_data_dict = weekly_data.dict()
            task = process_weekly_payments.delay(weekly_data_dict)
            task_ids.append(task.id)
        
        return {
            "status": "accepted",
            "message": f"Started processing {len(task_ids)} weekly payments",
            "task_ids": task_ids
        }
    except Exception as e:
        logger.error(f"Error starting weekly payments task: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error starting weekly payments task: {str(e)}"
        )
        

@router.get(
    "/task/{task_id}",
    response_model=TaskStatusResponse,
    description="Получение статуса задачи weekly_payments по ID",
    responses={
        200: {"description": "Статус задачи weekly_payments успешно получен"},
        401: {"description": "Ошибка авторизации"},
        404: {"description": "Задача не найдена"},
        },
    )
async def get_task_status(
                    task_id: str,
                    current_user: User = Depends(current_active_user)
                    ):
    """Get status of weekly payments processing task"""
    try:
        task_result = celery_app.AsyncResult(task_id)

        if task_result.state == 'PENDING':
            return TaskStatusResponse(
                status="pending",
                progress=0,
                current_status="Task is pending",
                result=None,
                error=None
            )
        elif task_result.state == 'PROGRESS':
            info = task_result.info or {}
            return TaskStatusResponse(
                status="in_progress",
                progress=info.get('progress', 0),
                current_status=info.get('status', 'Task in progress'),
                result=None,
                error=None
            )
        
        elif task_result.state == 'SUCCESS':
            return TaskStatusResponse(
                status="completed",
                progress=100,
                current_status="Task completed successfully",
                result=task_result.result,
                error=None
            )

        elif task_result.state == 'FAILURE':
            error_info = task_result.info or {}
            return TaskStatusResponse(
                status="error",
                progress=0,
                current_status="Task failed",
                result=None,
                error=str(error_info)
            )

        else:
            return TaskStatusResponse(
                status=task_result.state,
                progress=0,
                current_status="Unknown task state",
                result=None,
                error=None
            )

        
    except Exception as e:
        logger.error(f"Error getting task status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving task status: {str(e)}"
        )








