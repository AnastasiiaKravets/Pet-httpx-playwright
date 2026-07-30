from httpx import Response
from pydantic import BaseModel


class BaseClient:

    def __init__(self, api_client):
        self.api_client = api_client

    @staticmethod
    def assert_response_ok(response: Response):
        response.raise_for_status()

    @staticmethod
    def assert_response_and_parse(response: Response, model: type[BaseModel]) -> BaseModel:
        response.raise_for_status()
        return model.model_validate(response.json())
