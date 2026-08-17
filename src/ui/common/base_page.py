from abc import ABC, abstractmethod
from typing import Self

from playwright.sync_api import Page, expect

from config import settings


class BasePage(ABC):
    @property
    @abstractmethod
    def url_part(self) -> str:
        pass

    @classmethod
    def full_url(cls) -> str:
        return f"{settings.BASE_UI_URL}{cls.url_part}"

    def __init__(self, page: Page):
        self.page = page
        self.loading_text = self.page.locator("//p[contains(text(), 'Loading...')]")

    def open(self, *args, **kwargs) -> Self:
        self.page.goto(self._build_url(*args, **kwargs))
        expect(self.loading_text).not_to_be_visible()
        return self

    def _build_url(self, *args, **kwargs) -> str:
        return self.url_part
