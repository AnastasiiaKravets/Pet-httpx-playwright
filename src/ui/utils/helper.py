import re

from playwright.sync_api import Locator


def text(locator: Locator) -> str:
    return locator.text_content().lstrip()


def price(locator: Locator) -> int:
    price_text = re.sub(r'[^0-9]', '', text(locator))
    return int(price_text)
