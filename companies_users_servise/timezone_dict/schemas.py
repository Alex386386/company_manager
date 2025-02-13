from datetime import time

from pydantic import BaseModel, ConfigDict


class TimezoneDictBase(BaseModel):
    timezone_name: str | None = None
    timezone: time | None = None


class TimezoneDictCreate(TimezoneDictBase):
    pass


class TimezoneDictUpdate(TimezoneDictBase):
    pass


class TimezoneDictDB(TimezoneDictBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
