from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Request, Depends, Query, HTTPException, status
from fastapi_pagination import LimitOffsetParams, Page, add_pagination
from api.dependencies.user import current_active_user
from core.exceptions import NotFound, ValidationError
from crud.office import office_crud
from models.office import Office
from models.user import User
from schemas.office import IOfficeRead
from schemas.response import IResponsePaginated
from enums.common import ListOrderEnum
import logging

logger = logging.getLogger(__name__)



router = APIRouter(
    generate_unique_id_function=lambda route: f"checkpoint_{route.name}",
)


@router.get("/", response_model=IResponsePaginated[IOfficeRead])
async def get_list_paginated(
    params: LimitOffsetParams = Depends(),
    current_user: User = Depends(current_active_user),
    order_by: str = Query(None, description="Поле для сортировки"),
    order: ListOrderEnum = Query(ListOrderEnum.descendent, description="Направление сортировки")
) -> Page[IOfficeRead]:
    """
    Получение списка офисов текущего пользователя с пагинацией.

    - **limit**: количество элементов на странице
    - **offset**: смещение от начала списка
    - **order_by**: поле для сортировки
    - **order**: направление сортировки (asc/desc)
    """
    user_id = current_user.id
    logger.info(f"User id of current user - {user_id}")
    if order_by and order_by not in Office.__table__.columns.keys():
        raise ValidationError(f"Некорректное поле для сортировки: {order_by}")
    order_by = order_by or "id"
    return await office_crud.get_offices_paginated(
        user_id=user_id,
        params=params,
        order_by=order_by,
        order=order,
    )

@router.delete("/{office_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(office_id: int,current_user: User = Depends(current_active_user)):
    """Удаляет офис принадлежащий пользователю
    
    - **office_id**: office_id из модели офиса
    - **current_user**: Текущий пользователь
    """

    office = await office_crud.get_office_by_user_id(office_id=office_id, user_id=current_user.id)
    if not office:
        raise HTTPException(
            status_code=404,
            detail="Офис не найден или вы не имеете прав на его удаление"
        )
    await office_crud.delete(id=office.id)


                       


add_pagination(router)