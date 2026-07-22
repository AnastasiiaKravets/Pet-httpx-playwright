from dataclasses import dataclass

import pytest

from src.api.restfull_booker_service.clients.booking_client import BookingClient


@dataclass
class BookingCleanup:
    room_id: int | None = None
    date_from: str | None = None
    date_to: str | None = None

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)


@pytest.fixture(scope="function")
def clear_booking_data(authorized_api_client):
    cleanup = BookingCleanup()

    yield cleanup

    if cleanup.room_id is None:
        return

    booking_client = BookingClient(authorized_api_client)
    bookings = booking_client.get_all_booking_for_room(cleanup.room_id)
    booking = next(
        (
            booking
            for booking in bookings
            if booking.booking_dates.checkin == cleanup.date_from
               and booking.booking_dates.checkout == cleanup.date_to
        ),
        None
    )
    if booking:
        booking_client.delete_booking(booking.booking_id)
