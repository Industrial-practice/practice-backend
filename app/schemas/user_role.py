from pydantic import BaseModel


class UserRoleBase(BaseModel):
    user_id: int
    role_id: int


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleRead(UserRoleBase):
    class Config:
        from_attributes = True