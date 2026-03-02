from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class EmployeeBase(BaseModel):
    organization_id: int
    org_unit_id: Optional[int] = None

    employee_number: str = Field(..., max_length=50)

    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)

    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)

    position: Optional[str] = Field(None, max_length=255)
    grade: Optional[str] = Field(None, max_length=100)


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    organization_id: Optional[int] = None
    org_unit_id: Optional[int] = None

    employee_number: Optional[str] = Field(None, max_length=50)

    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)

    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)

    position: Optional[str] = Field(None, max_length=255)
    grade: Optional[str] = Field(None, max_length=100)

    is_active: Optional[bool] = None


class EmployeeRead(BaseModel):
    id: int

    organization_id: int
    org_unit_id: Optional[int]

    employee_number: str

    first_name: str
    last_name: str
    middle_name: Optional[str]

    email: Optional[EmailStr]
    phone: Optional[str]

    position: Optional[str]
    grade: Optional[str]

    is_active: bool

    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True