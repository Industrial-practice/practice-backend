from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from decimal import Decimal


class SessionStatus(str, Enum):
    planned = "planned"
    ongoing = "ongoing"
    completed = "completed"
    cancelled = "cancelled"


class PricingType(str, Enum):
    per_person = "per_person"
    per_group = "per_group"


class TrainingSessionBase(BaseModel):
    course_id: int
    trainer_id: Optional[int] = None

    start_datetime: datetime
    end_datetime: datetime

    city: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=500)

    pricing_type: PricingType
    price_amount: Decimal
    currency: str = Field(..., max_length=10)


class TrainingSessionCreate(TrainingSessionBase):
    pass


class TrainingSessionUpdate(BaseModel):
    course_id: Optional[int] = None
    trainer_id: Optional[int] = None

    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None

    city: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=500)

    pricing_type: Optional[PricingType] = None
    price_amount: Optional[Decimal] = None
    currency: Optional[str] = Field(None, max_length=10)

    status: Optional[SessionStatus] = None
    is_active: Optional[bool] = None


class TrainingSessionRead(BaseModel):
    id: int

    course_id: int
    trainer_id: Optional[int]

    start_datetime: datetime
    end_datetime: datetime

    city: Optional[str]
    location: Optional[str]

    pricing_type: PricingType
    price_amount: Decimal
    currency: str

    status: SessionStatus
    is_active: bool

    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True