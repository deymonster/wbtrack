from datetime import date
from models.office_report import OfficeReportBase

class IOfficeReportRead(OfficeReportBase):
    id: int
    office_id: int

class IOfficeReportCreate(OfficeReportBase):
    office_id: int

class IOfficeReportUpdate(OfficeReportBase):
    pass