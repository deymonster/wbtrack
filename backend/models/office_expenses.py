from typing import TYPE_CHECKING, Optional

from sqlmodel import Column, Field, ForeignKey, Integer, Relationship, SQLModel

from models.base import BaseTableID

if TYPE_CHECKING:
    from models.office import Office


class OfficeExpensesBase(SQLModel):
    rent: float = Field(description="Аренда помещения филиала")
    utilities: float = Field(description="Коммунальные платежи за помещение филиала")
    internet: float = Field(description="Оплата интернета")
    cameras: float = Field(description="Оплата видеонаблюдения")
    vat_rate: float = Field(description="Ставка НДС")
    simplified_tax_rate: float = Field(description="Ставка УСН")
    rf_payment: float = Field(description="ЗП руководителя филиала")
    revision_payment: float = Field(description="Оплата сотрудника по ревизии")
    min_salary: float = Field(description="Минимальная ЗП на филиале")
    commission_rate: float = Field(description="Процент от оборота - влияет на ЗП сотрудника филиала")
    total_without_tax: float = Field(description="Сумма всех обязательных платежей за филиал без налогов")


class OfficeExpenses(OfficeExpensesBase, BaseTableID, table=True):
    office_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey("office.id", ondelete="CASCADE"),
            nullable=False,
            unique=True
        )
    )
    office: "Office" = Relationship(back_populates="expenses")
