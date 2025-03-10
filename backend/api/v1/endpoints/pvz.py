from fastapi import APIRouter, Depends, HTTPException, Header, Query
from services.pvz_service import PVZService
from core.redis import redis_client
from schemas.response import (
    PVZRequestCodeResponse,
    PVZValidateCodeResponse,
)
from typing import Annotated
from core.celery_app import celery_app
from tasks.operations import fetch_operations, fetch_static_data, save_static_data
from api.dependencies.user import current_active_user
from models.user import User

router = APIRouter(
    generate_unique_id_function=lambda route: f"pvz_{route.name}",
)


async def get_phone_number(
    x_phone_number: Annotated[str, Header(alias="X-Phone-Number")]
) -> str:
    """Get phone number from header."""
    return x_phone_number


async def get_pvz_service(
    phone: Annotated[str, Depends(get_phone_number)]
) -> PVZService:
    """Get PVZ service instance."""
    return PVZService(redis_client=redis_client, phone=phone)


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
    pvz_service: Annotated[PVZService, Depends(get_pvz_service)]
):
    """
    Запрашивает код подтверждения для авторизации.
    
    Требуется заголовок X-Phone-Number с номером телефона в формате 79XXXXXXXXX
    """
    try:
        code_response = await pvz_service.login()
        print(code_response)
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
    pvz_service: Annotated[PVZService, Depends(get_pvz_service)],
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
    except ValueError as e:
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
    pvz_service: Annotated[PVZService, Depends(get_pvz_service)]
):
    """
    Возвращает список доступных пунктов выдачи.
    
    Требуется заголовок X-Phone-Number и действующий токен авторизации
    """
    try:
        return await pvz_service.get_pickpoint_list()
    except ValueError as e:
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
    pvz_service: Annotated[PVZService, Depends(get_pvz_service)]
):
    """
    Возвращает информацию о владельце аккаунта.
    
    Требуется заголовок X-Phone-Number и действующий токен авторизации
    """
    try:
        return await pvz_service.get_owner_info()
    except ValueError as e:
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
    pvz_service: Annotated[PVZService, Depends(get_pvz_service)],
    pickpoint_id: int
):
    """
    Возвращает рейтинг пункта выдачи.
    
    Требуется заголовок X-Phone-Number и действующий токен авторизации
    """
    try:
        return await pvz_service.get_pickpoint_rating(pickpoint_id)
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/operations/fetch",
    description="Запуск асинхронного получения операций",
    responses={
        202: {"description": "Задача поставлена в очередь"},
        401: {"description": "Ошибка авторизации"},
    }
)
async def start_operations_fetch(
    phone: Annotated[str, Depends(get_phone_number)],
    date_from: str = Query(..., description="Начальная дата (YYYY-MM-DD)"),
    date_to: str = Query(..., description="Конечная дата (YYYY-MM-DD)"),
):
    """
    Запускает асинхронную задачу получения операций.
    
    - Требуется заголовок X-Phone-Number
    - Даты должны быть в формате YYYY-MM-DD
    - Возвращает ID задачи для проверки статуса
    """
    try:
        task = fetch_operations.delay(phone, date_from, date_to)
        return {
            "task_id": task.id,
            "status": "accepted",
            "message": "Task has been queued"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/operations/status/{task_id}",
    description="Проверка статуса получения операций",
    responses={
        200: {"description": "Информация о статусе задачи"},
        404: {"description": "Задача не найдена"},
    }
)
async def get_operations_status(task_id: str):
    """
    Проверяет статус задачи получения операций
    """
    try:
        task = celery_app.AsyncResult(task_id)
        
        if task.state == 'PENDING':
            response = {
                "status": "pending",
                "progress": 0,
                "message": "Task is pending"
            }
        elif task.state == 'PROGRESS':
            response = {
                "status": task.state,
                "progress": task.info.get('progress', 0),
                "message": task.info.get('status', 'Task in progress')
            }
        elif task.state == 'SUCCESS':
            response = {
                "status": task.state,
                "progress": 100,
                "result": task.result,
                "message": "Task completed successfully"
            }
        elif task.state == 'FAILURE':
            response = {
                "status": "error",
                "progress": 0,
                "message": str(task.info),
            }
        else:
            response = {
                "status": task.state,
                "progress": 0,
                "message": "Unknown task state"
            }
        
        return response
    except Exception as e:
        logger.error(f"Error checking task status: {e}")
        raise HTTPException(status_code=404, detail="Task not found")


