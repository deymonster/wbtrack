import base64
import logging
import secrets

import httpx
from fastapi import APIRouter, Depends, Query
from fastapi_pagination import LimitOffsetParams, add_pagination
from sqlmodel import func, select

from api.dependencies.employee import get_currrent_employee
from api.dependencies.user import current_active_user
from config import settings
from core.exceptions import NotFound, ValidationError
from core.redis import redis_client
from core.user_management import create_employee_jwt_access, create_employee_jwt_refresh
from crud.employee import employee_crud
from enums.common import ListOrderEnum
from models.employee import Employee
from models.user import User
from schemas.employee import AuthRequest, IEmployeeRead, SearchParams
from schemas.response import IResponsePaginated
from schemas.user import RegisterResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    generate_unique_id_function=lambda route: f"employee_{route.name}",
)

client = httpx.AsyncClient()
BASE_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"


# def encode_phone_number(phone: str) -> str:
#     encoded_bytes = base64.b64encode(phone.encode('utf-8'))
#     return encoded_bytes.decode('utf-8')

#
# @router.post(path="/register", response_model=RegisterResponse)
# async def get_employee_by_phone(request: RegistrationRequest):
#     """Register new user by phone number and generate OTP
#
#     """
#     employee = await employee_crud.get_by_phone(request.phone)
#     if not employee:
#         raise NotFound
#
#     otp = secrets.randbelow(1000000)
#     encoded_phone = base64.b64encode(request.phone.encode('utf-8')).decode()
#     redis_key = f"otp:{encoded_phone}"
#     await redis_client.hset(redis_key, mapping={'otp': otp, 'email': request.email})
#     exists = await redis_client.exists(redis_key)
#     if not exists:
#         print("Key does not exist.")
#     await redis_client.expire(redis_key, 10 * 60)
#     bot_link = f"https://t.me/WBtrackAuth_bot?start={encoded_phone}_{otp}"
#     return RegisterResponse(registration_link=bot_link)


@router.post("/login")
async def login(request: AuthRequest):
    employee = await employee_crud.get_by_phone(request.phone)
    if not employee:
        raise NotFound(detail="Employee not found in database")
    if employee.tg_id is None:
        encoded_phone = base64.b64encode(request.phone.encode('utf-8')).decode()
        bot_link = f"https://t.me/WBtrackAuth_bot?start={encoded_phone}"
        return RegisterResponse(registration_link=bot_link)

    otp = f"{secrets.randbelow(1000000):06}"
    text = f"Код для входа в ЛК WBTRACK - {otp}"
    await redis_client.set(f"otp:{request.phone}", otp, ex=60)
    chat_id = employee.tg_id
    await client.get(f"{BASE_URL}/sendMessage?chat_id={chat_id}&text={text}")
    return {"message": "OTP has been sent"}


@router.post("/confirm")
async def confirm_code(request: AuthRequest):
    stored_otp = await redis_client.get(f"otp:{request.phone}") or None
    print(stored_otp)
    if not stored_otp:
        raise NotFound(detail="No OTP found in database")
    if stored_otp != request.otp:
        raise ValidationError(detail="Invalid OTP code")

    employee = await employee_crud.get_by_phone(request.phone)
    access_token = create_employee_jwt_access(employee)
    refresh_token = create_employee_jwt_refresh(employee)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/me")
async def get_info_employee(employee: Employee = Depends(get_currrent_employee)):
    return employee


@router.get(path="",
            response_model=IResponsePaginated[IEmployeeRead])
async def get_list(
        params: LimitOffsetParams = Depends(),
        current_user: User = Depends(current_active_user),
        order_by: str = Query(None, description="Поле для сортировки"),
        order: ListOrderEnum = Query(ListOrderEnum.descendent, description="Направление сортировки")


):
    """Получения списка сотрудников связанных с текущим пользователем

    - **limit**: количество элементов на странице
    - **offset**: смещение от начала списка
    - **order_by**: поле для сортировки (доступные поля create_date, name, last_name, is_deleted, phone, tg_id)
    - **order**: направление сортировки (asc/desc)
    """
    user_id = current_user.id
    logger.info(f"User id of current user - {user_id}")
    sortable_columns = Employee.__table__.columns.keys()

    if order_by and order_by not in sortable_columns:
        raise ValidationError(f"Некорректное поле для сортировки: {order_by}. Доступные поля: {', '.join(sortable_columns)}")
    order_by = order_by or "id"


    page = await employee_crud.get_employees_by_user_id(
        user_id=user_id,
        params=params,
        order_by=order_by,
        order=order
    )
    return page


@router.post(path="/search", response_model=IResponsePaginated[IEmployeeRead])
async def search_employees(
        *,
        order_by: str = "id",
        order: ListOrderEnum = ListOrderEnum.descendent,
        search_params: SearchParams,
        params: LimitOffsetParams = Depends(),
        user: User = Depends(current_active_user),
):
    """Search employees by last name or phone

    :param order_by: Order by field
    :param order: Order direction (asc or desc) Default: desc
    :param search_field: Search field
    :param search_value: Search value
    :param params: Pagination parameters
    :param user: Current active user
    """
    query = select(Employee)
    search_field = search_params.search_field
    search_value = search_params.search_value

    print(f"Search field: {search_field}, value: {search_value}")
    if search_field and search_value:
        if search_field == "last_name":
            query = query.where(Employee.last_name.startswith(search_value))

        elif search_field == "phone_number":
            query = query.where(
                func.array_to_string(Employee.phones, ',').ilike(f'{search_value}%')
            )

    page = await employee_crud.get_multi_paginated_ordered(
        query=query,
        order_by=order_by,
        order=order,
        params=params,
    )
    return page

add_pagination(router)









