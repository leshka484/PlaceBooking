from pydantic import BaseModel

from .roles import RoleRead


class UserBase(BaseModel):
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str
    role_id: int

class UserRead(UserBase):
    id: int
    role: RoleRead | None = None
    
    model_config = {"from_attributes": True}