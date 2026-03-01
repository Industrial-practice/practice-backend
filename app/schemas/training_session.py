from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class TrainingSessionStatus(str, Enum):
    planned = "planned"
    ongoing = "ongoing"
    finished = "finished"
    cancelled = "cancelled"


class TrainingSessionBase(BaseModel):
    course_id: int
    start_datetime: datetime
    end_datetime: datetime
    city: Optional[str] = None
    location: Optional[str] = None
    price_amount: Optional[float] = None
    currency: Optional[str] = None


class TrainingSessionCreate(TrainingSessionBase):
    pass


class TrainingSessionUpdate(BaseModel):
    course_id: Optional[int] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    city: Optional[str] = None
    location: Optional[str] = None
    price_amount: Optional[float] = None
    currency: Optional[str] = None
    status: Optional[TrainingSessionStatus] = None


class TrainingSessionRead(TrainingSessionBase):
    id: int
    status: TrainingSessionStatus

    class Config:
        from_attributes = True