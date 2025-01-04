from pydantic import BaseModel


class IEmployeeOfficeLinkBase(BaseModel):
    employee_id: int
    office_id: int



class IEmployeeOfficeLinkCreate(IEmployeeOfficeLinkBase):
    pass


class IEmployeeOfficeLinkRead(IEmployeeOfficeLinkBase):
    pass
