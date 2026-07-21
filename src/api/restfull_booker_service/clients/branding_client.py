from src.api.restfull_booker_service.clients.base_client import BaseClient
from src.api.restfull_booker_service.models.branding_models import Hotel


class BrandingClient(BaseClient):

    def get_hotel_details(self):
        response = self.api_client.get('/branding')
        return Hotel.model_validate(response.json())
