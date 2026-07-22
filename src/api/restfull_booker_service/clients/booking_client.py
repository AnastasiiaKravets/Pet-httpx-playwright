from src.api.restfull_booker_service.clients.base_client import BaseClient
from src.api.restfull_booker_service.models.booking_models import BookingListModel


class BookingClient(BaseClient):

    def get_all_booking_for_room(self, room_id):
        response = self.api_client.get('/booking', params={'roomid': room_id})
        print(response.json())
        return BookingListModel.model_validate(response.json()).bookings

    def create_booking(self):
        pass

    def delete_booking(self, booking_id):
        self.api_client.delete(f'/booking/{booking_id}')
