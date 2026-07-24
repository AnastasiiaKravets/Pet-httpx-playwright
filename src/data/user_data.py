from faker import Faker

from config import settings
from src.api.models.booking_models import BookingDates, BookingModelRequest


def get_valid_user():
    return {'username': settings.RESTFULL_USER, 'password': settings.RESTFULL_PASSWORD}


def get_user_reservation_data():
    faker = Faker()
    return dict(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
        phone=faker.country_calling_code() + faker.basic_phone_number(),
    )


def get_booking_payload(room_id, date_from, date_to):
    dates = BookingDates(checkin=date_from, checkout=date_to)
    user_data = get_user_reservation_data()
    return BookingModelRequest(
        room_id=room_id,
        deposit_paid=False,
        booking_dates=dates,
        **user_data
    )
