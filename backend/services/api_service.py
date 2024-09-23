import inspect
from typing import Callable, Any
from wb_franchise_api_client.api_auth import ApiAuth
from wb_franchise_api_client.api_client import ApiClient


class ApiClientWrapper:
    def __init__(self, api_client: ApiClient, redis_client, api_auth: ApiAuth):
        self.api_client = api_client
        self.redis_client = redis_client
        self.api_auth = api_auth

    def __getattr__(self, name: str) -> Callable:
        method = getattr(self.api_client, name, None)
        if method and inspect.iscoroutinefunction(method):
            return self._create_method_wrapper(method)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def _create_method_wrapper(self, method: Callable) -> Callable:
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await method(self.api_client, *args, **kwargs)
            except Exception as e:
                if e.status == 401:
                    phone = kwargs.get("phone")
                    if not phone:
                        raise Exception("Phone number must be provided to refresh token")

                    refresh_token = await self.redis_client.get(f"{phone}:refresh_token")
                    if not refresh_token:
                        raise Exception("Refresh token not found")

                    new_tokens = await self.api_auth.connect_code(username=phone, refresh_token=refresh_token)
                    self.api_client.update_access_token(new_tokens.access_token)
                    await self.redis_client.set(f"{phone}:access_token", new_tokens.access_token)

                    return await method(self.api_client, *args, **kwargs)
                else:
                    raise e

        return wrapper


















