from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    """
    Base for all response models.
    extra="forbid" means unknown fields from the API raise ValidationError.
    """
    model_config = ConfigDict(extra="forbid", strict=False, populate_by_name=True)


class BasicErrorResponse(StrictModel):
    message: str

class PaginatedStrictModel(StrictModel):
    total: int = Field(ge=0)
    skip: int = Field(ge=0)
    limit: int = Field(ge=0)

class DeletedResponseModel(StrictModel):
    isDeleted: bool
    deletedOn: datetime