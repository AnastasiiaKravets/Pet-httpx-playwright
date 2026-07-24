import pytest
from playwright.sync_api import sync_playwright

from config import settings
from src.helpers.auth_manager import AuthManager
from src.ui.utils.playwright_manager import PlaywrightManager


@pytest.fixture(scope="session", autouse=True)
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session", autouse=True)
def browser(playwright):
    manager = PlaywrightManager(playwright)
    browser = manager.create_browser()
    yield browser

    browser.close()


@pytest.fixture(scope='function')
def page(browser, playwright):
    manager = PlaywrightManager(playwright)
    context = manager.create_context(browser)
    page = context.new_page()
    yield page

    context.close()


@pytest.fixture(scope='function')
def auth_page(browser, playwright):
    manager = PlaywrightManager(playwright)
    context = manager.create_context(browser)
    context.add_cookies([
        {
            "name": "token",
            "value": AuthManager.get_token(),
            "domain": settings.DOMAIN,
            "path": "/",
        }
    ])
    page = context.new_page()
    yield page

    context.close()
