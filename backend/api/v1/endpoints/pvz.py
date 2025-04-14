from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from api.dependencies.pvz import pvz_service_dependency
from core.redis import redis_client
from schemas.response import (
    PVZRequestCodeResponse,
    PVZValidateCodeResponse,
)
from services.pvz_service import PVZService

router = APIRouter(
    generate_unique_id_function=lambda route: f"pvz_{route.name}",
)




@router.post(
    "/request-code",
    response_model=PVZRequestCodeResponse,
    description="Запрос кода подтверждения для авторизации",
    responses={
        200: {
            "description": "Код успешно отправлен",
            "content": {
                "application/json": {
                    "example": {"message": "Code sent successfully", "code_length": 6}
                }
            }
        },
        400: {"description": "Ошибка в запросе"},
    }
)
async def request_pvz_code(
    pvz_service: Annotated[PVZService, pvz_service_dependency]
):
    """
    Запрашивает код подтверждения для авторизации.

    Требуется заголовок X-Phone-Number с номером телефона в формате 79XXXXXXXXX
    """
    try:
        
        code_response = await pvz_service.login()
        
        return {
            "message": "Code sent successfully",
            "code_length": code_response.code_length
        }
    except Exception as e:
        
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/validate-code",
    response_model=PVZValidateCodeResponse,
    description="Валидация кода подтверждения",
    responses={
        200: {
            "description": "Код успешно подтвержден",
            "content": {
                "application/json": {
                    "example": {"access_token": "your-access-token"}
                }
            }
        },
        401: {"description": "Неверный код"},
    }
)
async def validate_pvz_code(
    pvz_service: Annotated[PVZService, pvz_service_dependency],
    code: str = Query(..., description="Код подтверждения из кабинета WB")
):
    """
    Подтверждает код и возвращает токен доступа.

    - Требуется заголовок X-Phone-Number с номером телефона
    - Код подтверждения передается в параметре запроса
    """
    try:
        pickpoint_id = "65717"
        external_id = "141685"
        token_response = await pvz_service.validate_code(code, pickpoint_id, external_id)
        return {"access_token": token_response.access.token}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/pickpoints",
    description="Получение списка пунктов выдачи",
    responses={
        200: {"description": "Список пунктов выдачи успешно получен"},
        401: {"description": "Ошибка авторизации"},
    }
)
async def get_pickpoints(
    pvz_service: Annotated[PVZService, pvz_service_dependency]
):
    """
    Возвращает список доступных пунктов выдачи.

    Требуется заголовок X-Phone-Number и действующий токен авторизации
    """
    try:
        return await pvz_service.get_pickpoint_list()
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/owner-info",
    description="Получение информации о владельце",
    responses={
        200: {"description": "Информация успешно получена"},
        401: {"description": "Ошибка авторизации"},
    }
)
async def get_owner_info(
    pvz_service: Annotated[PVZService, pvz_service_dependency]
):
    """
    Возвращает информацию о владельце аккаунта.

    Требуется заголовок X-Phone-Number и действующий токен авторизации
    """
    try:
        return await pvz_service.get_owner_info()
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/pickpoint-rating/{pickpoint_id}",
    description="Получение информации о рейтинге пункта выдачи",
    responses={
        200: {"description": "Информация успешно получена"},
        401: {"description": "Ошибка авторизации"},
    }
)
async def get_pickpoint_rating(
    pvz_service: Annotated[PVZService, pvz_service_dependency],
    pickpoint_id: int
):
    """
    Возвращает рейтинг пункта выдачи.

    Требуется заголовок X-Phone-Number и действующий токен авторизации
    """
    try:
        return await pvz_service.get_pickpoint_rating(pickpoint_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


