import pytest
from playwright.sync_api import Page

from src.ui.admin_part.pages.admin_room_details_page import AdminRoomDetailsPage


@pytest.mark.ui
def test_created_booking_in_rooms(auth_page: Page, booking_data):
    room_page = AdminRoomDetailsPage(auth_page)
    room_page.open(booking_data.room_id)

    assert room_page.contains_booking(booking_data.booking_dates.checkin, booking_data.booking_dates.checkout), \
        "There is no created booking in the room details page"
    actual_booking = room_page.get_booking(booking_data.booking_dates.checkin, booking_data.booking_dates.checkout)
    assert actual_booking.first_name == booking_data.first_name
    assert actual_booking.last_name == booking_data.last_name
    assert actual_booking.deposit_paid == booking_data.deposit_paid


@pytest.mark.ui
def test_created_booking_in_messages(page, booking_data):
    pass


@pytest.mark.ui
def test_created_booking_in_reports(page, booking_data):
    pass
