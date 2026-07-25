from typing import List

from pydantic import Field, EmailStr, PositiveInt

from src.api.models.common_models import StrictModel


class BookingDates(StrictModel):
    checkin: str
    checkout: str


class BookingModelRequest(StrictModel):
    room_id: PositiveInt = Field(..., alias="roomid")
    first_name: str = Field(..., alias="firstname", min_length=3, max_length=18)
    last_name: str = Field(..., alias="lastname", min_length=3, max_length=30)
    deposit_paid: bool = Field(..., alias="depositpaid")
    booking_dates: BookingDates = Field(..., alias="bookingdates")
    email: EmailStr | None = None
    phone: str | None = Field(None, min_length=11, max_length=21)


class BookingModelResponse(StrictModel):
    booking_id: PositiveInt = Field(..., alias="bookingid")
    room_id: PositiveInt = Field(..., alias="roomid")
    first_name: str = Field(..., alias="firstname", min_length=3, max_length=18)
    last_name: str = Field(..., alias="lastname", min_length=3, max_length=30)
    deposit_paid: bool = Field(..., alias="depositpaid")
    booking_dates: BookingDates = Field(..., alias="bookingdates")


class BookingListModelResponse(StrictModel):
    bookings: List[BookingModelResponse]


class BookingUpdateModelResponse(StrictModel):
    booking_id: PositiveInt = Field(..., alias="bookingid")
    booking: BookingModelResponse
