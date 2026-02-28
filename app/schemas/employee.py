from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class EmployeeBase(BaseModel):
    organization_id: int
    org_unit_id: Optional[int] = None
    employee_number: str

    first_name: str
    last_name: str
    middle_name: Optional[str] = None

    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    position: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    organization_id: Optional[int] = None
    org_unit_id: Optional[int] = None
    employee_number: Optional[str] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None

    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    position: Optional[str] = None

    is_active: Optional[bool] = None


class EmployeeRead(EmployeeBase):
    id: int
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True