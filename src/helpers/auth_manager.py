from datetime import datetime, timedelta

from config import settings
from src.api.API_Client import API_Client
from src.api.models.auth_models import Token
from src.data.user_data import get_valid_user


class AuthManager:
    _token: str | None = None
    _expires_at: datetime | None = None
    expiration_in_minutes = 9

    @classmethod
    def get_token(cls) -> str:
        if cls._token is None or cls._is_expired():
            cls._login()
        return cls._token

    @classmethod
    def _is_expired(cls) -> bool:
        return (
                cls._expires_at is None
                or datetime.now() >= cls._expires_at
        )

    @classmethod
    def _login(cls) -> None:
        response = API_Client(base_url=settings.RESTFULL_BASE_API_URL).post('auth/login', payload=get_valid_user())
        assert response.status_code == 200
        token = Token.model_validate(response.json())
        cls._token = token.token
        cls._expires_at = datetime.now() + timedelta(minutes=cls.expiration_in_minutes)
