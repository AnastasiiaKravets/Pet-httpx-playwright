from typing import Literal, List, Optional

from pydantic import Field, HttpUrl, EmailStr, IPvAnyAddress, PositiveInt, PositiveFloat

from src.api.dummy_json_service.models.common_models import StrictModel, PaginatedStrictModel, DeletedResponseModel


class Hair(StrictModel):
    color: str
    type: str


class Coordinates(StrictModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class Address(StrictModel):
    address: str
    city: str
    state: str
    state_code: str = Field(..., alias="stateCode")
    postal_code: str = Field(..., alias="postalCode")
    coordinates: Coordinates
    country: str


class Bank(StrictModel):
    card_expire: str = Field(..., alias="cardExpire")
    card_number: str = Field(..., alias="cardNumber")
    card_type: str = Field(..., alias="cardType")
    currency: str
    iban: str


class Company(StrictModel):
    department: str
    name: str
    title: str
    address: Address


class Crypto(StrictModel):
    coin: str
    wallet: str
    network: str


class UserResponse(StrictModel):
    id: PositiveInt
    first_name: str = Field(..., alias="firstName", min_length=1)
    last_name: str = Field(..., alias="lastName", min_length=1)
    maiden_name: Optional[str] = Field(None, alias="maidenName")
    age: int = Field(..., ge=0, le=120)
    gender: Literal["female", "male", "other"]
    email: EmailStr
    phone: str
    username: str = Field(..., min_length=3)
    password: str
    birth_date: str = Field(..., alias="birthDate")
    image: HttpUrl
    blood_group: str = Field(..., alias="bloodGroup")
    height: PositiveFloat
    weight: PositiveFloat
    eye_color: str = Field(..., alias="eyeColor")
    hair: Hair
    ip: IPvAnyAddress
    address: Address
    mac_address: str = Field(..., alias="macAddress")
    university: str
    bank: Bank
    company: Company
    ein: str
    ssn: str
    user_agent: str = Field(..., alias="userAgent")
    crypto: Crypto
    role: Literal["admin", "user", "moderator"]

class UserListResponse(PaginatedStrictModel):
    users: List[UserResponse]

class DeletedUserResponse(UserResponse, DeletedResponseModel):
    pass