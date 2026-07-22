from faker import Faker

from config import settings


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
