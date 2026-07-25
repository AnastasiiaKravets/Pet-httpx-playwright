import pytest
from playwright.sync_api import Page

from src.helpers.date_helper import get_only_day
from src.ui.admin_part.pages.admin_room_details_page import AdminRoomDetailsPage
from src.ui.admin_part.pages.messages_page import MessagesPage
from src.ui.admin_part.pages.report_page import ReportPage


@pytest.mark.ui
def test_created_booking_in_rooms(auth_page: Page, booking_data):
    room_page = AdminRoomDetailsPage(auth_page)
    room_page.open(booking_data.room_id)
    room_page.wait_at_least_one_booking()

    assert room_page.contains_booking(booking_data.booking_dates.checkin, booking_data.booking_dates.checkout), \
        "There is no created booking in the room details page"
    actual_booking = room_page.get_booking(booking_data.booking_dates.checkin, booking_data.booking_dates.checkout)
    assert actual_booking.first_name == booking_data.first_name
    assert actual_booking.last_name == booking_data.last_name
    assert actual_booking.deposit_paid == booking_data.deposit_paid


@pytest.mark.ui
def test_created_booking_in_messages(auth_page, booking_data):
    message_page = MessagesPage(auth_page)
    message_page.open()
    message_page.wait_at_least_one_message()

    full_name = booking_data.first_name + " " + booking_data.last_name
    assert message_page.contains_message(full_name)
    message = message_page.get_message(full_name)
    assert message.subject == "You have a new booking!"
    assert message.is_read is False


@pytest.mark.ui
def test_created_booking_in_reports(auth_page, booking_data):
    full_name = booking_data.first_name + " " + booking_data.last_name

    report_page = ReportPage(auth_page)
    report_page.open()

    report_page.calendar.next_button.click()
    selected_days = report_page.calendar.get_selected_days(full_name)

    assert selected_days, "There should be selected days for the created booking"
    assert selected_days[0] == get_only_day(booking_data.booking_dates.checkin)
    assert selected_days[-1] == get_only_day(booking_data.booking_dates.checkout) - 1
