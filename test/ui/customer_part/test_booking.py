import pytest
from playwright.sync_api import expect

from src.api.clients.room_client import RoomClient
from src.data.data_generators import get_user_reservation_data
from src.helpers.date_helper import get_date_today, get_future_date, get_only_day
from src.ui.customer_part.pages.main_page import MainPage
from src.ui.customer_part.pages.room_details_page import RoomDetailsPage
from src.ui.utils.helper import text, price


@pytest.mark.ui
def test_room_availability(page, api_client):
    date_from = get_date_today()
    date_to = get_future_date(delta_in_days=5)
    expected_rooms_data = RoomClient(api_client).available_rooms(date_from, date_to)
    expected_room_count = min(len(expected_rooms_data), 3)  # by default there is only 3 rooms are shown at UI

    main_page = MainPage(page)
    main_page.open()

    main_page.checkin_input.fill(date_from)
    main_page.checkout_input.fill(date_to)
    main_page.check_availability_button.click()

    main_page.room_list.scroll_into_view()

    assert main_page.room_list.count_cards() == expected_room_count, f"There should be {expected_room_count} rooms visible"

    for actual_room, expected_room in zip(main_page.room_list.get_all_rooms_cards(), expected_rooms_data):
        assert actual_room.get_image_src() == expected_room.image
        assert text(actual_room.title) == expected_room.type
        assert text(actual_room.description) == expected_room.description
        assert actual_room.get_amenities_text() == expected_room.features
        assert price(actual_room.price) == expected_room.room_price


@pytest.mark.ui
def test_successful_booking_for_a_few_days(page, available_room_in_future, clear_booking_data):
    expected_days = 3  # by default from test data
    user_reservation_data = get_user_reservation_data()
    clear_booking_data.update(**available_room_in_future)  # to clear booking data after test

    room_detail_page = RoomDetailsPage(page, **available_room_in_future)
    room_detail_page.open()
    room_detail_page.booking_details.scroll_into_view()
    room_detail_page.booking_details.calendar.next_button.click()

    selected_days = room_detail_page.booking_details.calendar.get_selected_days()
    assert get_only_day(available_room_in_future['date_from']) == selected_days[0], "Different first day was selected"
    assert len(selected_days) == expected_days, "fShould be {expected_days} selected days for initial test data"

    room_detail_page.booking_details.reserve_button.click()
    expect(room_detail_page.booking_details.first_name).to_be_visible()

    room_detail_page.booking_details.fill_user_data(user_reservation_data)
    room_detail_page.booking_details.reserve_button.click()

    expect(room_detail_page.booking_details.title).to_have_text('Booking Confirmed')
    assert (text(room_detail_page.booking_details.confirmed_dates) ==
            f'{available_room_in_future["date_from"]} - {available_room_in_future["date_to"]}')
    expect(room_detail_page.booking_details.return_button).to_be_visible()


@pytest.mark.ui
def test_form_validation_empty_form(page, available_room_in_future):
    room_detail_page = RoomDetailsPage(page, **available_room_in_future)
    room_detail_page.open()
    room_detail_page.booking_details.scroll_into_view()

    room_detail_page.booking_details.reserve_button.click()
    expect(room_detail_page.booking_details.first_name).to_be_visible()

    room_detail_page.booking_details.reserve_button.click()
    expect(room_detail_page.booking_details.alert.page).to_be_visible()
    expected_errors = ['must not be empty', 'size must be between 3 and 30', 'Lastname should not be blank',
                       'Firstname should not be blank', 'size must be between 11 and 21', 'must not be empty',
                       'size must be between 3 and 18']
    assert room_detail_page.booking_details.alert.get_messages().sort() == expected_errors.sort()
