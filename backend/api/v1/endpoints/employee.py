from fastapi import APIRouter, Request, Depends

from api.dependencies.employee import get_currrent_employee
from core.exceptions import NotFound, ValidationError
from core.user_management import create_employee_jwt_access, create_employee_jwt_refresh
from crud.employee import employee_crud
from models.employee import Employee
from schemas.employee import IEmployeeRead, RegistrationRequest, AuthRequest
from core.redis import redis_client
import base64
import string
import secrets
from config import settings

from schemas.user import RegisterResponse
import httpx

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




