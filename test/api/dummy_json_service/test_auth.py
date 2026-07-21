import pytest

from src.api.dummy_json_service.helpers.data_helper import get_valid_user
from src.api.dummy_json_service.models.auth_models import AuthResponse
from src.api.dummy_json_service.models.common_models import BasicErrorResponse
from src.api.dummy_json_service.models.user_models import UserResponse


@pytest.mark.api
def test_authorize_valid_user(dummy_api_client):
    user = get_valid_user()

    response = dummy_api_client.post('auth/login', payload=user)

    assert response.status_code == 200
    auth_response = AuthResponse.model_validate(response.json())
    assert auth_response.username == user.username


@pytest.mark.api
@pytest.mark.parametrize('credentials_override, error_message',
                         [({'username': ''}, 'Username and password required'),
                          ({'password': ''}, 'Username and password required'),
                          ({'username': '78979'}, 'Invalid credentials'),
                          ({'password': '123'}, 'Invalid credentials')])
def test_authorize_user_with_invalid_credentials(dummy_api_client, credentials_override, error_message):
    user = get_valid_user(**credentials_override)

    response = dummy_api_client.post('auth/login', payload=user)

    assert response.status_code == 400
    error_response = BasicErrorResponse.model_validate(response.json())
    assert error_response.message == error_message


@pytest.mark.api
def test_get_authorized_user(dummy_authorized_api_client):
    user = get_valid_user()
    response = dummy_authorized_api_client.get('auth/me')

    assert response.status_code == 200
    user_data = UserResponse.model_validate(response.json())
    assert user_data.username == user.username
