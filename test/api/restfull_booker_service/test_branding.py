import pytest

from src.api.restfull_booker_service.models.branding_models import Hotel


@pytest.mark.api
def test_get_branding_info(api_client):
    response = api_client.get("/branding")

    assert response.status_code == 200
    Hotel.model_validate(response.json())
