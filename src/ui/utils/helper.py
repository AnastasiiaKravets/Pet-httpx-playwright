from playwright.sync_api import Locator


def text(locator: Locator):
    return locator.text_content().lstrip()
