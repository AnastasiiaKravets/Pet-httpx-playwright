from typing import Literal, List

from pydantic import Field

from src.api.restfull_booker_service.models.common_models import StrictModel


class Room(StrictModel):
    room_id: int = Field(..., alias="roomid")
    room_name: str = Field(..., alias="roomName", min_length=1)
    type: Literal["Single", "Double", "Twin", "Suite", "Family"]
    accessible: bool
    room_price: int = Field(..., alias="roomPrice", gt=0)
    image: str = Field(..., min_length=1)
    description: str = Field(..., min_length=10)
    features: List[str]


class RoomList(StrictModel):
    rooms: List[Room]
