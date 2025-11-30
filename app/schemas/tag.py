from pydantic import BaseModel


class TagBase(BaseModel):
    name: str
    resource_type_id: int

class TagCreate(TagBase):
    pass

class TagRead(TagBase):
    id: int
    resource_ids: list[int] = []

    model_config = {"from_attributes": True}