from config import settings
from src.api.API_Client import API_Client
from src.api.restfull_booker_service.models.auth_models import Token
from src.data.user_data import get_valid_user

from test.fixtures.prepare_data import *


@pytest.fixture(scope="session")
def api_client():
    with API_Client(base_url=settings.RESTFULL_BASE_API_URL) as client:
        yield client


@pytest.fixture(scope="module")
def authorized_api_client(api_client):
    response = api_client.post('auth/login', payload=get_valid_user())
    auth_response = Token.model_validate(response.json())
    headers = {'Cookie': f'token={auth_response.token}'}
    with API_Client(base_url=settings.RESTFULL_BASE_API_URL, headers=headers) as auth_client:
        yield auth_client


@pytest.fixture(scope="module")
def token(authorized_api_client):
    return authorized_api_client.client.headers['Cookie'].replace('token=', '')
