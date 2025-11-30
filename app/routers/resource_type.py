from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models import ResourceType
from app.schemas.resource_type import ResourceTypeCreate, ResourceTypeRead

router = APIRouter(prefix="/resource-types", tags=["Resource Types"])


@router.post(
    "/", response_model=ResourceTypeRead, status_code=status.HTTP_201_CREATED
)
async def create_resource_type(
    type_data: ResourceTypeCreate, session: AsyncSession = Depends(get_db)
):
    result = await session.execute(
        select(ResourceType).where(ResourceType.name == type_data.name)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Resource type already exists")

    new_type = ResourceType(name=type_data.name)

    session.add(new_type)
    await session.commit()
    await session.refresh(new_type)

    return new_type


@router.get("/", response_model=list[ResourceTypeRead])
async def get_resource_types(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(ResourceType))
    types = result.scalars().all()
    return types
