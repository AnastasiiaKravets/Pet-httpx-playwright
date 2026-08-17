from collections.abc import Generator
from pathlib import Path

import allure
import pytest

from config import settings
from src.api.API_Client import API_Client
from src.helpers.auth_manager import AuthManager
from test.fixtures.cleanup import *  # noqa: F401, F403
from test.fixtures.prepare_data import *  # noqa: F401, F403


@pytest.fixture(scope="session")
def api_client() -> Generator[API_Client, None, None]:
    with API_Client(base_url=settings.RESTFULL_BASE_API_URL) as client:
        yield client


@pytest.fixture(scope="function")
def authorized_api_client() -> Generator[API_Client, None, None]:
    token = AuthManager.get_token()
    headers = {"Cookie": f"token={token}"}
    with API_Client(base_url=settings.RESTFULL_BASE_API_URL, headers=headers) as auth_client:
        yield auth_client


@pytest.fixture(scope="function")
def token() -> str:
    return AuthManager.get_token()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    setattr(item, f"rep_{report.when}", report)


@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item, nextitem):
    if hasattr(item, "queued_attachments"):
        for att in item.queued_attachments:
            if att["is_file"]:
                # Check that trace file exists before attempting processing
                if Path(att["source"]).exists():
                    allure.attach.file(att["source"], name=att["name"], attachment_type=att["type"])
                    # Automatically cleans up local trace archive files on disk
                    try:
                        Path(att["source"]).unlink()
                    except OSError:
                        pass
            else:
                allure.attach(att["source"], name=att["name"], attachment_type=att["type"])
