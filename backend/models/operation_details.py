# from sqlmodel import Field, SQLModel, Relationship, Column, ForeignKey, Integer, String, Float, Boolean, DateTime
# from typing import Optional
# from datetime import datetime
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from models.operation import Operation
    

# class OperationDetailsBase(SQLModel):
#     rid: int = Field(index=True)
#     model: int
#     vendor: int
#     payment_type: str
#     scanned_code: str
#     sell_summ: float
#     price: float
#     balance: float
#     buyer_id: int
#     with_discount: bool
#     created: datetime
#     currency: str
#     info: str

# class OperationDetails(OperationDetailsBase, BaseTableID, table=True):
#     operation_id: int = Field (
#         sa_column=Column(
#             Integer,
#             ForeignKey("operation.id", ondelete="CASCADE"),
#             nullable=False,
#             unique=True
#         )
#     )
#     operation: "Operation" = Relationship(back_populates="details")