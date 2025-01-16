from pvz_client.api_auth import ApiAuth
from redis.asyncio import Redis
from pvz_client.api_client import ApiClient
from config import settings
from pvz_client.models import *
import logging
import asyncio

logger = logging.getLogger(__name__)

class PVZService:
    def __init__(self, redis_client: Redis, phone: str):
        self.redis = redis_client
        self.phone = phone
        self.auth = ApiAuth(
            auth_base_path=settings.AUTH_BASE_PATH,
            base_path=settings.AUTH_BASE_PATH
        )

    async def _get_api_client(self) -> ApiClient:
        """Создает экземпляр ApiClient с токеном"""
        token = await self.get_token()
        return ApiClient(access_token=token)

    async def login(self) -> RequestCodeResponse:
        """Первый запрос для получения кода"""
        code_response = await self.auth.login(self.phone)
        print(f"Got code response: {code_response}")

        # Сохраняем временный токен в Redis
        redis_key = f"pvz:{self.phone}:temp_token"
        await self.redis.set(
            redis_key,
            code_response.data,
            ex=300
        )

        saved_token = await self.redis.get(redis_key)
        print(f"Saved token in Redis: {saved_token}")

        return code_response

    async def validate_code(self, code: str) -> TokenResponse:
        """Второй запрос для получения токена"""
        # Получаем временный токен из Redis
        temp_token = await self.redis.get(f"pvz:{self.phone}:temp_token")
        if not temp_token:
            raise ValueError("Temporary token not found. Please request a new code.")
        
        # Валидируем код и получаем постоянные токены
        token_response = await self.auth.validate(code=code, token=temp_token)

        # Сохраняем access токен в Redis с TTL из ответа
        await self.redis.set(
            f"pvz:{self.phone}:access_token",
            token_response.access.token,
            ex=token_response.access.ttl
        )

        # Удаляем временный токен
        await self.redis.delete(f"pvz:{self.phone}:temp_token")

        return token_response

    async def get_token(self) -> str:
        """Получаем access токен из Redis"""
        access_token = await self.redis.get(f"pvz:{self.phone}:access_token")
        if not access_token:
            raise ValueError("Access token not found for this phone number")
        return access_token
       
    async def validate_token(self) -> bool:
        """Проверяем валидность и существование access токена"""
        return await self.redis.exists(f"pvz:{self.phone}:access_token")

    # api_client methods
    async def get_pickpoint_list(self) -> List[PickpointModel]:
        """Получение списка пунктов выдачи"""
        client = await self._get_api_client()
        return await client.get_pickpoint_list()

    async def get_owner_info(self) -> OwnerInfoModel:
        """Получение информации о владельце"""
        client = await self._get_api_client()
        return await client.get_owner_info()

    async def get_pickpoint_rating(self, pickpoint_id: int) -> float:
        """Получение рейтинга пункта выдачи"""
        client = await self._get_api_client()
        return await client.get_pickpoint_rating(pickpoint_id)

    async def get_operation_category(Self) -> CategoriesOperationsResponse:
        """Получение категорий и названий операций - вознаграждений"""

        client = await self._get_api_client()
        return await client.get_operations_name()

    async def get_operations(self, *, date_from: str, date_to: str, chunk_size: int = 3, progress_callback: None) -> List[OperationModel]:
        """Получение списка операций за период с параллельной пагинацией

        Args:
            date_from: Начальная дата (в формате YYYY-MM-DD)
            date_to: Конечная дата (в формате YYYY-MM-DD)
            chunk_size: Количество параллельных запросов (по умолчанию 3)

        Returns:
            List[OperationModel]: Полный список операций за период
        """
        client = await self._get_api_client()
        logger.info(f"Getting operations from {date_from} to {date_to}")
        
        try:
            # Первый запрос для получения общего количества
            initial_response = await client.get_operations(date_from=date_from, date_to=date_to, offset=0, limit=1)
            total_rows = initial_response.total_rows
            logger.info(f"Total operations to fetch: {total_rows}")

            if total_rows == 0:
                return []

            limit = 100
            offsets = range(0, total_rows, limit)
            all_operations = []

            # Разбиваем offsets на чанки для параллельных запросов
            for i in range(0, len(offsets), chunk_size):
                chunk_offsets = offsets[i:i + chunk_size]
                tasks = []
            
                for offset in chunk_offsets:
                    task = asyncio.create_task(
                        self._fetch_operations_with_retry(
                            client=client,
                            date_from=date_from,
                            date_to=date_to,
                            offset=offset,
                            limit=limit
                        )
                    )
                    tasks.append(task)

                try:
                    # Выполняем запросы параллельно
                    chunk_responses = await asyncio.gather(*tasks, return_exceptions=True)
                    # Обрабатываем результаты, включая возможные исключения
                    for response in chunk_responses:
                        if isinstance(response, Exception):
                            logger.error(f"Error in batch: {str(response)}")
                            continue
                        all_operations.extend(response.data)
                        if progress_callback:
                            progress_callback(len(all_operations), total_rows)
                        logger.info(f"Fetched batch. Total so far: {len(all_operations)}/{total_rows}")

                    await asyncio.sleep(0.5)
                except Exception as e:
                    logger.error(f"Error in parallel operations fetch: {str(e)}")
                    continue

            logger.info(f"Successfully fetched {len(all_operations)} operations out of {total_rows}")
            if len(all_operations) < total_rows:
                logger.warning(f"Only {len(all_operations)} operations fetched, but {total_rows} expected.")

            return all_operations
        except Exception as e:
            logger.error(f"Error in get_operations: {str(e)}")
            raise

    
    async def _fetch_operations_with_retry(self, client, date_from: str, date_to: str, offset: int, limit: int, max_retries: int = 3, initial_delay: float = 1.0):

        """Получение операций с механизмом повторных попыток"""
        delay = initial_delay
        last_exception = None   

        for attempt in range(max_retries):
            try:
                return await client.get_operations(
                    date_from=date_from,
                    date_to=date_to,
                    offset=offset,
                    limit=limit
                )
            except Exception as e:
                last_exception = e
                if attempt < max_retries - 1:
                    logger.warning(f"Attempt {attempt + 1} failed for offset {offset}: {str(e)}")
                    await asyncio.sleep(delay)
                    delay *= 2  # Экспоненциальная задержка
                else:
                    logger.error(f"All retries failed for offset {offset}: {str(e)}")
                raise last_exception