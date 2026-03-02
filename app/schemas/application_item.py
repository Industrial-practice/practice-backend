from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime
from enum import Enum


class ApplicationItemStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ApplicationItemBase(BaseModel):
    application_id: int
    employee_id: int
    session_id: Optional[int] = None
    price_amount: Decimal
    currency: str = Field(..., max_length=10)


class ApplicationItemCreate(ApplicationItemBase):
    pass


class ApplicationItemUpdate(BaseModel):
    application_id: Optional[int] = None
    employee_id: Optional[int] = None
    session_id: Optional[int] = None
    price_amount: Optional[Decimal] = None
    currency: Optional[str] = Field(None, max_length=10)
    status: Optional[ApplicationItemStatus] = None


class ApplicationItemRead(BaseModel):
    id: int

    application_id: int
    employee_id: int
    session_id: Optional[int]

    price_amount: Decimal
    currency: str
    status: ApplicationItemStatus


    class Config:
        from_attributes = True