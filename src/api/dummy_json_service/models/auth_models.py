from pydantic import EmailStr, PositiveInt, HttpUrl, Field

from src.api.dummy_json_service.models.common_models import StrictModel


class AuthRequest(StrictModel):
    username: str
    password: str
    expires_in: int | None = Field(None, alias='expiresInMins')

class AuthResponse(StrictModel):
    accessToken: str
    refreshToken: str
    id: PositiveInt
    username: str
    email: EmailStr
    firstName: str
    lastName: str
    gender: str
    image: HttpUrl

