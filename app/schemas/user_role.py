from pydantic import BaseModel

from app.schemas.role import RoleRead


class UserRoleBase(BaseModel):
    user_id: int
    role_id: int


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleRead(BaseModel):
    role: RoleRead

    class Config:
        from_attributes = True