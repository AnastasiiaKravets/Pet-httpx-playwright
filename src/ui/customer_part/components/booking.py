from playwright.sync_api import Page

from src.ui.common.alert_component import AlertComponent
from src.ui.common.base_component import BaseComponent
from src.ui.common.calendar_component import CalendarComponent


class BookingDetailsComponent(BaseComponent):
    def __init__(self, page: Page):
        component_locator = page.locator("div.booking-card")
        super().__init__(component_locator)

        self.calendar = CalendarComponent(page)
        self.alert = AlertComponent(page)

        self.title = self.page.get_by_role("heading", level=2)
        self.confirmed_dates = self.page.get_by_role("strong")
        self.price_per_night = self.page.locator("//*[contains(text(), 'per night')]/..")
        self.total_price = self.page.locator("div.card-body div").last

        self.first_name = self.page.get_by_role("textbox", name="Firstname")
        self.last_name = self.page.get_by_role("textbox", name="Lastname")
        self.email = self.page.get_by_role("textbox", name="Email")
        self.phone = self.page.get_by_role("textbox", name="Phone")

        self.reserve_button = self.page.get_by_role("button", name="Reserve Now")
        self.cancel_button = self.page.get_by_role("button", name="Cancel")
        self.return_button = self.page.get_by_role("link", name="Return home")

    def fill_user_data(self, user_data: dict[str, str]) -> None:
        self.first_name.fill(user_data["first_name"])
        self.last_name.fill(user_data["last_name"])
        self.email.fill(user_data["email"])
        self.phone.fill(user_data["phone"])
