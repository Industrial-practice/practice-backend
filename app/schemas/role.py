from pydantic import BaseModel
from typing import Optional


class RoleBase(BaseModel):
    code: str
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None


class RoleRead(RoleBase):
    id: int

    class Config:
        from_attributes = True