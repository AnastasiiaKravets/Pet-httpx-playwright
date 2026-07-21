import pytest

from config import settings
from src.api.API_Client import API_Client


@pytest.fixture(scope="package")
def api_client():
    with API_Client(base_url=settings.RESTFULL_BASE_API_URL) as client:
        yield client
