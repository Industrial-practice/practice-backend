from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrgUnitBase(BaseModel):
    organization_id: int
    parent_id: Optional[int] = None
    name: str
    code: Optional[str] = None
    manager_employee_id: Optional[int] = None


class OrgUnitCreate(OrgUnitBase):
    pass


class OrgUnitUpdate(BaseModel):
    organization_id: Optional[int] = None
    parent_id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    manager_employee_id: Optional[int] = None


class OrgUnitRead(OrgUnitBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True