import json
import sys
from typing import Any

from loguru import logger

logger.remove(0)
logger.add(sys.stderr, format="{level} - {time} - {message} - {process}")


SENSITIVE_KEYS = {
    "authorization",
    "cookie",
    "set-cookie",
    "token",
    "access_token",
    "refresh_token",
    "api_key",
    "user",
    "username",
    "password",
}


def redact_sensitive_data(data: Any) -> Any:
    if isinstance(data, dict):
        return {key: "***" if key in SENSITIVE_KEYS else redact_sensitive_data(value) for key, value in data.items()}

    if isinstance(data, list):
        return [redact_sensitive_data(item) for item in data]

    if isinstance(data, str):
        try:
            parsed_data = json.loads(data)
        except json.JSONDecodeError:
            return data
        return redact_sensitive_data(parsed_data)

    return data
