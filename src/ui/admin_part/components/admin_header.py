from playwright.sync_api import Page

from src.ui.common.base_component import BaseComponent


class AdminHeaderComponent(BaseComponent):
    def __init__(self, page: Page):
        component_locator = page.get_by_role("navigation")
        super().__init__(component_locator)

        self.rooms_tab = self.page.get_by_role("link", name="Rooms")
        self.messages_tab = self.page.get_by_role("link", name="Messages")
        self.logout_button = self.page.get_by_role("button", name="Logout")

    def open_rooms_tab(self):
        self.rooms_tab.click()
        return self

    def open_messages_tab(self):
        self.messages_tab.click()
        return self

    def logout(self):
        self.logout_button.click()
        return self
