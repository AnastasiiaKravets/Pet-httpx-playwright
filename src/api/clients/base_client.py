from typing import TypeVar

from httpx import Response
from pydantic import BaseModel

from src.api.API_Client import API_Client

T = TypeVar("T", bound=BaseModel)


class BaseClient:
    def __init__(self, api_client: API_Client):
        self.api_client = api_client

    @staticmethod
    def assert_response_ok(response: Response) -> None:
        response.raise_for_status()

    @staticmethod
    def assert_response_and_parse(response: Response, model: type[T]) -> T:
        response.raise_for_status()
        return model.model_validate(response.json())
