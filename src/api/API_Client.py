from typing import Any

import httpx

from config import settings
from src.api.dummy_json_service.models.common_models import BaseModel


class API_Client:

    def __init__(self, base_url: str, headers=None, timeout: int=None, **kwargs):
        default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if headers:
            default_headers.update(headers)
        default_timeout = timeout if timeout else settings.DEFAULT_API_TIMEOUT

        self.client = httpx.Client(base_url=base_url,
                                   timeout=default_timeout,
                                   headers = default_headers,
                                   **kwargs)

    def __enter__(self) -> API_Client:
        return self

    def __exit__(self, *_: object):
        self.client.close()

    def get(self, path: str, **kwargs):
        return self.client.get(path, **kwargs)

    def post(self, path: str, payload: BaseModel | dict[str, Any], **kwargs):
        return self.client.post(path, json=self._serialize_payload(payload), **kwargs)

    def put(self, path: str, payload: BaseModel | dict[str, Any], **kwargs):
        return self.client.put(path, json=self._serialize_payload(payload), **kwargs)

    def delete(self, path: str, **kwargs):
        return self.client.delete(path, **kwargs)

    @staticmethod
    def _serialize_payload(payload: BaseModel | dict[str, Any]):
        if isinstance(payload, BaseModel):
            return payload.model_dump(exclude_unset=True, by_alias=True)
        return payload
