from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.entities import Audience


def _as_image_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()][:4]
    return []


class ProductOption(BaseModel):
    key: str
    label: str
    values: list[str] = Field(default_factory=list)


class ProductVariant(BaseModel):
    id: str | None = None
    attributes: dict[str, str] = Field(default_factory=dict)
    price: int | None = Field(default=None, gt=0)
    compare_at: int | None = None
    image: str | None = None
    active: bool = True


class ProductBase(BaseModel):
    slug: str
    name: str
    audience: Audience
    group: str
    type: str
    line: str
    price: int = Field(gt=0)
    description: str
    composition: str
    care: str
    image: str = ""
    images: list[str] = Field(default_factory=list)
    colors: list[str] = Field(default_factory=list)
    sizes: list[str] = Field(default_factory=list)
    options: list[ProductOption] = Field(default_factory=list)
    color_images: dict[str, list[str]] = Field(default_factory=dict)
    variants: list[ProductVariant] = Field(default_factory=list)
    featured: bool = False
    compare_at: int | None = None
    active: bool = True

    @field_validator("images", mode="before")
    @classmethod
    def validate_images(cls, value: Any) -> list[str]:
        return _as_image_list(value)

    @field_validator("color_images", mode="before")
    @classmethod
    def validate_color_images(cls, value: Any) -> dict[str, list[str]]:
        if not isinstance(value, dict):
            return {}
        return {str(key): _as_image_list(item) for key, item in value.items() if str(key).strip()}


class ProductCreate(ProductBase):
    id: str | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    price: int | None = Field(default=None, gt=0)
    description: str | None = None
    composition: str | None = None
    care: str | None = None
    image: str | None = None
    images: list[str] | None = None
    colors: list[str] | None = None
    sizes: list[str] | None = None
    options: list[ProductOption] | None = None
    color_images: dict[str, list[str]] | None = None
    variants: list[ProductVariant] | None = None
    featured: bool | None = None
    compare_at: int | None = None
    active: bool | None = None
    group: str | None = None
    type: str | None = None
    line: str | None = None
    audience: Audience | None = None

    @field_validator("images", mode="before")
    @classmethod
    def validate_images(cls, value: Any) -> list[str] | None:
        if value is None:
            return None
        return _as_image_list(value)

    @field_validator("color_images", mode="before")
    @classmethod
    def validate_color_images(cls, value: Any) -> dict[str, list[str]] | None:
        if value is None:
            return None
        if not isinstance(value, dict):
            return {}
        return {str(key): _as_image_list(item) for key, item in value.items() if str(key).strip()}


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
