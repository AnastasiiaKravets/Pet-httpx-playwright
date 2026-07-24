from config import settings
from src.api.API_Client import API_Client
from src.helpers.auth_manager import AuthManager

from test.fixtures.cleanup import *


@pytest.fixture(scope="session")
def api_client():
    with API_Client(base_url=settings.RESTFULL_BASE_API_URL) as client:
        yield client


@pytest.fixture(scope="function")
def authorized_api_client():
    token = AuthManager.get_token()
    headers = {'Cookie': f'token={token}'}
    with API_Client(base_url=settings.RESTFULL_BASE_API_URL, headers=headers) as auth_client:
        yield auth_client


@pytest.fixture(scope="function")
def token():
    return AuthManager.get_token()
