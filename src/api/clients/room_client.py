import httpx

from src.api.clients.base_client import BaseClient
from src.api.models.common_models import BasicSuccessResponse
from src.api.models.room_models import RoomList, RoomResponse
from src.data.data_generators import get_room_payload


class RoomClient(BaseClient):
    def get_all_rooms(self) -> list[RoomResponse]:
        response = self.api_client.get("/room")
        return self.assert_response_and_parse(response, RoomList).rooms

    def available_rooms(self, date_from, date_to):
        params = dict(checkin=date_from, checkout=date_to)
        response = self.api_client.get("/room", params=params)
        return self.assert_response_and_parse(response, RoomList).rooms

    def create_room(self, room_name: str | None = None):
        payload = get_room_payload(room_name)
        response = self.api_client.post("/room", payload)
        return self.assert_response_and_parse(response, BasicSuccessResponse)

    def delete_room(self, room_id: int):
        response = self.api_client.delete(f"/room/{room_id}")
        self.assert_response_ok(response)

    def delete_room_if_exists(self, room_id: int):
        try:
            self.delete_room(room_id)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return
            raise
