from playwright.sync_api import Page

from src.ui.common.base_component import BaseComponent


class FooterComponent(BaseComponent):
    def __init__(self, page: Page):
        component_locator = page.locator("footer")
        super().__init__(component_locator)

        self.title = self.page.get_by_role("heading").first
        self.description = self.page.get_by_role("paragraph")
        self.location = self.page.locator("//i[contains(@class, 'bi-geo-alt')]/..")
        self.phone = self.page.locator("//i[contains(@class, 'bi-telephone')]/..")
        self.email = self.page.locator("//i[contains(@class, 'bi-envelope')]/..")
