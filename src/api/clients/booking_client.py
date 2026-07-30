from src.api.clients.base_client import BaseClient
from src.api.models.booking_models import BookingListModelResponse, BookingModelResponse
from src.data.data_generators import get_booking_payload


class BookingClient(BaseClient):

    def get_all_booking_for_room(self, room_id):
        response = self.api_client.get('/booking', params={'roomid': room_id})
        return self.assert_response_and_parse(response, BookingListModelResponse).bookings

    def create_booking(self, room_id, date_from, date_to):
        payload = get_booking_payload(room_id, date_from, date_to)
        response = self.api_client.post('/booking', payload=payload)
        return self.assert_response_and_parse(response, BookingModelResponse)

    def delete_booking(self, booking_id):
        response = self.api_client.delete(f'/booking/{booking_id}')
        self.assert_response_ok(response)
