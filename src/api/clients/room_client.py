from src.api.clients.base_client import BaseClient
from src.api.models.room_models import RoomList
from src.data.data_generators import get_room_payload


class RoomClient(BaseClient):

    def get_all_rooms(self):
        response = self.api_client.get('/room')
        return RoomList.model_validate(response.json()).rooms

    def available_rooms(self, date_from, date_to):
        params = dict(checkin=date_from,
                      checkout=date_to)
        response = self.api_client.get('/room', params=params)
        return RoomList.model_validate(response.json()).rooms

    def create_room(self):
        payload = get_room_payload()
        response = self.api_client.post('/room', payload)
