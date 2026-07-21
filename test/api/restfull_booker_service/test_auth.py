import pytest

from src.api.restfull_booker_service.models.auth_models import LogoutResponse
from src.api.restfull_booker_service.models.auth_models import Token, ValidateResponse
from src.api.restfull_booker_service.models.common_models import BasicErrorResponse, BasicWarningResponse
from src.data.user_data import get_valid_user


@pytest.mark.api
def test_login_valid_credentials(api_client):
    response = api_client.post('auth/login', payload=get_valid_user())

    assert response.status_code == 200

    Token.model_validate(response.json())


@pytest.mark.parametrize('credentials_override', [{'username': ''},
                                      {'password': ''},
                                      {'username': 'invalid'},
                                      {'password': 'invalid'}])
@pytest.mark.api
def test_login_invalid_credentials(api_client, credentials_override):
    user = get_valid_user()
    user.update(credentials_override)

    response = api_client.post('auth/login', payload=user)
    assert response.status_code == 401
    error_response = BasicErrorResponse.model_validate(response.json())
    assert error_response.error == 'Invalid credentials'


@pytest.mark.api
def test_validate_token(authorized_api_client, token):
    response = authorized_api_client.post('auth/validate', payload=Token(token=token))

    assert response.status_code == 200
    validate_response = ValidateResponse.model_validate(response.json())
    assert validate_response.valid, 'Token should be valid'


@pytest.mark.parametrize('token_payload, expected_status_code, error_message',
                         [('', 401, 'No token provided'),
                          ('123456789', 403, 'Invalid token'),
                          ('ltwuVTzYnXYed87j', 403, 'Invalid token')])
@pytest.mark.api
def test_validate_invalid_token(authorized_api_client, token_payload, expected_status_code, error_message):
    response = authorized_api_client.post('auth/validate', payload=Token(token=token_payload))

    assert response.status_code == expected_status_code
    error_response = BasicErrorResponse.model_validate(response.json())
    assert error_response.error, error_message


@pytest.mark.api
def test_logout(authorized_api_client, token):
    payload = Token(token=token)

    response = authorized_api_client.post('auth/logout', payload=payload)

    assert response.status_code == 200
    logout_response = LogoutResponse.model_validate(response.json())
    assert logout_response.success, 'Logout should be successful'


@pytest.mark.api
@pytest.mark.parametrize('token_payload, expected_status_code, error_message',
                         [('', 400, 'Token is required')])
def test_logout(authorized_api_client, token_payload, expected_status_code, error_message):
    response = authorized_api_client.post('auth/logout', payload=Token(token=token_payload))
    print(response.text)
    assert response.status_code == expected_status_code
    error_response = BasicWarningResponse.model_validate(response.json())
    assert error_response.message, error_message


@pytest.mark.api
@pytest.mark.workflows
def test_full_token_validation(api_client):
    """
    Login -> Validate token -> logout -> Validate token
    """
    response = api_client.post('auth/login', payload=get_valid_user())
    assert response.status_code == 200
    token = Token.model_validate(response.json())

    response = api_client.post('auth/validate', payload=token)
    assert response.status_code == 200
    validate_response = ValidateResponse.model_validate(response.json())
    assert validate_response.valid, 'Token should be valid'

    response = api_client.post('auth/logout', payload=token)
    assert response.status_code == 200
    logout_response = LogoutResponse.model_validate(response.json())
    assert logout_response.success, 'Logout should be successful'

    response = api_client.post('auth/validate', payload=token)
    assert response.status_code == 200
    validate_response = ValidateResponse.model_validate(response.json())
    assert not validate_response.valid, 'Token should be invalid'