from datetime import date

from pydantic import BaseModel, ConfigDict

from property_code_dicts.schemas import PropertyCodeDictDB


class CompanyBase(BaseModel):
    name: str
    inn: str
    kpp: str
    ogrn: str | None = None
    bic: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    name: str | None = None
    inn: str | None = None
    kpp: str | None = None


class CompanyDB(CompanyBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_date: date


class CompanyWithPropertiesDB(CompanyDB):
    properties: list["PropertyCodeDictDB"]
