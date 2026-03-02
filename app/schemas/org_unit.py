from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class OrgUnitBase(BaseModel):
    organization_id: int
    parent_id: Optional[int] = None

    name: str = Field(..., max_length=255)
    code: Optional[str] = Field(None, max_length=50)

    manager_employee_id: Optional[int] = None


class OrgUnitCreate(OrgUnitBase):
    pass


class OrgUnitUpdate(BaseModel):
    organization_id: Optional[int] = None
    parent_id: Optional[int] = None

    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=50)

    manager_employee_id: Optional[int] = None


class OrgUnitRead(BaseModel):
    id: int

    organization_id: int
    parent_id: Optional[int]

    name: str
    code: Optional[str]

    manager_employee_id: Optional[int]

    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True