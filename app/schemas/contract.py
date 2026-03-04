from pydantic import BaseModel, Field, field_validator, model_validator
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

    @field_validator("contract_number")
    @classmethod
    def contract_number_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Contract number cannot be empty")
        return v.strip()

    @field_validator("budget_limit")
    @classmethod
    def budget_positive(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("Budget limit cannot be negative")
        return v

    @model_validator(mode="after")
    def end_after_start(self) -> "ContractBase":
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValueError("end_date must be after start_date")
        return self


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

    @field_validator("budget_limit")
    @classmethod
    def budget_positive(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        if v is not None and v < 0:
            raise ValueError("Budget limit cannot be negative")
        return v

    @model_validator(mode="after")
    def end_after_start(self) -> "ContractUpdate":
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValueError("end_date must be after start_date")
        return self


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