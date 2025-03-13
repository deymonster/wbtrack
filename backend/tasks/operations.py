import logging
import json
from itertools import islice
from typing import List, Dict, Any, Type
from core.celery_app import celery_app
from core.redis import redis_client
from services.pvz_service import PVZService
from datetime import datetime
import asyncio
from crud import * 
from schemas.company import ICompanyCreate
from schemas.office import IOfficeCreate
from schemas.employee import IEmployeeCreate
from schemas.employee_office_link import IEmployeeOfficeLinkCreate
from schemas.operation import IOperationCreate
from schemas.categories_operation import ICategoryOperationCreate
from schemas.operation_name import IOperationNameCreate
from crud.base import CRUDBase
from pydantic import BaseModel
from core.db import get_db_session_instance
from sqlalchemy.ext.asyncio import AsyncSession
from crud.company import company_crud
from crud.employee import employee_crud
from crud.employee_office_link import employee_office_link_crud
from crud.operation import operation_crud
from crud.office import office_crud
from crud.categories_operation import categories_operation_crud
from crud.operation_name import operation_name_crud
from models.user import User
import sqlalchemy.exc

logger = logging.getLogger(__name__)

@celery_app.task(
    name="fetch_operations",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    rate_limit="10/m"
)
def fetch_operations(self, phone: str, date_from: str, date_to: str, chunk_size: int = 100) -> Dict[str, Any]:
    """
    Celery задача для получения операций с поддержкой повторных попыток и ограничением частоты
    """
    logger.info(f"Starting operations fetch for period {date_from} to {date_to}")

    def chunks(iterable, size):
        """Разделяет данные на чанки заданного размера."""
        it = iter(iterable)
        while chunk := list(islice(it, size)):
            yield chunk

    async def process_chunk(chunk, office_map, employee_map):
        """Асинхронная обработка чанка операций"""
        operation_data = []
        missing_offices = set()  # Для отслеживания отсутствующих офисов
        
        for operation in chunk:
            db_office = office_map.get(operation.pickpoint_id)
            db_employee = employee_map.get(operation.employee_id)
            
            if db_office is None:
                missing_offices.add(operation.pickpoint_id)
                logger.warning(f"Office not found for pickpoint_id: {operation.pickpoint_id}")
                continue  # Пропускаем операции с отсутствующими офисами
            
            operation_data.append({
                "operation_id": operation.operation_id,
                "operation_type": operation.operation_type,
                "summ": operation.summ,
                "rids": operation.rids,
                "created": datetime.fromisoformat(operation.created),
                "currency": operation.currency,
                "description": operation.description,
                "summ_pickpoint": operation.summ_pickpoint,
                "office_id": db_office.id,
                "employee_id": db_employee.id if db_employee else None,
            })
        
        if missing_offices:
            logger.error(f"Missing offices with pickpoint_ids: {sorted(list(missing_offices))}")
        
        return operation_data
    
    async def save_chunked_operations(operation_objects, chunk_size, db_session):
        """Сохранение операций по чанкам с асинхронной обработкой."""
        total_operations = len(operation_objects)
        saved_operations = 0
        
        for chunk in chunks(operation_objects, chunk_size):
            try:
                await operation_crud.create_or_update_multi(
                    list_in=chunk,
                    index_elements=["operation_id"],
                    on_conflict_set={
                        "operation_type",
                        "summ",
                        "rids",
                        "created",
                        "currency",
                        "description",
                        "summ_pickpoint",
                        "office_id",
                        "employee_id"
                    },
                    db_session=db_session
                )
                saved_operations += len(chunk)
                progress = 50 + int((saved_operations / total_operations) * 50)  # От 50% до 100%
                self.update_state(
                    state='PROGRESS',
                    meta={
                        'progress': progress,
                        'status': f'Сохранено операций: {saved_operations}/{total_operations}'
                    }
                )
            except Exception as e:
                logger.error(f"Error saving chunk: {e}")
                raise


    async def run_task():
        try:
            # Обновляем статус задачи
            self.update_state(state='PROGRESS', meta={'progress': 0, 'status': 'Инициализация'})

            # Инициализируем сервис
            service = PVZService(redis_client=redis_client, phone=phone)

            # Получаем операции
            operations = await service.get_operations(
                date_from=date_from,
                date_to=date_to,
                progress_callback=lambda current, total: self.update_state(
                    state='PROGRESS',
                    meta={
                        'progress': int((current / total) * 50),  # 50% на получение данных
                        'status': f'Получено операций: {current}/{total}'
                    }
                )
            )
            logger.info(f"Received {len(operations)} operations from service")
            

            total_operations = len(operations)
            if total_operations == 0:
                logger.info("No operations found.")
                self.update_state(state='SUCCESS', meta={'progress': 100, 'status': 'Нет операций для сохранения'})
                return {"status": "success", "message": "No operations to save"}

            processed_operations = 0

            # Загружаем все офисы и сотрудников
            async with get_db_session_instance() as session:
                office_map = await office_crud.get_all_offices(db_session=session)
                employee_map = await employee_crud.get_all_employees(db_session=session)

                # Обрабатываем операции по чанкам
                tasks = [process_chunk(chunk, office_map, employee_map) for chunk in chunks(operations, chunk_size)]
                all_operation_data = await asyncio.gather(*tasks)
                flat_operation_data = [item for sublist in all_operation_data for item in sublist] # "выпрямить" вложенные списки

                # Преобразуем данные в объекты для сохранения
                operation_objects = [IOperationCreate(**operation) for operation in flat_operation_data]
                await save_chunked_operations(operation_objects, chunk_size=chunk_size, db_session=session)

            self.update_state(state='SUCCESS', meta={'progress': 100, 'status': 'Операции успешно сохранены'})
            return {"status": "success", "message": f"Successfully processed {total_operations} operations"}
        except Exception as exc:
            logger.error(f"Error fetching and saving operations: {str(exc)}")
            self.update_state(state='FAILURE', meta={
                'exc_type': exc.__class__.__name__,
                'exc_message': str(exc),
                'progress': 0,
                'status': f'Ошибка: {str(exc)}'
            })
            raise 
    # Запускаем асинхронную задачу 
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(run_task())
    except Exception as exc:
        logger.error(f"Task failed: {exc.__class__.__name__}: {str(exc)}")
        return {
            "status": "error",
            "error_type": exc.__class__.__name__,
            "message": str(exc)
        }




