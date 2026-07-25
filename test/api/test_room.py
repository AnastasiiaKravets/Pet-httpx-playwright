import pytest

from src.api.models.booking_models import BookingListModelResponse
from src.api.models.common_models import ExtendedErrorResponse
from src.api.models.room_models import RoomResponse, RoomList
from src.helpers.date_helper import get_future_date, get_past_date, get_date_today


@pytest.mark.api
def test_get_all_rooms_info(api_client):
    response = api_client.get("/room")

    assert response.status_code == 200
    RoomList.model_validate(response.json())


@pytest.mark.api
def test_get_rooms_availability(api_client):
    params = dict(check_in=get_future_date(100),  # just to be sure there is no booking
                  check_out=get_future_date(101))
    response = api_client.get("/room", params=params)

    assert response.status_code == 200
    RoomList.model_validate(response.json())


@pytest.mark.api
@pytest.mark.parametrize("check_in, check_out", [
    (get_future_date(10), get_future_date(7)),
    (get_past_date(10), get_past_date(7)),
    (get_date_today(), get_date_today())
])
def test_room_availability_invalid_business_data_rules(api_client, check_in, check_out):
    params = dict(check_in=check_in,
                  check_out=check_out)
    response = api_client.get("/room", params=params)

    assert response.status_code == 400
    assert response.json() == []


@pytest.mark.api
@pytest.mark.parametrize("check_in, check_out", [
    ('asdasd', 'asdasd'),
    ('01.01.2027', '64-01-2026'),
    ('', '')
])
def test_room_availability_invalid_data_format(api_client, check_in, check_out):
    params = dict(check_in=check_in,
                  check_out=check_out)
    response = api_client.get("/room", params=params)

    assert response.status_code == 500
    assert response.json() == []


@pytest.mark.api
@pytest.mark.workflow
@pytest.mark.parametrize("check_in, check_out, should_be_available", [
    (get_future_date(30), get_future_date(32), False),  # exact matching
    (get_future_date(30), get_future_date(31), False),  # full matching inside
    (get_future_date(31), get_future_date(32), False),  # full matching inside
    (get_future_date(28), get_future_date(31), False),  # partial matching at the beginning
    (get_future_date(31), get_future_date(34), False),  # partial matching at the ending
    (get_future_date(28), get_future_date(30), True),  # date before
    (get_future_date(32), get_future_date(34), True)  # date after
])
def test_room_availability_with_existing_booking(api_client, booking_data, check_in, check_out, should_be_available):
    room_id = booking_data.room_id
    params = dict(check_in=check_in,
                  check_out=check_out)

    response = api_client.get("/room", params=params)

    assert response.status_code == 200
    rooms_response = RoomList.model_validate(response.json())
    is_available = room_id in [room.room_id for room in rooms_response.rooms]

    assert is_available == should_be_available, f"Room should be available ({should_be_available})"


@pytest.mark.api
def test_get_room_by_id(api_client, random_existing_room_id):
    response = api_client.get(f"/room/{random_existing_room_id}")
    assert response.status_code == 200
    room = RoomResponse.model_validate(response.json())
    assert room.room_id == random_existing_room_id


@pytest.mark.api
def test_get_room_by_invalid_id(api_client):
    room_id = 9999
    response = api_client.get(f"/room/{room_id}")
    assert response.status_code == 404
    ExtendedErrorResponse.model_validate(response.json())


@pytest.mark.api
def test_delete_room_by_id(authorized_api_client, random_existing_room_id):
    response = authorized_api_client.delete(f"/room/{random_existing_room_id}")
    assert response.status_code == 202

    response = authorized_api_client.get(f"/room/{random_existing_room_id}")
    assert response.status_code == 500


@pytest.mark.api
@pytest.mark.workflow
def test_delete_room_with_booking(authorized_api_client, booking_data):
    room_id = booking_data.room_id

    response = authorized_api_client.get("/booking", params={'roomid': room_id})
    existed_booking = BookingListModelResponse.model_validate(response.json()).bookings

    response = authorized_api_client.delete(f"/room/{room_id}")
    assert response.status_code == 202

    for booking in existed_booking:
        response = authorized_api_client.get(f"/booking/{booking.booking_id}")
        assert response.status_code == 404
