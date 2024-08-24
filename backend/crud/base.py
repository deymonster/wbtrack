from fastapi import HTTPException
from typing import Any, Generic, Sequence, Tuple, TypeVar, cast

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from core.utils.pagination import paginate
from enums.common import ListOrderEnum
from fastapi_async_sqlalchemy import db
from fastapi_pagination import LimitOffsetParams, Page
from sqlmodel import SQLModel, col, select, func
from sqlmodel.sql.expression import SelectOfScalar
from sqlalchemy import exc
from sqlalchemy.dialects._typing import _OnConflictIndexElementsT

from schemas.model import IModel, IModelUpdate

ModelType = TypeVar("ModelType", bound=IModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=IModelUpdate)
T = TypeVar("T", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLModel model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.db = db

    def get_db(self):
        return self.db

    async def get(
        self,
        *,
        id: int,
        db_session: AsyncSession | None = None,
    ) -> ModelType | None:
        """Get one object by id.

        :param id: The primary key of the model.
        :param db_session: The database session.
        :return: A single object or None
        """
        session: AsyncSession = db_session or self.db.session
        query = select(self.model).where(self.model.id == id)
        response = await session.execute(query)
        return response.scalar_one_or_none()

    async def get_by_ids(
        self,
        *,
        list_ids: list[int],
        query: SelectOfScalar[ModelType] | None = None,
        db_session: AsyncSession | None = None,
    ) -> Sequence[ModelType]:
        """Get multiple objects by ids.

        :param list_ids: List of ids.
        :param query Query object.
        :param db_session: The database session.
        :return: A list of objects or None
        """
        session: AsyncSession = db_session or self.db.session
        if query is None:
            query = select(self.model).where(col(self.model.id).in_(list_ids))
        else:
            query = query.where(col(self.model.id).in_(list_ids))
        response = await session.execute(query)
        return response.scalars().all()

    async def get_by_ids_ordered(
        self,
        *,
        list_ids: list[int],
        order_by: str | None = "id",
        order: ListOrderEnum = ListOrderEnum.descendent,
        query: SelectOfScalar[ModelType] | None = None,
        db_session: AsyncSession | None = None,
    ):
        """Get multiple ordered objects by ids."""
        session: AsyncSession = db_session or self.db.session

        columns = self.model.__table__.columns

        if query is None:
            query = select(self.model).where(col(self.model.id).in_(list_ids))
        else:
            query = query.where(col(self.model.id).in_(list_ids))

        if order_by is not None:
            if order == ListOrderEnum.ascendent:
                query = query.order_by(columns[order_by].asc())
            else:
                query = query.order_by(columns[order_by].desc())

        response = await session.execute(query)
        return response.scalars().all()

    async def get_count(
        self,
        db_session: AsyncSession | None = None,
    ) -> int | None:
        """Get the total count of objects."""
        session: AsyncSession = db_session or self.db.session
        response = await session.execute(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.scalar_one()

    async def get_multi(
        self,
        *,
        offset: int = 0,
        limit: int = 50,
        query: SelectOfScalar[ModelType] | None = None,
        db_session: AsyncSession | None = None,
    ) -> Sequence[ModelType]:
        """Get multiple objects with limit."""
        session: AsyncSession = db_session or self.db.session
        if query is None:
            query = (
                select(self.model)
                .offset(offset)
                .limit(limit)
                .order_by(col(self.model.id))
            )
        response = await session.execute(query)
        return response.scalars().all()

    async def get_multi_paginated(
        self,
        *,
        params: LimitOffsetParams | None = LimitOffsetParams(),
        query: SelectOfScalar[ModelType] | None = None,
        db_session: AsyncSession | None = None,
    ) -> Page[ModelType]:
        """Get multiple paginated objects."""
        session: AsyncSession = db_session or self.db.session
        if query is None:
            query = select(self.model)

        output = await paginate(session, query, params)
        return output

    async def get_multi_paginated_ordered(
        self,
        *,
        params: LimitOffsetParams | None = LimitOffsetParams(),
        order_by: str | None = "id",
        order: ListOrderEnum | None = ListOrderEnum.descendent,
        query: SelectOfScalar[ModelType] | None = None,
        db_session: AsyncSession | None = None,
    ) -> Page[ModelType]:
        """Get multiple paginated ordered objects."""
        session: AsyncSession = db_session or self.db.session

        columns = self.model.__table__.columns

        if query is None:
            query = select(self.model)

        if order_by is not None:
            if order == ListOrderEnum.ascendent:
                query = query.order_by(columns[order_by].asc())
            else:
                query = query.order_by(columns[order_by].desc())

        return await paginate(session, query, params)

    async def get_multi_ordered(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        order_by: str | None = None,
        order: ListOrderEnum | None = ListOrderEnum.ascendent,
        db_session: AsyncSession | None = None,
    ) -> Sequence[ModelType]:
        """Get multiple ordered objects."""
        session: AsyncSession = db_session or self.db.session

        columns = self.model.__table__.columns

        if order_by is None or order_by not in columns:
            order_by = "id"

        if order == ListOrderEnum.ascendent:
            query = (
                select(self.model)
                .offset(offset)
                .limit(limit)
                .order_by(columns[order_by].asc())
            )
        else:
            query = (
                select(self.model)
                .offset(offset)
                .limit(limit)
                .order_by(columns[order_by].desc())
            )

        response = await session.execute(query)
        return response.scalars().all()

    async def create(
        self,
        *,
        obj_in: CreateSchemaType | ModelType,
        additionals: dict[str, Any] | None = None,
        db_session: AsyncSession | None = None,
    ) -> ModelType:
        """Create an object."""
        session: AsyncSession = db_session or self.db.session
        db_obj = self.model.model_validate(
            obj_in.model_dump(exclude={"id"}),
            update=additionals,
        )

        try:
            session.add(db_obj)
            await session.commit()
        except exc.IntegrityError as e:
            await session.rollback()
            print(e)
            raise HTTPException(
                status_code=409,
                detail="Integrity error, create",
            )
        await session.refresh(db_obj)
        return db_obj

    async def create_or_update(
        self,
        *,
        obj_in: CreateSchemaType | ModelType,
        index_elements: _OnConflictIndexElementsT,
        create_exclude: set[str] | None = None,
        create_include: set[str] | None = None,
        update_exclude: set[str] | None = None,
        update_include: set[str] | None = None,
        db_session: AsyncSession | None = None,
    ) -> ModelType:
        """Create or update an object."""
        session: AsyncSession = db_session or self.db.session
        db_obj = self.model.model_validate(obj_in.model_dump(exclude={"id"}))

        insert_query = (
            insert(self.model)
            .values(
                db_obj.model_dump(
                    exclude=create_exclude,
                    include=create_include,
                )
            )
            .on_conflict_do_update(
                index_elements=index_elements,
                set_=obj_in.model_dump(
                    exclude=update_exclude,
                    include=update_include,
                ),
            )
            .returning(self.model)
        )

        try:
            response = await session.execute(insert_query)
            await session.commit()
        except exc.IntegrityError as e:
            await session.rollback()
            print(e)
            raise HTTPException(
                status_code=409,
                detail="Integrity error, create or update",
            )

        db_obj = response.scalar_one()
        return db_obj

    async def create_or_update_multi(
        self,
        *,
        list_in: Sequence[CreateSchemaType | ModelType],
        index_elements: _OnConflictIndexElementsT,
        exclude: set[str] | None = None,
        include: set[str] | None = None,
        on_conflict_set: set[str] = set(),
        additionals: dict[str, Any] | None = None,
        db_session: AsyncSession | None = None,
    ) -> None:
        """Create or update an object."""
        session: AsyncSession = db_session or self.db.session

        objs: list[ModelType] = []

        for obj_in in list_in:

            obj: ModelType = self.model.model_validate(
                obj_in.model_dump(
                    exclude=exclude,
                    include=include,
                ),
                update=additionals,
            )

            objs.append(obj.model_dump(exclude={"id"}))

        insert_query = insert(self.model).values(objs)

        insert_query = insert_query.on_conflict_do_update(
            index_elements=index_elements,
            set_={key: getattr(insert_query.excluded, key) for key in on_conflict_set},
        ).returning(self.model)

        try:
            await session.execute(insert_query)
            await session.commit()
        except exc.IntegrityError as e:
            await session.rollback()
            print(e)
            raise HTTPException(
                status_code=409,
                detail="Integrity error, create or update",
            )

    async def update(
        self,
        *,
        obj_current: ModelType,
        obj_new: UpdateSchemaType | dict[str, Any] | ModelType,
        db_session: AsyncSession | None = None,
    ) -> ModelType:
        """Update an object."""
        session: AsyncSession = db_session or self.db.session

        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.model_dump(
                exclude_unset=True
            )  # This tells Pydantic to not include the values that were not sent (default value)

        obj_current.model_update(**update_data)

        session.add(obj_current)
        await session.commit()
        await session.refresh(obj_current)
        return obj_current

    async def delete(
        self,
        *,
        id: int,
        db_session: AsyncSession | None = None,
    ) -> ModelType:
        """Delete an object."""
        session: AsyncSession = db_session or self.db.session
        query = select(self.model).where(self.model.id == id)
        response = await session.execute(query)
        obj = response.scalar_one()
        await session.delete(obj)
        await session.commit()
        return obj

    async def update_multi(
        self,
        *,
        list_in: list[UpdateSchemaType],
        db_session: AsyncSession | None = None,
    ) -> Sequence[ModelType]:
        """Update multiple objects."""
        session: AsyncSession = db_session or self.db.session

        objs = await self.get_by_ids(
            list_ids=[obj.id for obj in list_in],
        )

        objs_map = {obj.id: obj for obj in objs}

        for obj_in in list_in:
            obj = objs_map.get(obj_in.id)

            if not obj:
                continue

            update_data = obj_in.model_dump(exclude={"id"}, exclude_unset=True)

            obj.model_update(**update_data)

        session.add_all(objs)
        await session.commit()

        return objs

    async def create_multi(
        self,
        *,
        list_in: list[ModelType | CreateSchemaType],
        additionals: dict[str, Any] | None = None,
        db_session: AsyncSession | None = None,
    ) -> Sequence[ModelType]:
        """Create multiple objects."""
        session: AsyncSession = db_session or self.db.session

        objs: list[ModelType] = []

        for obj_in in list_in:

            obj = self.model.model_validate(
                obj_in.model_dump(
                    exclude={"id"},
                    by_alias=True,
                ),
                update=additionals,
            )

            objs.append(obj)

        session.add_all(objs)
        await session.commit()

        return objs

    async def delete_multi(
        self,
        *,
        list_ids: list[int],
        db_session: AsyncSession | None = None,
    ) -> Sequence[ModelType]:
        """Delete multiple objects."""
        session: AsyncSession = db_session or self.db.session

        objs = await self.get_by_ids(
            list_ids=list_ids,
        )

        for obj in objs:
            await session.delete(obj)

        await session.commit()

        return objs
