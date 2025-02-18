from datetime import time

from pydantic import BaseModel, ConfigDict

from common_models.fields_validation import validate_str_255


class TimezoneDictBase(BaseModel):
    timezone_name: validate_str_255 | None = None
    timezone: time | None = None


class TimezoneDictCreate(TimezoneDictBase):
    pass


class TimezoneDictUpdate(TimezoneDictBase):
    pass


class TimezoneDictDB(TimezoneDictBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
