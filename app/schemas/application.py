from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ApplicationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ApplicationBase(BaseModel):
    requested_by_user_id: int
    organization_id: int
    org_unit_id: Optional[int] = None
    course_id: Optional[int] = None
    comment: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    requested_by_user_id: Optional[int] = None
    organization_id: Optional[int] = None
    org_unit_id: Optional[int] = None
    course_id: Optional[int] = None
    status: Optional[ApplicationStatus] = None
    comment: Optional[str] = None


class ApplicationRead(ApplicationBase):
    id: int
    status: ApplicationStatus
    submitted_at: Optional[datetime]

    class Config:
        from_attributes = True