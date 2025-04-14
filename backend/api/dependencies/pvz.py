from typing import Annotated

from fastapi import Depends, Header

from core.redis import redis_client
from services.pvz_service import PVZService


async def get_phone_number(
    x_phone_number: Annotated[str, Header(alias="X-Phone-Number")]
) -> str:
    """Get phone number from header."""
    if not x_phone_number:
        raise ValueError("Phone number is required")
    return x_phone_number


pvz_phone_dependency = Depends(get_phone_number)


async def get_pvz_service(
    phone: Annotated[str, pvz_phone_dependency]
) -> PVZService:
    """Get PVZ service instance."""
    return PVZService(redis_client=redis_client, phone=phone)


pvz_service_dependency = Depends(get_pvz_service)