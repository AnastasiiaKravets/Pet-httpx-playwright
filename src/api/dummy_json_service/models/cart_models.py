from typing import List, Optional

from pydantic import HttpUrl, Field, PositiveFloat

from src.api.dummy_json_service.models.common_models import StrictModel, PaginatedStrictModel, DeletedResponseModel


class CartListResponse(PaginatedStrictModel):
    carts: List[CartResponse]


class CartProduct(StrictModel):
    id: int
    title: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    total: float = Field(..., gt=0)
    discount_percentage: float = Field(alias="discountPercentage", ge=0, le=100)
    discountedPrice: Optional[float] = Field(None, alias="discountedPrice", ge=0)
    discounted_total: Optional[float] = Field(None, alias="discountedTotal", ge=0)
    thumbnail: HttpUrl


class CartResponse(StrictModel):
    id: int
    products: list[CartProduct]
    total: PositiveFloat
    discounted_total: float = Field(alias="discountedTotal", ge=0)
    user_id: int = Field(alias="userId")
    total_products: int = Field(alias="totalProducts", ge=0)
    total_quantity: int = Field(alias="totalQuantity", ge=0)


class DeletedCartResponse(CartResponse, DeletedResponseModel):
    pass


class CartUpdateRequest(StrictModel):
    user_id: int | None = Field(None, alias="userId")
    merge: bool | None = None
    products: List[CartUpdateProduct]


class CartUpdateProduct(StrictModel):
    id: int
    quantity: int
