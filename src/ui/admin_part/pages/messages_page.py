from playwright.sync_api import Locator, expect
from pydantic import BaseModel

from src.ui.common.base_page import BasePage


class MessagesPage(BasePage):
    url_part = 'admin/message'

    def __init__(self, page):
        super().__init__(page)
        self.message_rows = self.page.locator('div.row.detail')

    def _find_row(self, name: str) -> Locator:
        for i in range(self.message_rows.count()):
            row = self.message_rows.nth(i)
            value = row.locator(f"//div[contains(@data-testid, 'message{i}')]").inner_text()

            if value == name:
                return row

        raise AssertionError(
            f"Message with name {name} was not found."
        )

    def get_all_messages(self) -> list[MessageRow]:
        messages = []

        for i in range(self.message_rows.count()):
            values = self.message_rows.nth(i).locator("p").all_inner_texts()
            is_read = 'read-true' in self.message_rows.nth(i).get_attribute('class')
            messages.append(
                MessageRow(
                    name=values[0],
                    subject=values[1],
                    is_read=is_read
                )
            )
        return messages

    def get_message(self, name: str) -> MessageRow:
        row = self._find_row(name)
        is_read = 'read-true' in row.get_attribute('class')
        values = row.locator("p").all_inner_texts()

        return MessageRow(
            name=values[0],
            subject=values[1],
            is_read=is_read
        )

    def delete_message(self, name: str) -> None:
        row = self._find_row(name)

        row.locator("//span[contains(@data-testid, 'DeleteMessage')]").click()

    def contains_message(self, name: str) -> bool:
        for message in self.get_all_messages():
            if message.name == name:
                return True
        return False

    def wait_at_least_one_message(self, timeout: int = 1000) -> None:
        expect(self.message_rows.first).to_be_visible(timeout=timeout), "There are no messages"


class MessageRow(BaseModel):
    name: str
    subject: str
    is_read: bool
