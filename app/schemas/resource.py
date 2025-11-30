from pydantic import BaseModel

from app.schemas.locations import LocationRead
from app.schemas.resource_type import ResourceTypeRead
from app.schemas.tag import TagRead


class ResourceBase(BaseModel):
    name: str
    location_id: int
    type_id: int


class ResourceCreate(ResourceBase):
    tag_ids: list[int] | None = None


class ResourceRead(ResourceBase):
    id: int
    location: LocationRead
    type: ResourceTypeRead
    tags: list[TagRead] = []

    model_config = {"from_attributes": True}
