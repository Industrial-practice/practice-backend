from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ContractStatus(str, Enum):
    draft = "draft"
    active = "active"
    closed = "closed"
    cancelled = "cancelled"


class ContractBase(BaseModel):
    provider_id: int
    contract_number: str
    title: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    currency: Optional[str] = None
    budget_limit: Optional[float] = None


class ContractCreate(ContractBase):
    pass


class ContractUpdate(BaseModel):
    provider_id: Optional[int] = None
    contract_number: Optional[str] = None
    title: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    currency: Optional[str] = None
    budget_limit: Optional[float] = None
    status: Optional[ContractStatus] = None


class ContractRead(ContractBase):
    id: int
    status: ContractStatus
    created_at: Optional[datetime]

    class Config:
        from_attributes = True