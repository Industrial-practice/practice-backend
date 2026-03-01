from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class ApplicationItemBase(BaseModel):
    application_id: int
    employee_id: int
    session_id: Optional[int] = None
    price_amount: Decimal
    currency: str


class ApplicationItemCreate(ApplicationItemBase):
    pass


class ApplicationItemUpdate(BaseModel):
    application_id: Optional[int] = None
    employee_id: Optional[int] = None
    session_id: Optional[int] = None
    price_amount: Optional[Decimal] = None
    currency: Optional[str] = None
    status: Optional[str] = None


class ApplicationItemRead(ApplicationItemBase):
    id: int
    status: str

    class Config:
        from_attributes = True