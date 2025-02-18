from pydantic import BaseModel, ConfigDict

from common_models.fields_validation import validate_str_30, validate_str_100


class PropertyCodeDictBase(BaseModel):
    group_code: validate_str_30
    code: validate_str_30
    name: validate_str_100 | None = None


class PropertyCodeDictCreate(PropertyCodeDictBase):
    pass


class PropertyCodeDictUpdate(PropertyCodeDictBase):
    group_code: validate_str_30 | None = None
    code: validate_str_30 | None = None


class PropertyCodeDictDB(PropertyCodeDictBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
