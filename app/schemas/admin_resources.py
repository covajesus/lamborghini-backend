from pydantic import BaseModel, ConfigDict, EmailStr, Field


class InventoryCreate(BaseModel):
    id: str | None = None
    product_id: str
    sku: str
    warehouse: str
    quantity: int = Field(ge=0)
    reserved: int = Field(default=0, ge=0)
    average_cost: float = Field(default=0, ge=0)
    active: bool = True


class InventoryUpdate(BaseModel):
    product_id: str | None = None
    sku: str | None = None
    warehouse: str | None = None
    quantity: int | None = Field(default=None, ge=0)
    reserved: int | None = Field(default=None, ge=0)
    average_cost: float | None = Field(default=None, ge=0)
    incoming_quantity: int | None = Field(default=None, ge=0)
    unit_cost: float | None = Field(default=None, ge=0)
    active: bool | None = None


class InventoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    product_id: str
    sku: str
    warehouse: str
    quantity: int
    reserved: int = 0
    average_cost: float = 0
    active: bool = True


class PaymentCreate(BaseModel):
    id: str | None = None
    reference: str
    customer_name: str
    amount: int = Field(gt=0)
    method: str
    status: str
    paid_at: str
    active: bool = True


class PaymentUpdate(BaseModel):
    reference: str | None = None
    customer_name: str | None = None
    amount: int | None = Field(default=None, gt=0)
    method: str | None = None
    status: str | None = None
    paid_at: str | None = None
    active: bool | None = None


class PaymentRead(PaymentCreate):
    model_config = ConfigDict(from_attributes=True)
    id: str


class StaffUserCreate(BaseModel):
    id: str | None = None
    full_name: str
    email: EmailStr
    role: str
    phone: str = ""
    active: bool = True


class StaffUserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    role: str | None = None
    phone: str | None = None
    active: bool | None = None


class StaffUserRead(StaffUserCreate):
    model_config = ConfigDict(from_attributes=True)
    id: str


class RoleCreate(BaseModel):
    id: str | None = None
    key: str = Field(min_length=2, max_length=60)
    name: str = Field(min_length=2, max_length=120)
    description: str = ""
    color: str | None = None
    permissions: list[str] = Field(default_factory=list)
    is_system: bool = False
    active: bool = True


class RoleUpdate(BaseModel):
    key: str | None = Field(default=None, min_length=2, max_length=60)
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = None
    color: str | None = None
    permissions: list[str] | None = None
    active: bool | None = None


class RoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    key: str
    name: str
    description: str = ""
    color: str
    permissions: list[str] = Field(default_factory=list)
    is_system: bool = False
    active: bool = True


class PermissionRead(BaseModel):
    key: str
    label: str
    group: str


class SettingCreate(BaseModel):
    id: str | None = None
    key: str
    label: str
    value: str
    group: str = "general"
    active: bool = True


class SettingUpdate(BaseModel):
    key: str | None = None
    label: str | None = None
    value: str | None = None
    group: str | None = None
    active: bool | None = None


class SettingRead(SettingCreate):
    model_config = ConfigDict(from_attributes=True)
    id: str
