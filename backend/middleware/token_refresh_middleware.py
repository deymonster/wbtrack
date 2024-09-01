from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import redis.asyncio as aioredis
from wb_franchise_api_client import ApiAuth


class TokenRefreshMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_client: aioredis.Redis, api_auth: ApiAuth):
        super().__init__(app)
        self.redis_client = redis_client
        self.api_auth = api_auth

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if response.status_code == 401:
            phone = request.headers.get("X-User-Phone")
            refresh_token = await self.redis_client.get(f"{phone}:refresh_token")

            if refresh_token:
                new_tokens = await self.api_auth.connect_code(username=phone, refresh_token=refresh_token)

                await self.redis_client.set(f"{phone}:access_token", new_tokens.access_token)
                await self.redis_client.set(f"{phone}:refresh_token", new_tokens.refresh_token)

                request.headers["Authorization"] = f"Bearer {new_tokens.access_token}"
                response = await call_next(request)

        return response



