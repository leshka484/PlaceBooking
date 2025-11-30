from datetime import date, datetime, time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Booking, Resource, User
from app.schemas.booking import BookingCreate, BookingRead

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("/", response_model=list[BookingRead])
async def get_bookings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Booking))
    return result.scalars().all()

@router.post("/", response_model=BookingRead)
async def create_booking(data: BookingCreate, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, data.user_id)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    resource = await db.get(Resource, data.resource_id)
    if not resource:
        raise HTTPException(status_code=400, detail="Resource does not exist")

    if data.start_time >= data.end_time:
        raise HTTPException(status_code=400, detail="Invalid time range")
    
    if data.start_time.date() < date.today():
        raise HTTPException(status_code=400, detail="You cannot book in past")

    overlap_query = select(Booking).where(
        and_(
            Booking.resource_id == data.resource_id,
            Booking.start_time < data.end_time,
            Booking.end_time > data.start_time,
        )
    )

    result = await db.execute(overlap_query)
    overlap = result.scalar_one_or_none()

    if overlap:
        raise HTTPException(
            status_code=400, detail="Resource is already booked in this time range"
        )

    booking = Booking(
        user_id=data.user_id,
        resource_id=data.resource_id,
        start_time=data.start_time,
        end_time=data.end_time,
    )

    db.add(booking)
    await db.commit()
    await db.refresh(booking)

    return booking