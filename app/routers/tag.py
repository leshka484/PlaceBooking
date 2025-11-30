from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import ResourceType, Tag
from app.schemas.tag import TagCreate, TagRead

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("/", response_model=list[TagRead])
async def get_tags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).options(
        selectinload(Tag.resources)))
    tags = result.scalars().all()

    return [
        TagRead(
            id=tag.id,
            name=tag.name,
            resource_type_id=tag.resource_type_id,
            resource_ids=[resources.id for resources in tag.resources],
        )
        for tag in tags
    ]

@router.post("/", response_model=TagRead)
async def create_tag(data: TagCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ResourceType).where(ResourceType.id == data.resource_type_id)
    )
    resource_type = result.scalar_one_or_none()

    if resource_type is None:
        raise HTTPException(status_code=400, detail="Resource type does not exist")

    tag = Tag(name=data.name, resource_type_id=data.resource_type_id)

    db.add(tag)
    await db.commit()
    await db.refresh(tag)

    result = await db.execute(select(Tag).where(Tag.id == tag.id).options(
        selectinload(Tag.resources))
    )
    tag = result.scalar_one()

    return TagRead(
        id=tag.id,
        name=tag.name,
        resource_type_id=tag.resource_type_id,
        resource_ids=[resource.id for resource in tag.resources],
    )