from typing import Any, Dict, Literal, Protocol, Self, Type, Union, runtime_checkable
from uuid import UUID

from sqlalchemy import Table
from sqlmodel import SQLModel
from sqlmodel.main import FieldInfo, IncEx


@runtime_checkable
class IModelBase(Protocol):
    id: Any
    __table__: Table
    model_fields: Dict[str, FieldInfo]

    @classmethod
    def model_validate(
        cls: Any,
        obj: Any,
        *,
        strict: Union[bool, None] = None,
        from_attributes: Union[bool, None] = None,
        context: Union[Dict[str, Any], None] = None,
        update: Union[Dict[str, Any], None] = None,
    ) -> Any: ...

    def model_dump(
        self,
        *,
        mode: Union[Literal["json", "python"], str] = "python",
        include: IncEx = None,
        exclude: IncEx = None,
        context: Union[Dict[str, Any], None] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
        serialize_as_any: bool = False,
    ) -> Dict[str, Any]: ...


@runtime_checkable
class IModel(IModelBase, Protocol):

    def model_update(
        self,
        **update_data: Any,
    ) -> Self: ...


@runtime_checkable
class IModelUpdate(IModelBase, Protocol):
    id: Any
