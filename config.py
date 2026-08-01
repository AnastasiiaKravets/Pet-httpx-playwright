import os
from enum import StrEnum
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV = os.getenv("ENV", "local")
print(_ENV)
_ENV_FILE = Path(__file__).parent / "config" / f".env.{_ENV}"


class BrowserType(StrEnum):
    CHROME = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"


class Settings(BaseSettings):
    ENV: str
    AUTH_KEY: str
    DEFAULT_API_TIMEOUT: int

    DUMMY_BASE_API_URL: str
    DUMMY_TEST_API_USERNAME: str
    DUMMY_TEST_API_PASSWORD: str

    RESTFULL_BASE_API_URL: str

    RESTFULL_USER: str
    RESTFULL_PASSWORD: str

    BASE_UI_URL: str
    DOMAIN: str
    BROWSER: BrowserType
    DEVICE: str | None = None  # none for desktop, value for mobile device, ex. 'Galaxy Tab S4'
    HEADLESS: bool
    SLOW_MO: int = 0

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        # cli_parse_args=True,
        extra="ignore",
    )


settings = Settings()
