from pydantic import BaseModel, ConfigDict, Field


class SlideCreate(BaseModel):
    id: str | None = None
    sort_order: int = Field(default=0, ge=0)
    kicker: str
    title: str
    text: str
    cta_label: str = "Descubrir"
    cta_to: str
    image: str
    image_position: str = "center center"
    active: bool = True


class SlideUpdate(BaseModel):
    sort_order: int | None = Field(default=None, ge=0)
    kicker: str | None = None
    title: str | None = None
    text: str | None = None
    cta_label: str | None = None
    cta_to: str | None = None
    image: str | None = None
    image_position: str | None = None
    active: bool | None = None


class SlideRead(SlideCreate):
    model_config = ConfigDict(from_attributes=True)
    id: str
