from playwright.sync_api import Page

from src.ui.common.base_component import BaseComponent


class AlertComponent(BaseComponent):

    def __init__(self, page: Page):
        self.page = page.locator(".alert")

        self.error_messages = self.page.locator("li")

    def get_messages(self) -> list[str]:
        return [message.strip() for message in self.error_messages.all_text_contents()]

    def get_message_count(self) -> int:
        return self.error_messages.count()
