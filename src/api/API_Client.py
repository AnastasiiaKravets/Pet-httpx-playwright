import random
import time
from typing import Any, Self

import httpx
from pydantic import BaseModel

from config import settings
from src.helpers.logger import logger


class API_Client:
    """
    Base HTTP client — thin wrapper around httpx.

    All API interaction in the framework goes through this class.
    Never instantiate httpx directly in tests or fixtures.

    Features:
        - Base URL injection
        - Auth header management
        - Structured request/response logging
        - Automatic retry on HTTP 429, 502, 503, 504

    Args:
        base_url:    API root, e.g. "https://example.com/api"
        headers:     Default headers merged into every request
        timeout:     Per-request timeout in seconds
    """

    RETRY_STATUSES = {429, 502, 503, 504}  # Too Many Requests, Bad Gateway, Service Unavailable, Gateway Timeout
    RETRIES = 3
    BASE_DELAY = 0.5

    def __init__(self, base_url: str, headers: dict[str, str] | None = None, timeout: int | None = None, **kwargs):
        default_headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if headers:
            default_headers.update(headers)
        default_timeout = timeout if timeout is not None else settings.DEFAULT_API_TIMEOUT

        self.client = httpx.Client(base_url=base_url, timeout=default_timeout, headers=default_headers, **kwargs)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object):
        self.client.close()

    def _request(
        self, method: str, path: str, payload: BaseModel | dict[str, Any] | None = None, **kwargs
    ) -> httpx.Response:
        """
        Send an HTTP request and retry it automatically for temporary server errors.

        The request is retried for HTTP 429, 502, 503 and 504 using exponential
        backoff strategy with a small random jitter to reduce simultaneous retries
        during parallel execution.
        All requests and responses are logged. Transport errors are logged and re-raised.

        Args:
            method: HTTP method.
            path: Relative API endpoint path.
            payload: Request body as a Pydantic model or dictionary.
            **kwargs: Additional arguments passed to ``httpx.Client.request()``.

        Returns:
            The final ``httpx.Response`` object. This may contain one of the retryable
            status codes if all retry attempts were exhausted.

        Raises:
            httpx.TimeoutException: If the request times out.
            httpx.RequestError: If a transport-level error occurs.
        """

        logger.info(
            dict(
                name="REQUEST",
                method=method,
                path=f"{self.client.base_url}{path}",
                payload=payload,
                additional=kwargs,
                headers=self.client.headers,
            )
        )

        try:
            for attempt in range(self.RETRIES + 1):
                if payload is not None:
                    response = self.client.request(method, path, json=self._serialize_payload(payload), **kwargs)
                else:
                    response = self.client.request(method, path, **kwargs)

                if (response.status_code not in self.RETRY_STATUSES) or (attempt == self.RETRIES):
                    break

                # Exponential delay, in order to spread request in time for parallel run
                delay = self.BASE_DELAY * (2**attempt) + random.uniform(0, 0.5)
                logger.warning(
                    dict(
                        name="RETRY",
                        attempt=attempt + 1,
                        status_code=response.status_code,
                        detail=f"Next attempt in {delay} seconds.",
                    )
                )
                time.sleep(delay)

        except httpx.TimeoutException as exc:
            logger.error(dict(name="REQUEST TIMEOUT", method=method, path=path, error=str(exc)))
            raise
        except httpx.RequestError as exc:
            logger.error(dict(name="REQUEST ERROR", method=method, path=path, error=str(exc)))
            raise

        logger.info(
            dict(
                name="RESPONSE",
                method=method,
                path=f"{self.client.base_url}{path}",
                status_code=response.status_code,
                body=response.text,
            )
        )
        return response

    def get(self, path: str, **kwargs) -> httpx.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, payload: BaseModel | dict[str, Any], **kwargs) -> httpx.Response:
        return self._request("POST", path, payload, **kwargs)

    def put(self, path: str, payload: BaseModel | dict[str, Any], **kwargs) -> httpx.Response:
        return self._request("PUT", path, payload, **kwargs)

    def delete(self, path: str, **kwargs) -> httpx.Response:
        return self._request("DELETE", path, **kwargs)

    @staticmethod
    def _serialize_payload(payload: BaseModel | dict[str, Any]) -> dict[str, Any]:
        if isinstance(payload, BaseModel):
            return payload.model_dump(exclude_unset=True, by_alias=True)
        return payload
