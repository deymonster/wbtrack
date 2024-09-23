from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi_users.jwt import decode_jwt

from config import settings
from core.exceptions import NotAuthenticated, NotFound
from crud.employee import employee_crud
from models.employee import Employee
from fastapi import HTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/employee/login")


async def get_currrent_employee(token: str = Depends(oauth2_scheme)) -> Employee:
    try:
        payload = decode_jwt(token, settings.APP_SECRET_KEY, audience=["employee"])
        employee_id = payload["sub"]
        print(payload)
        if not employee_id:
            raise NotAuthenticated(detail="Invalid refresh token")
        employee = await employee_crud.get(id=employee_id)
        print(f"employee: {employee}")
        if not employee or employee.is_deleted:
            raise NotFound(detail="Employee is deleted or not found")
        return employee
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid refresh token - {e}")


