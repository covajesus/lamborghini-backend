from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    id: str | None = None
    slug: str
    name: str
    line: str
    image: str
    sort_order: int = Field(default=0, ge=0)
    active: bool = True


class CategoryUpdate(BaseModel):
    slug: str | None = None
    name: str | None = None
    line: str | None = None
    image: str | None = None
    sort_order: int | None = Field(default=None, ge=0)
    active: bool | None = None


class CategoryRead(CategoryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: str