@celery_app.task(
    name="fetch_static_data",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    rate_limit="10/m"
)
def fetch_static_data(self, phone: str) -> Dict[str, Any]:
    """
    Celery задача для получения статических данных с поддержкой повторных попыток и ограничением частоты
    """
    logger.info(f"Fetching static data for phone: {phone}")
    
    async def fetch_task():
        try:
            service = PVZService(redis_client=redis_client, phone=phone)

            # Асинхронное получение данных
            pickpoint_list_with_employees = await service.get_pickpoint_list()
            owner_info = await service.get_owner_info()
            categories = await service.get_operation_category()

            # Преобразуем в сериализуемый формат
            pickpoint_list_serializable = [p.dict() for p in pickpoint_list_with_employees]
            owner_info_serializable = owner_info.dict()
            categories_serializable = categories.dict()

            logger.info(
                f"Successfully fetched static data: "
                f"Company: {owner_info_serializable}, Offices with employees: {len(pickpoint_list_serializable)}"
            )
            return {
                "status": "success",
                "pickpoint_list": pickpoint_list_serializable,
                "owner_info": owner_info_serializable,
                "categories": categories_serializable,
                "completed_at": datetime.now().isoformat()
            }
        except Exception as exc:
            logger.error(f"Error fetching static data: {str(exc)}")
            raise exc

    # Создаём loop и запускаем задачу
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        result = loop.run_until_complete(fetch_task())
        return result
    except Exception as exc:
        logger.error(f"Error in Celery task: {str(exc)}")
        self.retry(exc=exc)



async def save_data(
    data_list: List[dict],
    crud_instance: CRUDBase,
    schema: Type[BaseModel],
    index_elements: List[str],
    on_conflict_set: set[str],
    session: AsyncSession
) -> None:
    """
    Универсальная функция для сохранения данных.

    :param data_list: Список словарей с данными для сохранения.
    :param crud_instance: Экземпляр CRUD-класса.
    :param schema: Схема для валидации данных.
    :param index_elements: Поля для проверки уникальности (индексы).
    :param on_conflict_set: Поля для обновления при конфликте.
    :param session: Активная сессия базы данных.
    """
    schema_objects = [schema(**data) for data in data_list]

    await crud_instance.create_or_update_multi(
        list_in=schema_objects,
        index_elements=index_elements,
        on_conflict_set=on_conflict_set,
        db_session=session,
  
    )

