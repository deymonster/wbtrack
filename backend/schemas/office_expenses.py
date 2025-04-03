from models.office_expenses import OfficeExpensesBase

class IOfficeExpensesRead(OfficeExpensesBase):
    id: int
    office_id: int

class IOfficeExpensesCreate(OfficeExpensesBase):
    office_id: int

class IOfficeExpensesUpdate(OfficeExpensesBase):
    id: int