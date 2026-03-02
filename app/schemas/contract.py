from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from decimal import Decimal


class ContractStatus(str, Enum):
    draft = "draft"
    active = "active"
    suspended = "suspended"
    closed = "closed"
    expired = "expired"


class ContractBase(BaseModel):
    provider_id: int
    contract_number: str = Field(..., max_length=100)
    title: Optional[str] = Field(None, max_length=255)

    start_date: datetime
    end_date: datetime

    currency: str = Field(..., max_length=10)
    budget_limit: Decimal


class ContractCreate(ContractBase):
    pass

class ContractUpdate(BaseModel):
    provider_id: Optional[int] = None
    contract_number: Optional[str] = Field(None, max_length=100)
    title: Optional[str] = Field(None, max_length=255)

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    currency: Optional[str] = Field(None, max_length=10)
    budget_limit: Optional[Decimal] = None

    status: Optional[ContractStatus] = None


class ContractRead(BaseModel):
    id: int

    provider_id: int
    contract_number: str
    title: Optional[str]

    start_date: datetime
    end_date: datetime

    currency: str
    budget_limit: Decimal

    status: ContractStatus
    created_by_user_id: Optional[int]

    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True