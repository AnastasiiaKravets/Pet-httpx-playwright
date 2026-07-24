from src.api.clients.base_client import BaseClient
from src.api.models.booking_models import BookingListModel, BookingModelResponse
from src.data.user_data import get_booking_payload


class BookingClient(BaseClient):

    def get_all_booking_for_room(self, room_id):
        response = self.api_client.get('/booking', params={'roomid': room_id})
        return BookingListModel.model_validate(response.json()).bookings

    def create_booking(self, room_id, date_from, date_to):
        payload = get_booking_payload(room_id, date_from, date_to)
        response = self.api_client.post('/booking', payload=payload)
        return BookingModelResponse.model_validate(response.json())

    def delete_booking(self, booking_id):
        self.api_client.delete(f'/booking/{booking_id}')
