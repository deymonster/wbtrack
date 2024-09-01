from typing import TypeVar
from sqlalchemy.orm import QueryableAttribute


_T = TypeVar("_T")


def relations(relations_expression) -> QueryableAttribute:
    if not isinstance(relations_expression, (QueryableAttribute)):
        raise RuntimeError(f"Not a SQLAlchemy relations: {relations_expression}")
    return relations_expression
