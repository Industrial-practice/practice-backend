from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime
from enum import Enum
from decimal import Decimal


class SessionStatus(str, Enum):
    planned = "planned"
    ongoing = "ongoing"
    completed = "completed"
    cancelled = "cancelled"


class SessionType(str, Enum):
    seminar = "seminar"
    training = "training"
    certification = "certification"


class PricingType(str, Enum):
    per_person = "per_person"
    per_group = "per_group"


class TrainingSessionBase(BaseModel):
    course_id: int
    trainer_id: Optional[int] = None
    session_type: SessionType
    start_datetime: datetime
    end_datetime: datetime
    city: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=500)
    pricing_type: PricingType
    price_amount: Decimal
    currency: str = Field(..., max_length=10)

    @field_validator("price_amount")
    @classmethod
    def price_positive(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("Price amount cannot be negative")
        return v

    @model_validator(mode="after")
    def end_after_start(self) -> "TrainingSessionBase":
        if self.start_datetime and self.end_datetime:
            if self.end_datetime <= self.start_datetime:
                raise ValueError("end_datetime must be after start_datetime")
        return self


class TrainingSessionCreate(TrainingSessionBase):
    pass


class TrainingSessionUpdate(BaseModel):
    course_id: Optional[int] = None
    trainer_id: Optional[int] = None
    session_type: Optional[SessionType] = None 
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    city: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=500)
    pricing_type: Optional[PricingType] = None
    price_amount: Optional[Decimal] = None
    currency: Optional[str] = Field(None, max_length=10)
    status: Optional[SessionStatus] = None
    is_active: Optional[bool] = None

    @field_validator("price_amount")
    @classmethod
    def price_positive(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        if v is not None and v < 0:
            raise ValueError("Price amount cannot be negative")
        return v

    @model_validator(mode="after")
    def end_after_start(self) -> "TrainingSessionUpdate":
        if self.start_datetime and self.end_datetime:
            if self.end_datetime <= self.start_datetime:
                raise ValueError("end_datetime must be after start_datetime")
        return self


class TrainingSessionRead(BaseModel):
    id: int

    course_id: int
    trainer_id: Optional[int]

    session_type: SessionType

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