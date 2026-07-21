from datetime import datetime
from typing import List, Literal

from pydantic import Field, EmailStr, PositiveFloat

from src.api.dummy_json_service.models.common_models import StrictModel, PaginatedStrictModel, DeletedResponseModel


class Dimensions(StrictModel):
    width: PositiveFloat
    height: PositiveFloat
    depth: PositiveFloat


class Review(StrictModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=1)
    date: datetime
    reviewer_name: str = Field(..., alias="reviewerName")
    reviewer_email: EmailStr = Field(..., alias="reviewerEmail")


class ProductMeta(StrictModel):
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    barcode: str = Field(..., min_length=1)
    qr_code: str = Field(..., alias="qrCode")


class ProductResponse(StrictModel):
    id: int
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    category: str
    price: PositiveFloat
    discount_percentage: float = Field(..., alias="discountPercentage", ge=0, le=100)
    rating: float = Field(..., ge=0, le=5)
    stock: int = Field(..., ge=0)
    tags: List[str] = Field(..., min_length=1)
    brand: str | None = None
    sku: str = Field(..., min_length=1)
    weight: float = Field(..., gt=0)
    dimensions: Dimensions
    warranty_information: str = Field(..., alias="warrantyInformation")
    shipping_information: str = Field(..., alias="shippingInformation")
    availability_status: Literal["In Stock", "Low Stock", "Out of Stock"] = Field(..., alias="availabilityStatus")
    reviews: List[Review]
    return_policy: str = Field(..., alias="returnPolicy")
    minimum_order_quantity: int = Field(..., alias="minimumOrderQuantity", gt=0)
    meta: ProductMeta
    thumbnail: str
    images: List[str]


class ProductListResponse(PaginatedStrictModel):
    products: List[ProductResponse]

class DeletedProductResponse(ProductResponse, DeletedResponseModel):
    pass