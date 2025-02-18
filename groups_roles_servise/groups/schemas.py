from pydantic import BaseModel, ConfigDict

from common_models.fields_validation import validate_str_255, validate_str_1000


class GroupBase(BaseModel):
    company_id: int
    group_name: validate_str_255
    comment: validate_str_1000 | None = None


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    company_id: int | None = None
    group_name: validate_str_255 | None = None


class GroupDB(GroupBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
