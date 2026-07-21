import pytest

from src.api.restfull_booker_service.models.room_models import Room, RoomList


@pytest.mark.api
def test_get_all_rooms_info(api_client):
    response = api_client.get("/room")

    assert response.status_code == 200
    RoomList.model_validate(response.json())


def test_get_rooms_availability(api_client):
    response = api_client.get("/room?checkin=2026-07-16&checkout=2026-07-17")
    assert response.status_code == 200


def test_get_room_by_id(api_client):
    room_id = 1
    response = api_client.get(f"/room/{room_id}")
    assert response.status_code == 200
    Room.model_validate(response.json())


def test_get_room_by_invalid_id(api_client):
    room_id = 1
    # response = api_client.get(f"/room/{room_id}")
    # assert response.status_code == 200
    # Room.model_validate(response.json())


def test_get_room_availability_by_id(api_client):
    response = api_client.get("/report/room/1")
    assert response.status_code == 200
    # {"report": [{"end": "2026-02-05", "start": "2026-02-01", "title": "Unavailable"}]}


def test_delete_room_by_id(api_client):
    room_id = 1
    response = api_client.delete(f"/room/{room_id}")
    assert response.status_code == 202
    # verify all related booking was deleted
