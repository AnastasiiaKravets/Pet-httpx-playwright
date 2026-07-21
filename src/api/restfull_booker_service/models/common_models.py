from pydantic import BaseModel, ConfigDict


class StrictModel(BaseModel):
    """
    Base for all response models.
    extra="forbid" means unknown fields from the API raise ValidationError.
    """
    model_config = ConfigDict(extra="forbid", strict=False, populate_by_name=True)


class BasicErrorResponse(StrictModel):
    error: str

class BasicWarningResponse(StrictModel):
    message: str

