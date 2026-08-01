from collections.abc import Generator
from dataclasses import dataclass

import pytest

from src.api.clients.booking_client import BookingClient
from src.helpers.logger import logger


@dataclass
class BookingCleanupData:
    booking_id: int | None = None
    room_id: int | None = None
    date_from: str | None = None
    date_to: str | None = None

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)


@pytest.fixture(scope="function")
def clear_booking_data(authorized_api_client) -> Generator[BookingCleanupData, None, None]:
    cleanup = BookingCleanupData()

    yield cleanup

    logger.info(f"STARTED FIXTURE booking cleanup: {cleanup}")

    booking_client = BookingClient(authorized_api_client)
    if cleanup.booking_id:
        booking_client.delete_booking(cleanup.booking_id)
        return

    if cleanup.room_id:
        bookings = booking_client.get_all_booking_for_room(cleanup.room_id)
        booking = next(
            (
                booking
                for booking in bookings
                if booking.booking_dates.checkin == cleanup.date_from
                and booking.booking_dates.checkout == cleanup.date_to
            ),
            None,
        )
        if booking:
            booking_client.delete_booking(booking.booking_id)
        return

    logger.warning("No booking data to clean")
