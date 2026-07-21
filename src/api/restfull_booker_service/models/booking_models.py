from datetime import date

from pydantic import Field, EmailStr, PositiveInt

from src.api.restfull_booker_service.models.common_models import StrictModel


class BookingDates(StrictModel):
    checkin: date
    checkout: date


class BookingModel(StrictModel):
    room_id: PositiveInt = Field(..., alias="roomid")
    first_name: str = Field(..., alias="firstname", min_length=3, max_length=18)
    last_name: str = Field(..., alias="lastname", min_length=3, max_length=30)
    deposit_paid: bool = Field(..., alias="depositpaid")
    booking_dates: BookingDates = Field(..., alias="bookingdates")
    email: EmailStr
    phone: str = Field(..., min_length=11, max_length=21)
