from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Location, Resource, ResourceType, Tag
from app.schemas.resource import ResourceCreate, ResourceRead

router = APIRouter(prefix="/resources", tags=["Resources"])

@router.get("/", response_model=list[ResourceRead])
async def get_resources(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Resource))
    resources = result.scalars().all()
    return resources

@router.post("/", response_model=ResourceRead)
async def create_resource(data: ResourceCreate, db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(select(Location).where(Location.id == data.location_id))
    location = result.scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=400, detail="Location does not exist")

    result = await db.execute(
        select(ResourceType).where(ResourceType.id == data.type_id)
    )
    resource_type = result.scalar_one_or_none()
    if not resource_type:
        raise HTTPException(status_code=400, detail="Resource type does not exist")

    resource = Resource(
        name=data.name,
        location_id=data.location_id,
        type_id=data.type_id,
    )

    if data.tag_ids:
        result = await db.execute(
            select(Tag)
            .options(selectinload(Resource.tags))
            .where(Tag.id.in_(data.tag_ids))
        )
        tags = result.scalars().all()

        if len(tags) != len(data.tag_ids):
            raise HTTPException(status_code=400, detail="Some tag_ids do not exist")

        resource.tags = tags

    db.add(resource)
    await db.commit()
    await db.refresh(resource)

    result = await db.execute(
        select(Resource)
        .options(
            selectinload(Resource.tags),
            selectinload(Resource.location),
            selectinload(Resource.type),
        )
        .where(Resource.id == resource.id)
    )
    resource = result.scalar_one()

    return resource