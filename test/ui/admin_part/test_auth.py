import pytest
from playwright.sync_api import expect

from src.data.data_generators import get_valid_user
from src.ui.admin_part.pages.admin_room_page import AdminRoomPage
from src.ui.admin_part.pages.login_page import LoginPage


@pytest.mark.ui
def test_valid_login(page):
    user = get_valid_user()

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(user)

    room_page = AdminRoomPage(page)
    expect(page).to_have_url(room_page.full_url())
    expect(room_page.header.rooms_tab).to_contain_class('active')
