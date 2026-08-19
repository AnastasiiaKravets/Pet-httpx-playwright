from datetime import datetime, timedelta

from config import settings
from src.api.api_client import APIClient
from src.api.models.auth_models import Token
from src.data.data_generators import get_valid_user


class AuthManager:
    _token: str | None = None
    _expires_at: datetime | None = None
    expiration_in_minutes = 9

    @classmethod
    def get_token(cls) -> str:
        if cls._token is None or cls._is_expired():
            cls._login()
        if cls._token is None:
            raise RuntimeError("Failed to get authentication token.")
        return cls._token

    @classmethod
    def _is_expired(cls) -> bool:
        return cls._expires_at is None or datetime.now() >= cls._expires_at

    @classmethod
    def _login(cls) -> None:
        with APIClient(base_url=settings.RESTFULL_BASE_API_URL) as api_client:
            response = api_client.post("auth/login", payload=get_valid_user())
            response.raise_for_status()
        token = Token.model_validate(response.json())
        cls._token = token.token
        cls._expires_at = datetime.now() + timedelta(minutes=cls.expiration_in_minutes)
