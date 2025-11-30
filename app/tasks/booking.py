from datetime import datetime, timezone

from sqlalchemy import select

from app.core.celery_app import celery_app
from app.database import SessionLocal
from app.models import Booking, BookingStatus


@celery_app.task
def update_statuses():
    now = datetime.now(timezone.utc)

    with SessionLocal() as db:  # синхронная сессия
        # upcoming → active
        change_to_active = select(Booking).where(
            Booking.status == BookingStatus.upcoming, Booking.start_time <= now
        )
        just_started = db.execute(change_to_active).scalars().all()
        for booking in just_started:
            booking.status = BookingStatus.active

        # active → ended
        change_to_ended = select(Booking).where(
            Booking.status == BookingStatus.active, Booking.end_time <= now
        )
        just_ended = db.execute(change_to_ended).scalars().all()
        for booking in just_ended:
            booking.status = BookingStatus.ended

        db.commit()