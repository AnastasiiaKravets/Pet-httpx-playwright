from playwright.sync_api import Page

from src.ui.common.base_component import BaseComponent


class HeaderComponent(BaseComponent):
    def __init__(self, page: Page):
        component_locator = page.locator("nav.navbar")
        super().__init__(component_locator)

        self.title_link = page.locator("a.navbar-brand")
        self.contact_link = page.get_by_role("link", name="Contact")
