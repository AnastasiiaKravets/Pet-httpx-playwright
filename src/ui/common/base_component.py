from playwright.sync_api import Locator


class BaseComponent:
    def __init__(self, component_locator: Locator) -> None:
        self.page = component_locator

    def scroll_into_view(self):
        self.page.scroll_into_view_if_needed()
