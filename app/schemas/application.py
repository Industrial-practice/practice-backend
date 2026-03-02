from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ApplicationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    cancelled = "cancelled"


class ApplicationBase(BaseModel):
    requested_by_user_id: Optional[int] = None
    organization_id: int
    org_unit_id: Optional[int] = None
    contract_id: Optional[int] = None
    course_id: int
    comment: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    requested_by_user_id: Optional[int] = None
    organization_id: Optional[int] = None
    org_unit_id: Optional[int] = None
    contract_id: Optional[int] = None
    course_id: Optional[int] = None
    status: Optional[ApplicationStatus] = None
    comment: Optional[str] = None


class ApplicationRead(BaseModel):
    id: int

    requested_by_user_id: Optional[int]
    organization_id: int
    org_unit_id: Optional[int]
    contract_id: Optional[int]
    course_id: int

    status: ApplicationStatus
    comment: Optional[str]

    submitted_at: Optional[datetime]
    approved_at: Optional[datetime]
    rejected_at: Optional[datetime]


    class Config:
        from_attributes = True