@router.post("/static-data/fetch", description="Запуск задачи получения и сохранения статичных данных",
             responses={
                202: {
                    "description": "Задача успешно поставлена в очередь",
                    "content": {
                        "application/json": {
                            "example": {"task_id": "task-id", "status": "accepted", "message": "Task has been queued"}
                        }
                    }
                },
                400: {"description": "Ошибка в запросе"},
             }
)
async def start_static_data_fetch(
    phone: Annotated[str, Depends(get_phone_number)],
    current_user: User = Depends(current_active_user)):
    """Запускает задачу получения и сохранения статичных данных.

    Требуется заголовок X-Phone-Number с номером телефона.
    Возвращает ID задачи для проверки статуса."""

    
    
    try:
        # Связываем задачи в цепочку Celery
        # fetch_task = fetch_static_data.delay(phone)
        chain_task = (fetch_static_data.s(phone) | save_static_data.s(user_id=current_user.id)).apply_async()

        # Запускаем задачу сохранения данных после получения
        
        return {
            "fetch_task_id": chain_task.parent.id,
            "chain_task_id": chain_task.id,
            "status": "accepted",
            "message": "Task has been queued"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/static-data/status/{task_id}", 
            description="Проверка статуса задачи",
    responses={
        200: {"description": "Информация о статусе задачи"},
        404: {"description": "Задача не найдена"},
    }
    )
async def check_static_data_fetch_status(task_id: str):
    """
    Проверяет статус задачи (получение или сохранение статичных данных).
    """
    try:
        task = celery_app.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                'status': 'pending',
                'current': 0,
                'total': 1,
                'message': 'Task is pending'
            }
        elif task.state == 'FAILURE':
            response = {
                'status': 'error',
                'error': str(task.info),
            }
        else:
            response = {
                'status': task.state,
                'result': task.result,
            }
        
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail="Task not found")


@router.post(
    "/operations/fetch",
    description="Запуск задачи получения и сохранения операций",
    responses={
        202: {"description": "Задача поставлена в очередь"},
        400: {"description": "Ошибка в запросе"},
    }
)
async def start_operations_fetch(
    phone: Annotated[str, Depends(get_phone_number)],
    date_from: str = Query(..., description="Начальная дата (YYYY-MM-DD)"),
    date_to: str = Query(..., description="Конечная дата (YYYY-MM-DD)"),
    current_user: User = Depends(current_active_user)
    ):
    """
    Запускает задачу получения и сохранения операций.
    
    - Требуется заголовок X-Phone-Number с номером телефона
    - Даты должны быть в формате YYYY-MM-DD
    - Возвращает ID задачи для проверки статуса
    """
    try:
        # Запускаем задачу получения операций
        task = fetch_operations.delay(phone, date_from, date_to)
        return {
            "task_id": task.id,
            "status": "accepted",
            "message": "Task has been queued"
        }
    except Exception as e:
        logger.error(f"Error starting task: {e}")
        raise HTTPException(status_code=400, detail="Failed to start the task")


@router.get(
    "/operations/status/{task_id}",
    description="Проверка статуса задачи получения и сохранения операций",
    responses={
        200: {"description": "Информация о статусе задачи"},
        404: {"description": "Задача не найдена"},
    }
)
async def check_operations_fetch_status(task_id: str):
    """
    Проверяет статус задачи получения и сохранения операций.
    
    - Требуется `task_id`, возвращённый при создании задачи.
    """
    try:
        task = celery_app.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                "status": "pending",
                "progress": 0,
                "message": "Task is pending"
            }
        elif task.state == 'PROGRESS':
            response = {
                "status": task.state,
                "progress": task.info.get('progress', 0),
                "message": task.info.get('status', 'Task in progress')
            }
        elif task.state == 'SUCCESS':
            response = {
                "status": task.state,
                "progress": 100,
                "result": task.result,
                "message": "Task completed successfully"
            }
        elif task.state == 'FAILURE':
            response = {
                "status": "error",
                "progress": 0,
                "message": str(task.info),
            }
        else:
            response = {
                "status": task.state,
                "progress": 0,
                "message": "Unknown task state"
            }
        
        return response
    except Exception as e:
        logger.error(f"Error checking task status: {e}")
        raise HTTPException(status_code=404, detail="Task not found")