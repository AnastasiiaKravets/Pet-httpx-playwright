import pytest

from src.api.restfull_booker_service.clients.room_client import RoomClient
from src.helpers.date_helper import get_date_today, get_future_date


@pytest.fixture(scope='function')
def available_room(authorized_api_client):
    date_from = get_date_today()
    date_to = get_future_date(2)
    rooms = RoomClient(authorized_api_client).available_rooms(date_from, date_to)
    if len(rooms) == 0:
        raise Exception("No rooms to check")
    return dict(room_id=rooms[0].room_id, date_from=date_from, date_to=date_to)
