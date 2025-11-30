from pydantic import BaseModel


class ResourceTypeBase(BaseModel):
    name: str

class ResourceTypeCreate(ResourceTypeBase):
    pass

class ResourceTypeRead(ResourceTypeBase):
    id: int

    model_config = {"from_attributes": True}
