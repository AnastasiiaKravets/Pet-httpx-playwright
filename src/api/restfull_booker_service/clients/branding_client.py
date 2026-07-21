from src.api.restfull_booker_service.models.branding_models import Hotel


class BrandingClient:

    def __init__(self, api_client):
        self.api_client = api_client

    def get_hotel_details(self):
        response = self.api_client.get('/branding')
        return Hotel.model_validate(response.json())
