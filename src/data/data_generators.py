import random

from faker import Faker

from config import settings
from src.api.models.booking_models import BookingDates, BookingModelRequest
from src.api.models.room_models import Room, RoomFeatures, RoomType


def get_valid_user() -> dict[str, str]:
    return {"username": settings.RESTFULL_USER, "password": settings.RESTFULL_PASSWORD}


def get_user_reservation_data() -> dict[str, str]:
    faker = Faker()
    return dict(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
        phone=faker.country_calling_code() + faker.basic_phone_number(),
    )


def get_booking_payload(room_id: int, date_from: str, date_to: str) -> BookingModelRequest:
    dates = BookingDates(checkin=date_from, checkout=date_to)
    user_data = get_user_reservation_data()
    return BookingModelRequest(room_id=room_id, deposit_paid=False, booking_dates=dates, **user_data)


def get_room_payload():
    faker = Faker()
    return Room(
        room_name=f"Room {random.randint(1, 100)}",
        type=random.choice([item.value for item in RoomType]),
        accessible=random.choice([True, False]),
        room_price=random.randint(10, 999),
        image=faker.image_url(),
        description=faker.sentence(),
        features=random.choices([item.value for item in RoomFeatures], k=3),
    )
