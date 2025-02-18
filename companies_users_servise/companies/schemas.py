from datetime import date

from pydantic import BaseModel, ConfigDict

from common_models.fields_validation import validate_str_9, validate_str_13, validate_str_16, validate_str_255
from property_code_dicts.schemas import PropertyCodeDictDB


class CompanyBase(BaseModel):
    name: validate_str_255
    inn: validate_str_16
    kpp: validate_str_9
    ogrn: validate_str_13 | None = None
    bic: validate_str_9 | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    name: validate_str_255 | None = None
    inn: validate_str_16 | None = None
    kpp: validate_str_9 | None = None


class CompanyDB(CompanyBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_date: date


class CompanyWithPropertiesDB(CompanyDB):
    properties: list["PropertyCodeDictDB"]
