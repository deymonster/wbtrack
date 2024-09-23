from config import settings
from wb_franchise_api_client.api_client import ApiAuth, ApiClient
from core.redis import redis_client


async def get_api_auth() -> ApiAuth:
    """
    Get ApiAuth instance
    """
    api_auth = ApiAuth(
        auth_base_path=settings.AUTH_BASE_PATH,
        base_path=settings.WILDBERRIES_BASE_PATH,
        basic_token=settings.WB_BASIC_TOKEN
    )
    return api_auth


async def get_api_client(phone: str) -> ApiClient:
    """Get ApiClient instance

    :param phone: phone number
    :return: ApiClient instance
    """
    api_auth = await get_api_auth()
    return ApiClient(
        api_auth=api_auth,
        redis_client=redis_client,
        phone=phone
    )


