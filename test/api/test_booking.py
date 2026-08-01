from dataclasses import asdict

import pytest

from src.api.models.booking_models import BookingModelResponse, BookingUpdateModelResponse
from src.api.models.common_models import ExtendedErrorResponse
from src.data.data_generators import get_booking_payload
from src.helpers.date_helper import get_date_with_offset


@pytest.mark.api
def test_create_valid_booking(authorized_api_client, available_room_in_future, clear_booking_data):
    payload = get_booking_payload(**available_room_in_future.dict())

    response = authorized_api_client.post('/booking', payload=payload)
    assert response.status_code == 201

    clear_booking_data.update(**available_room_in_future.dict())
    booking_data = BookingModelResponse.model_validate(response.json())
    assert booking_data.room_id == payload.room_id
    assert booking_data.booking_dates.checkin == payload.booking_dates.checkin
    assert booking_data.booking_dates.checkout == payload.booking_dates.checkout
    assert booking_data.first_name == payload.first_name
    assert booking_data.last_name == payload.last_name
    assert booking_data.deposit_paid == payload.deposit_paid

    clear_booking_data.booking_id = booking_data.booking_id

    response = authorized_api_client.get(f'/booking/{booking_data.booking_id}')
    assert response.status_code == 200
    get_booking_data = BookingModelResponse.model_validate(response.json())

    assert get_booking_data == booking_data


@pytest.mark.api
def test_update_booking(authorized_api_client, booking_data):
    booking_data.deposit_paid = True
    booking_data.booking_dates.checkin = get_date_with_offset(56)
    booking_data.booking_dates.checkout = get_date_with_offset(59)
    booking_data.first_name = booking_data.first_name + 'Updated'

    response = authorized_api_client.put(f'/booking/{booking_data.booking_id}', payload=booking_data)
    assert response.status_code == 200
    updated_booking_data = BookingUpdateModelResponse.model_validate(response.json()).booking

    assert updated_booking_data == booking_data

    response = authorized_api_client.get(f'/booking/{booking_data.booking_id}')
    assert response.status_code == 200
    get_booking_data = BookingModelResponse.model_validate(response.json())

    assert get_booking_data == updated_booking_data


@pytest.mark.api
def test_update_booking_with_invalid_data(authorized_api_client, booking_data):
    original_booking_data = booking_data.model_copy(deep=True)
    booking_data.deposit_paid = True
    booking_data.booking_dates.checkin = '123'
    booking_data.first_name = ''

    response = authorized_api_client.put(f'/booking/{booking_data.booking_id}', payload=booking_data)
    assert response.status_code == 400
    ExtendedErrorResponse.model_validate(response.json())

    response = authorized_api_client.get(f'/booking/{booking_data.booking_id}')
    assert response.status_code == 200
    get_booking_data = BookingModelResponse.model_validate(response.json())

    assert get_booking_data == original_booking_data
