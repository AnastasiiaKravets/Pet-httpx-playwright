from pydantic import Field

from src.api.models.common_models import StrictModel


class AuthRequest(StrictModel):
    username: str
    password: str


class Token(StrictModel):
    token: str = Field(max_length=16)


class ValidateResponse(StrictModel):
    valid: bool


class LogoutResponse(StrictModel):
    success: bool