@celery_app.task(
    name="save_static_data",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    rate_limit="10/m"
)
def save_static_data(self, static_data: Dict[str, Any], user_id: int) -> None:
    """Сохранение статических данных в БД"""
    logger.info(f"Saving static data to DB: {static_data}")

    async def run_task():
        async with get_db_session_instance() as session:
            try:
                logger.info("Received static_data:")
                logger.info(f"Keys in static_data: {static_data.keys()}")
                logger.info(f"Categories data keys: {static_data.get('categories', {}).keys()}")
                
                #Извлечение данных из словаря
                company_data = static_data.get("owner_info", {})
                offices_data = static_data.get("pickpoint_list", [])
                categories_data = static_data.get("categories", {})
                operations_data = categories_data.get("operations", [])

                logger.info(f"Static data keys: {static_data.keys()}")
                logger.info(f"Categories data keys: {categories_data.keys()}")
                logger.info(f"Raw data: categories={len(categories_data.get('categories', []))}, operations={len(operations_data)}")

                # Создаем словарь операций для быстрого доступа
                operations_dict = {str(op["id"]): op for op in operations_data}
                logger.info(f"Created operations dictionary with {len(operations_dict)} items")
                logger.info(f"Available operation IDs: {list(operations_dict.keys())}")
                logger.info(f"Operations data sample: {operations_data[:2] if operations_data else 'No operations'}")

                # Сохранение категорий и названий операций
                if categories_data:
                    # Сохраняем категории
                    categories_list = categories_data.get("categories", [])
                    logger.info(f"Processing {len(categories_list)} categories")
                    
                    for category in categories_list:
                        try:
                            logger.info(f"Processing category {category['id']}: {category['name']}")
                            logger.info(f"Category operations: {category.get('operations', [])}")
                            logger.info(f"Category raw data: {category}")
                            
                            # Сохраняем категорию
                            db_category = await categories_operation_crud.get_by_external_id(
                                external_id=category["id"],
                                db_session=session
                            )
                            if not db_category:
                                logger.info(f"Creating new category {category['id']}")
                                await save_data(
                                    data_list=[{
                                        "external_id": category["id"],
                                        "name": category["name"],
                                        "description": category["description"]
                                    }],
                                    crud_instance=categories_operation_crud,
                                    schema=ICategoryOperationCreate,
                                    index_elements=["external_id"],
                                    on_conflict_set={"name", "description"},
                                    session=session
                                )
                                # Получаем созданную категорию
                                db_category = await categories_operation_crud.get_by_external_id(
                                    external_id=category["id"],
                                    db_session=session
                                )

                            # Если категория существует, сохраняем её операции
                            if db_category:
                                # Сохраняем операции для этой категории
                                category_operations = []
                                for op_id in category.get("operations", []):
                                    op_id_str = str(op_id)
                                    if op_id_str in operations_dict:
                                        category_operations.append(operations_dict[op_id_str])
                                    else:
                                        logger.warning(f"Operation {op_id} not found in operations dictionary")
                                
                                logger.info(f"Found {len(category_operations)} operations for category {category['id']}")
                                
                                for operation in category_operations:
                                    try:
                                        logger.info(f"Saving operation {operation['id']}: {operation['name']} for category {db_category.id}")
                                        await save_data(
                                            data_list=[{
                                                "external_id": operation["id"],
                                                "base_name": operation["base_name"],
                                                "name": operation["name"],
                                                "description": operation.get("description", ""),
                                                "minus_name": operation.get("minus_name", ""),
                                                "minus_description": operation.get("minus_description", ""),
                                                "category_id": db_category.id
                                            }],
                                            crud_instance=operation_name_crud,
                                            schema=IOperationNameCreate,
                                            index_elements=["external_id"],
                                            on_conflict_set={
                                                "base_name",
                                                "name",
                                                "description",
                                                "minus_name",
                                                "minus_description",
                                                "category_id"
                                            },
                                            session=session
                                        )
                                    except Exception as e:
                                        logger.error(f"Error saving operation {operation['id']}: {str(e)}")
                                        logger.error(f"Operation data: {operation}")
                                        # Пропускаем ошибку и продолжаем с следующей операцией
                                        continue
                        except Exception as e:
                            logger.error(f"Error processing category {category['id']}: {str(e)}")
                            # Пропускаем ошибку и продолжаем с следующей категорией
                            continue

                # Сохранение данных компании
                if company_data:
                    try:
                        logger.info(f"Attempting to create/update company with wb_user_id: {company_data['wb_user_id']}")
                        # Проверяем существование компании
                        existing = await company_crud.get_company_by_wb_user_id(
                            wb_user_id=company_data["wb_user_id"],
                            db_session=session
                        )
                        logger.info(f"Existing company found: {existing is not None}")
                        company = await company_crud.create_or_update(
                            obj_in=ICompanyCreate(
                                wb_user_id=company_data["wb_user_id"],
                                name=company_data["name"],
                                phone=str(company_data["phone"]),
                                org_name=company_data["org_name"],
                            ),
                            index_elements=["wb_user_id"],
                            create_exclude={"id"},
                            update_exclude={"id"},
                            db_session=session,
                        )
                        logger.info(f"Company created/updated successfully: {company.id}")
                    except sqlalchemy.exc.IntegrityError as e:
                        await session.rollback()
                        logger.error(f"Integrity error: {e.orig}")
                        logger.error(f"Conflict occurred on data: {company_create_data.model_dump()}")
                        raise HTTPException(
                            status_code=409,
                            detail=f"Integrity error: {str(e.orig)}",
                        )

                    # Создание связи между пользователем и компанией
                    user = await session.get(User, user_id)
                    if not user:
                        raise ValueError(f"User with id {user_id} not found")
                    await company_crud.add_user(
                        company=company,
                        user=user,
                        db_session=session,
                    )

                
                # Сохранение данных офисов и сотрудников
                if offices_data:
                    company = await company_crud.get_company_by_wb_user_id(wb_user_id=company_data["wb_user_id"], db_session=session)
                    if not company:
                        logger.error(f"Company with wb_user_id={company_data['wb_user_id']} not found.")
                        return
                    # Сохраняем офисы
                    office_data = [
                        {
                            "office_id": office["id"],
                            "name": office["name"],
                            "latitude": office["latitude"],
                            "longitude": office["longitude"],
                            "is_active": office["is_active"],
                            "external_id": office["external_id"],
                            "rate": office.get("rate", 0.0),
                            "company_id": company.id
                        }
                        for office in offices_data
                    ]
                    await save_data(
                        data_list=office_data,
                        crud_instance=office_crud,
                        schema=IOfficeCreate,
                        index_elements=["office_id"],
                        on_conflict_set={"name", "latitude", "longitude", "is_active", "external_id", "rate"},
                        session=session
                    )
                    

                    employee_office_links = []

                    for office in offices_data:
                        for user in office["users"]:
                            # Проверяем существование сотрудника
                            existing_employee = await employee_crud.get_by_phone(phone=str(user["phone"]), db_session=session)

                            # Найти реальный id офиса в БД
                            db_office = await office_crud.get_by_office_id(office_id=office["id"], db_session=session)

                            if not db_office:
                                logger.error(f"Office with office_id={office['id']} not found in the database.")
                                continue

                            real_office_id = db_office.id

                            if existing_employee:
                                # Проверяем существующую связь
                                existing_link = await employee_office_link_crud.get_link(
                                    employee_id=existing_employee.id,
                                    office_id=real_office_id,
                                    db_session=session
                                )
                                if not existing_link:
                                    # 
                                    employee_office_links.append({
                                        "employee_id": existing_employee.id,
                                        "office_id": real_office_id,
                                    })

                            else:
                                try:
                                    # Создаём нового сотрудника
                                    new_employee_data = {
                                        "user_id": user["user_id"],
                                        "name": user["name"],
                                        "last_name": user["last_name"],
                                        "phone": str(user["phone"]),
                                        "is_deleted": user["is_deleted"],
                                        "tg_id": None,
                                    }
                                    new_employee = await employee_crud.create(
                                        obj_in=IEmployeeCreate(**new_employee_data), db_session=session
                                    )
                                    # Добавляем связь нового сотрудника и офиса в список
                                    employee_office_links.append({
                                        "employee_id": new_employee.id,
                                        "office_id": real_office_id,
                                    })
                                except Exception as exc:
                                    logger.error(f"Error creating employee {user['name']}: {str(exc)}")
                                    continue

                    # Массово создаём связи
                    if employee_office_links:
                        await save_data(
                            data_list=employee_office_links,
                            crud_instance=employee_office_link_crud,
                            schema=IEmployeeOfficeLinkCreate,  
                            index_elements=["employee_id", "office_id"],
                            on_conflict_set=set(["employee_id", "office_id"]),  
                            session=session
                        )

                logger.info("Static data saved successfully")

            except Exception as exc:
                logger.error(f"Error saving static data: {str(exc)}")
                self.retry(exc=exc)

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            logger.info("Using running event loop")
            asyncio.ensure_future(run_task())
        else:
            loop.run_until_complete(run_task())
    except Exception as exc:
        logger.error(f"Task failed: {exc.__class__.__name__}: {str(exc)}")
        raise
