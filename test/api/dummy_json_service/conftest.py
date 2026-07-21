import pytest

from config import settings
from src.api.API_Client import API_Client
from src.api.dummy_json_service.helpers.data_helper import get_valid_user
from src.api.dummy_json_service.models.auth_models import AuthResponse


@pytest.fixture(scope="package")
def dummy_api_client():
    with API_Client(base_url=settings.DUMMY_BASE_API_URL) as client:
        yield client


@pytest.fixture(scope="function")
def dummy_authorized_api_client(dummy_api_client):
    response = dummy_api_client.post('auth/login', payload=get_valid_user())
    auth_response = AuthResponse.model_validate(response.json())
    headers = {'Authorization': f'Bearer {auth_response.accessToken}'}
    with API_Client(base_url=settings.DUMMY_BASE_API_URL, headers=headers) as auth_client:
        yield auth_client
