from src.api.clients.base_client import BaseClient
from src.api.models.branding_models import Hotel


class BrandingClient(BaseClient):

    def get_hotel_details(self):
        response = self.api_client.get('/branding')
        return self.assert_response_and_parse(response, Hotel)
