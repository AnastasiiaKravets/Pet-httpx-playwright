from collections.abc import Generator
from pathlib import Path

import pytest
from playwright.sync_api import Page, Playwright, sync_playwright

from config import settings
from src.helpers.auth_manager import AuthManager
from src.ui.utils.playwright_manager import PlaywrightManager


@pytest.fixture(scope="session", autouse=True)
def playwright() -> Generator[Playwright, None, None]:
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session", autouse=True)
def browser(playwright):
    manager = PlaywrightManager(playwright)
    browser = manager.create_browser()
    yield browser

    browser.close()


@pytest.fixture(scope="function")
def new_context(browser, playwright, request):
    manager = PlaywrightManager(playwright)
    context = manager.create_context(browser)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    # Initialize the queue on the test node
    request.node.queued_attachments = []

    yield context

    trace_path = f"trace_{request.node.name}.zip"
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    if failed:
        context.tracing.stop(path=trace_path)
        if Path(trace_path).exists():
            # Queue the trace file path to be processed inside the teardown hook
            request.node.queued_attachments.append(
                {
                    "is_file": True,
                    "source": trace_path,
                    "name": "Playwright Trace",
                    "type": "application/vnd.allure.playwright-trace",
                    # in order to open trace directly from allure report
                }
            )
    else:
        context.tracing.stop()

    context.close()


@pytest.fixture(scope="function")
def page(new_context) -> Generator[Page, None, None]:
    page = new_context.new_page()
    yield page


@pytest.fixture(scope="function")
def auth_page(new_context) -> Generator[Page, None, None]:
    new_context.add_cookies(
        [
            {
                "name": "token",
                "value": AuthManager.get_token(),
                "domain": settings.DOMAIN,
                "path": "/",
            }
        ]
    )
    page = new_context.new_page()
    yield page
