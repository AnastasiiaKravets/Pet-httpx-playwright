from enum import StrEnum

from pydantic import Field

from src.api.models.common_models import StrictModel


class RoomFeatures(StrEnum):
    WIFI = "WiFi"
    TV = "TV"
    RADIO = "Radio"
    REFRESHMENTS = "Refreshments"
    SAFE = "Safe"
    VIEWS = "Views"


class RoomType(StrEnum):
    SINGLE = "Single"
    DOUBLE = "Double"
    TWIN = "Twin"
    SUITE = "Suite"
    FAMILY = "Family"


class Room(StrictModel):
    room_name: str = Field(..., alias="roomName", min_length=1)
    type: RoomType
    accessible: bool
    room_price: int = Field(..., alias="roomPrice", gt=0)
    image: str = Field(..., min_length=1)
    description: str = Field(..., min_length=10)
    features: list[RoomFeatures]


class RoomResponse(Room):
    room_id: int = Field(..., alias="roomid")


class RoomList(StrictModel):
    rooms: list[RoomResponse]
