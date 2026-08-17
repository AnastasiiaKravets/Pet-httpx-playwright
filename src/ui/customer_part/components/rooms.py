from playwright.sync_api import Locator, Page, expect

from src.ui.common.base_component import BaseComponent
from src.ui.utils.helper import text


class RoomCardComponent(BaseComponent):
    def __init__(self, component_locator: Locator):
        super().__init__(component_locator)

        self.image = self.page.locator("div.room-image img")
        self.title = self.page.locator("div.card-body .card-title")
        self.description = self.page.locator("p.card-text")
        self.amenities = self.page.locator("div.card-text")
        self.price = self.page.locator("div.card-footer div")
        self.book_button = self.page.get_by_role("link", name="Book now")

    def get_image_src(self) -> str | None:
        return self.image.get_attribute("src")

    def get_amenities_text(self) -> list[str]:
        return text(self.amenities).split(" ")


class RoomListComponent(BaseComponent):
    def __init__(self, page: Page):
        component_locator = page.locator("#rooms")
        super().__init__(component_locator)

        self.room_cards = self.page.locator("div.room-card")

    def get_all_rooms_cards(self) -> list[RoomCardComponent]:
        return [RoomCardComponent(self.room_cards.nth(i)) for i in range(self.room_cards.count())]

    def get_room_card(self, index: int) -> RoomCardComponent:
        return RoomCardComponent(self.room_cards.nth(index))

    def count_cards(self) -> int:
        return self.room_cards.count()

    def open_first_room(self) -> None:
        RoomCardComponent(self.room_cards.first).book_button.click()

    def wait_at_least_one_room(self, timeout: int = 1000) -> None:
        expect(self.room_cards.first).to_be_visible(timeout=timeout)
