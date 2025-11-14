from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str

class RoleRead(RoleBase):
    id: int
    
    model_config = {"from_attributes": True}

class RoleCreate(RoleBase):
    pass