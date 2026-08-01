import pytest
from playwright.sync_api import expect

from src.api.clients.branding_client import BrandingClient
from src.api.clients.room_client import RoomClient
from src.ui.customer_part.pages.main_page import MainPage
from src.ui.utils.helper import price, text


@pytest.mark.ui
def test_room_list_data(page, api_client):
    expected_rooms_data = RoomClient(api_client).get_all_rooms()
    expected_room_count = min(len(expected_rooms_data), 3)  # by default there is only 3 rooms are shown at UI

    main_page = MainPage(page)
    main_page.open()
    main_page.room_list.wait_at_least_one_room()

    assert main_page.room_list.count_cards() == expected_room_count, (
        f"There should be {expected_room_count} rooms visible"
    )

    for actual_room, expected_room in zip(main_page.room_list.get_all_rooms_cards(), expected_rooms_data, strict=False):
        assert actual_room.get_image_src() == expected_room.image
        assert text(actual_room.title) == expected_room.type
        assert text(actual_room.description) == expected_room.description
        assert actual_room.get_amenities_text() == expected_room.features
        assert price(actual_room.price) == expected_room.room_price


@pytest.mark.ui
def test_hotel_data(page, api_client):
    expected_hotel_data = BrandingClient(api_client).get_hotel_details()
    expected_address_text = (
        f"{expected_hotel_data.address.line1}, {expected_hotel_data.address.line2}, "
        f"{expected_hotel_data.address.post_town}, {expected_hotel_data.address.county}, "
        f"{expected_hotel_data.address.post_code}"
    )

    main_page = MainPage(page)
    main_page.open()

    assert text(main_page.header.title_link) == expected_hotel_data.name

    assert text(main_page.heading) == f"Welcome to {expected_hotel_data.name}"
    assert text(main_page.heading_description) == expected_hotel_data.description
    expect(main_page.booking_button).to_be_visible()

    main_page.footer.scroll_into_view()
    assert text(main_page.footer.title) == expected_hotel_data.name
    assert text(main_page.footer.description) == expected_hotel_data.description
    assert text(main_page.footer.location) == expected_address_text
    assert text(main_page.footer.phone) == expected_hotel_data.contact.phone
    assert text(main_page.footer.email) == expected_hotel_data.contact.email
