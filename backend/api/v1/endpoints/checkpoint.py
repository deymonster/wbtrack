import logging

from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import LimitOffsetParams, Page, add_pagination

from api.dependencies.user import current_active_user
from core.exceptions import ValidationError
from crud.office import office_crud
from enums.common import ListOrderEnum
from models.office import Office
from models.user import User
from schemas.office import IOfficeRead
from schemas.response import IResponsePaginated

logger = logging.getLogger(__name__)



router = APIRouter(
    generate_unique_id_function=lambda route: f"checkpoint_{route.name}",
)

limit_offset_dependency = Depends()
current_user_dependency = Depends(current_active_user)
order_by_query = Query(None, description="Поле для сортировки")
order_query = Query(ListOrderEnum.descendent, description="Направление сортировки")


@router.get("/", response_model=IResponsePaginated[IOfficeRead])
async def get_list_paginated(
    params: LimitOffsetParams = limit_offset_dependency,
    current_user: User = current_user_dependency,
    order_by: str = order_by_query,
    order: ListOrderEnum = order_query
) -> Page[IOfficeRead]:
    """
    Получение списка офисов текущего пользователя c пагинацией

    Parameters:
    - **params**: Параметры пагинации
        - limit: количество элементов на странице
        - offset: смещение от начала списка
    - **order_by**: поле для сортировки (доступные поля: id, name, address, create_date)
    - **order**: направление сортировки (asc/desc)

    Returns:
    - **200**: Успешное получение списка
        - items: Список офисов
        - total: Общее количество офисов
        - limit: Размер страницы
        - offset: Текущее смещение
    - **422**: Ошибка валидации
        - detail: Описание ошибки

    Example:
    ```json
    {
        "items": [
            {
                "id": 1,
                "name": "Офис на Ленина",
                "address": "ул. Ленина, 1",
                "create_date": "2023-01-01T00:00:00"
            }
        ],
        "total": 1,
        "limit": 10,
        "offset": 0
    }
    ```
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
async def delete_by_id(office_id: int,current_user: User = current_user_dependency):
    """Удаляет офис принадлежащий пользователю

    Parameters:
    - **office_id**: ID офиса для удаления

    Returns:
    - **204**: Успешное удаление
    - **404**: Офис не найден или нет прав доступа
        - detail: Описание ошибки
    """

    await office_crud.delete_office_by_user(
        office_id=office_id,
        user_id=current_user.id
    )




add_pagination(router)
