from typing import Any, Optional

from sqlalchemy import CompoundSelect, Subquery, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from fastapi_pagination.api import apply_items_transformer, create_page
from fastapi_pagination.bases import AbstractParams
from fastapi_pagination.types import AdditionalData, AsyncItemsTransformer
from fastapi_pagination.utils import verify_params


async def paginate(
    session: AsyncSession,
    query: Select,
    params: Optional[AbstractParams] = None,
    *,
    transformer: Optional[AsyncItemsTransformer] = None,
    additional_data: Optional[AdditionalData] = None,
    scalars: bool = True,
) -> Any:
    """Paginate query results.

    :param session: AsyncSession instance.
    :param query: Query to paginate.
    :param params: Query parameters.
    :param transformer Optional function to transform items.
    :param additional_data: Additional data to pass to the transformer.
    :param scalars: Flag to return scalars instead of lists.
    :return: Paginated results.
    """
    params, raw_params = verify_params(params, "limit-offset")

    total_query = select(func.count()).select_from(query.froms[0])
    if query.whereclause is not None:
        total_query = total_query.where(query.whereclause)

    total = await session.scalar(total_query)
    query = query.offset(raw_params.offset).limit(raw_params.limit)

    if not scalars:
        items = (await session.execute(query)).all()
    else:
        items = (await session.execute(query)).scalars().all()

    transformed_items = await apply_items_transformer(items, transformer, async_=True)

    next = None
    if (
        raw_params.offset is not None
        and raw_params.limit is not None
        and total is not None
    ):
        next_offset = raw_params.offset + raw_params.limit
        if next_offset < total:
            next = dict(
                offset=next_offset,
                limit=raw_params.limit,
            )

    return create_page(
        transformed_items,
        params=params,
        **dict(
            next=next,
            total=total,
            additional_data=additional_data or {},
        ),
    )
