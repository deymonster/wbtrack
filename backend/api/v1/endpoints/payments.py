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



