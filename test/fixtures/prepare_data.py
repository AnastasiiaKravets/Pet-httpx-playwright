import random

import pytest

from src.api.clients.booking_client import BookingClient
from src.api.clients.room_client import RoomClient
from src.api.models.booking_models import BookingModelResponse
from src.helpers.date_helper import get_future_date


@pytest.fixture(scope='function')
def available_room_in_future(authorized_api_client):
    date_from = get_future_date(30)
    date_to = get_future_date(32)
    room_client = RoomClient(authorized_api_client)
    rooms = room_client.available_rooms(date_from, date_to)
    if len(rooms) == 0:
        room_client.create_room()
    rooms = room_client.available_rooms(date_from, date_to)
    return dict(room_id=rooms[0].room_id, date_from=date_from, date_to=date_to)


@pytest.fixture(scope='function')
def booking_data(api_client, available_room_in_future, clear_booking_data) -> BookingModelResponse:
    booking_data = BookingClient(api_client).create_booking(**available_room_in_future)
    clear_booking_data.booking_id = booking_data.booking_id
    return booking_data


@pytest.fixture(scope='function')
def random_existing_room_id(authorized_api_client):
    rooms = RoomClient(authorized_api_client).get_all_rooms()
    return random.choice([room.room_id for room in rooms])
