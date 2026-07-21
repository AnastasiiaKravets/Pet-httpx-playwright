from src.api.restfull_booker_service.models.room_models import RoomList


class RoomClient:

    def __init__(self, api_client):
        self.api_client = api_client

    def get_all_rooms(self):
        response = self.api_client.get('/room')
        return RoomList.model_validate(response.json()).rooms
