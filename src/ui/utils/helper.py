import re

from playwright.sync_api import Locator


def text(locator: Locator):
    return locator.text_content().lstrip()


def price(locator: Locator):
    price = re.sub(r'[^0-9]', '', text(locator))
    return int(price)
