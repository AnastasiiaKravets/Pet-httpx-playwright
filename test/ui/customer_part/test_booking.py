from src.api.restfull_booker_service.clients.room_client import RoomClient
from src.helpers.date_helper import get_date_today, get_future_date
from src.ui.customer_part.pages.main_page import MainPage
from src.ui.utils.helper import text


def test_successfull_booking_for_a_few_days():
    pass


def test_form_validation():
    pass


def test_room_availability(page, api_client):
    date_from = get_date_today()
    date_to = get_future_date(delta_in_days=5)
    expected_rooms_data = RoomClient(api_client).available_rooms(date_from, date_to)
    expected_room_count = min(len(expected_rooms_data), 3)  # by default there is only 3 rooms are shown at UI
    print(expected_rooms_data)

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
        assert actual_room.get_price() == expected_room.room_price
