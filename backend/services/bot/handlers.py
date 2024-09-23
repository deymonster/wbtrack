from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.filters.command import CommandObject
from aiogram.types import Message
import base64

from core.db import get_db_session
from core.redis import redis_client
from crud.employee import employee_crud
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import IUserCreate
from services.user import UserService

router = Router()

Session = get_db_session()


def decode_phone_number(encoded_phone: str) -> str:
    decoded_bytes = base64.b64decode(encoded_phone.encode('utf-8'))
    return decoded_bytes.decode('utf-8')


@router.message(CommandStart())
async def start(message: Message, command: CommandObject):
    tg_id = message.from_user.id
    print(f'TG id-{tg_id}')
    args = command.args
    print(f"args-{args}")
    # username = message.from_user.username or "неизвестный"
    # text = message.text.strip()
    # print(f"text-{text}")
    if not args:
        await message.answer("Incorrect command")

    phone_number = decode_phone_number(args)

    async with Session() as session:
        employee = await employee_crud.get_by_phone(phone_number, session)
        # update employee
        update_data = {"tg_id": tg_id}
        await employee_crud.update(obj_current=employee, obj_new=update_data, db_session=session)
        await message.answer(f"Успешная регистрация!")










