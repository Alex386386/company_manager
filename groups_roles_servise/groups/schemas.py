from pydantic import BaseModel, ConfigDict


class GroupBase(BaseModel):
    company_id: int
    group_name: str
    comment: str | None = None


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    company_id: int | None = None
    group_name: str | None = None


class GroupDB(GroupBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
