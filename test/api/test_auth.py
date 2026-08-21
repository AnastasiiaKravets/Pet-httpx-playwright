import pytest

from src.api.models.auth_models import LogoutResponse, Token, ValidateResponse
from src.api.models.common_models import BasicErrorResponse, BasicWarningResponse
from src.data.data_generators import get_valid_user


@pytest.mark.api
def test_login_valid_credentials(api_client):
    response = api_client.post("auth/login", payload=get_valid_user())

    assert response.status_code == 200

    Token.model_validate(response.json())


@pytest.mark.parametrize(
    "credentials_override",
    [{"username": ""}, {"password": ""}, {"username": "invalid"}, {"password": "invalid"}],
    ids=["Empty username", "Empty password", "Invalid username", "Invalid password"],
)
@pytest.mark.api
def test_login_invalid_credentials(api_client, credentials_override):
    user = get_valid_user()
    user.update(credentials_override)

    response = api_client.post("auth/login", payload=user)
    assert response.status_code == 401
    error_response = BasicErrorResponse.model_validate(response.json())
    assert error_response.error == "Invalid credentials"


@pytest.mark.api
def test_validate_token(authorized_api_client, token):
    response = authorized_api_client.post("auth/validate", payload=Token(token=token))

    assert response.status_code == 200
    validate_response = ValidateResponse.model_validate(response.json())
    assert validate_response.valid, "Token should be valid"


@pytest.mark.parametrize(
    "token_payload, expected_status_code, error_message",
    [("", 401, "No token provided"), ("ltwuVTzYnXYed87j", 403, "Invalid token")],
    ids=["Empty token", "Invalid token"],
)
@pytest.mark.api
def test_validate_invalid_token(authorized_api_client, token_payload, expected_status_code, error_message):
    response = authorized_api_client.post("auth/validate", payload=Token(token=token_payload))

    assert response.status_code == expected_status_code
    error_response = BasicErrorResponse.model_validate(response.json())
    assert error_response.error == error_message


@pytest.mark.api
def test_logout(authorized_api_client, token):
    payload = Token(token=token)

    response = authorized_api_client.post("auth/logout", payload=payload)

    assert response.status_code == 200
    logout_response = LogoutResponse.model_validate(response.json())
    assert logout_response.success, "Logout should be successful"


@pytest.mark.api
def test_logout_with_missing_token(authorized_api_client):
    response = authorized_api_client.post("auth/logout", payload=Token(token=""))
    assert response.status_code == 400
    error_response = BasicWarningResponse.model_validate(response.json())
    assert error_response.message, "Token is required"


@pytest.mark.api
@pytest.mark.workflow
def test_full_token_validation(api_client):
    """
    Login -> Validate token -> logout -> Validate token
    """
    response = api_client.post("auth/login", payload=get_valid_user())
    assert response.status_code == 200
    token = Token.model_validate(response.json())

    response = api_client.post("auth/validate", payload=token)
    assert response.status_code == 200
    validate_response = ValidateResponse.model_validate(response.json())
    assert validate_response.valid, "Token should be valid"

    response = api_client.post("auth/logout", payload=token)
    assert response.status_code == 200
    logout_response = LogoutResponse.model_validate(response.json())
    assert logout_response.success, "Logout should be successful"

    response = api_client.post("auth/validate", payload=token)
    assert response.status_code == 200
    validate_response = ValidateResponse.model_validate(response.json())
    assert not validate_response.valid, "Token should be invalid"
