from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models import Location
from app.schemas.locations import LocationCreate, LocationRead

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.post(
    "/", response_model=LocationRead, status_code=status.HTTP_201_CREATED
)
async def create_location(
    location_data: LocationCreate, session: AsyncSession = Depends(get_db)
):
    # Проверяем, нет ли уже локации с таким именем
    result = await session.execute(
        select(Location).where(Location.name == location_data.name)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Location already exists")

    new_location = Location(name=location_data.name, address=location_data.address)

    session.add(new_location)
    await session.commit()
    await session.refresh(new_location)

    return new_location


@router.get("/", response_model=list[LocationRead])
async def get_locations(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Location))
    locations = result.scalars().all()
    return locations
