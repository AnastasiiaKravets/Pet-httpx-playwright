from pydantic import Field, EmailStr, field_validator

from src.api.models.common_models import StrictModel


class Address(StrictModel):
    county: str = Field(..., min_length=1)
    line1: str = Field(..., min_length=1)
    line2: str | None = Field(None, min_length=1)
    post_code: str = Field(..., min_length=1, alias="postCode")
    post_town: str = Field(..., min_length=1, alias="postTown")


class Contact(StrictModel):
    email: EmailStr
    name: str = Field(..., min_length=3, max_length=40)
    phone: str = Field(..., min_length=1)


class MapCoordinates(StrictModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class Hotel(StrictModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=500)
    directions: str = Field(..., min_length=1)

    logo_url: str = Field(..., alias="logoUrl")

    address: Address
    contact: Contact
    map_coords: MapCoordinates = Field(..., alias="map")

    @field_validator("logo_url")
    @classmethod
    def validate_logo_path(cls, value: str) -> str:
        if not any(value.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp", ".svg"]):
            raise ValueError("logoUrl must point to an image file (jpg, jpeg, png, webp, svg)")
        return value
