from abc import ABC, abstractmethod

from playwright.sync_api import Page, expect

from config import settings


class BasePage(ABC):
    @property
    @abstractmethod
    def url_part(self):
        pass

    @classmethod
    def full_url(cls):
        return f"{settings.BASE_UI_URL}{cls.url_part}"

    def __init__(self, page: Page):
        self.page = page
        self.loading_text = self.page.locator("//p[contains(text(), 'Loading...')]")

    def open(self):
        self.page.goto(self.url_part)
        expect(self.loading_text).not_to_be_visible()
        return self
