from typing import Any

from src.ui.admin_part.components.admin_header import AdminHeaderComponent
from src.ui.common.base_page import BasePage


class LoginPage(BasePage):
    url_part = "admin"

    def __init__(self, page):
        super().__init__(page)
        self.header = AdminHeaderComponent(page)

        self.username_input = self.page.get_by_role("textbox", name="username")
        self.password_input = self.page.get_by_role("textbox", name="password")
        self.submit_button = self.page.get_by_role("button", name="login")

    def login_as(self, user_data: dict[str, Any]):
        self.username_input.fill(user_data["username"])
        self.password_input.fill(user_data["password"])
        self.submit_button.click()
        return self
