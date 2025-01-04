from pydantic import BaseModel, Field


class PhoneRequest(BaseModel):
    phone: str = Field(..., description="Номер телефона")

class ValidateCodeRequest(BaseModel):
    phone: str = Field(..., description="Номер телефона")
    code: str = Field(..., description="Код подтверждения")