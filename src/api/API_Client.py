from typing import Any

import httpx
from pydantic import BaseModel

from config import settings
from src.helpers.logger import logger


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

    def _request(self, method: str, path: str, payload: BaseModel | dict[str, Any] = None, **kwargs):
        logger.info(dict(
            name='REQUEST',
            method=method,
            path=f'{self.client.base_url}{path}',
            payload=payload,
            additional=kwargs,
            headers=self.client.headers
        ))

        try:
            if payload is not None:
                response = self.client.request(method, path, json=self._serialize_payload(payload), **kwargs)
            else:
                response = self.client.request(method, path, **kwargs)
        except httpx.TimeoutException as exc:
            logger.error(dict(name="REQUEST TIMEOUT", method=method, path=path))
            raise
        except httpx.RequestError as exc:
            logger.error(dict(name="REQUEST ERROR", method=method, path=path, error=str(exc)))
            raise

        logger.info(dict(
            name='RESPONSE',
            method=method,
            path=f'{self.client.base_url}{path}',
            status_code=response.status_code,
            body=response.text
        ))
        return response

    def get(self, path: str, **kwargs):
        return self._request('GET', path, **kwargs)

    def post(self, path: str, payload: BaseModel | dict[str, Any], **kwargs):
        return self._request('POST', path, payload, **kwargs)

    def put(self, path: str, payload: BaseModel | dict[str, Any], **kwargs):
        return self._request('PUT', path, payload, **kwargs)

    def delete(self, path: str, **kwargs):
        return self._request('DELETE', path, **kwargs)

    @staticmethod
    def _serialize_payload(payload: BaseModel | dict[str, Any]):
        if isinstance(payload, BaseModel):
            return payload.model_dump(exclude_unset=True, by_alias=True)
        return payload
