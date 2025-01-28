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
    description="Создание недельных выплат с вложенными данными",
    responses={
        201: {"description": "Недельные выплаты успешно созданы"},
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
        
        created_payments = []
        for weekly_data in all_weekly_data:
            try:
                created_payment = await weekly_payments_crud.create_weekly_payments_with_relations(
                    weekly_data=weekly_data
                )
                created_payments.append(created_payment)
            except ValueError as ve:
                logger.error(f"Validation error while processing weekly data: {ve}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Ошибка при обработке данных недели: {ve}"
                )

            except Exception as e:
                logger.error(f"Error while saving weekly data: {e}")
                raise HTTPException(
                    status_code=500,
                    detail="Произошла ошибка при сохранении данных недели"
                )
            
        return {
            "status": "success",
            "message": f"{len(created_payments)} недельные выплаты успешно сохранены.",
            "data": created_payments
        }
    except ValueError as e:
        logger.error(f"Validation error while fetching weekly payments: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка при получении данных выплат: {e}"
        )
    except Exception as e:
        logger.error(f"Unexpected error while fetching or saving weekly payments: {e}")
        raise HTTPException(
            status_code=500,
            detail="Произошла ошибка на сервере"
        )








