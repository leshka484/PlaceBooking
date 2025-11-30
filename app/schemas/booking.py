from datetime import datetime

from pydantic import BaseModel


class BookingBase(BaseModel):
    user_id: int
    resource_id: int
    start_time: datetime
    end_time: datetime


class BookingCreate(BookingBase):
    pass

class BookingRead(BookingBase):
    id: int
    status: str
    created_at: datetime
    
    model_config = {"from_attributes": True}