from enum import Enum
from typing import Optional, Literal

from pydantic import PositiveInt, BaseModel
from pydantic.fields import Field


class PetStatus(str, Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"

class PetCreateModelRequest(BaseModel):
    id: PositiveInt
    name: str
    status: PetStatus = PetStatus.AVAILABLE
    photoUrls: Optional[list[str]] = []
    tags: Optional[list[str]] = []

class PetCreateModelResponse(BaseModel):
    id: PositiveInt
    name: str
    status: PetStatus
    photoUrls: list[str]
    tags: list[str]

class PetErrorResponse(BaseModel):
    code: int
    type: Literal["error"]
    message: str