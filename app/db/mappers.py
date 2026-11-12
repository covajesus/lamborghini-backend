from app.db.models import (
    AdminUserModel,
    CategoryModel,
    InventoryItemModel,
    PaymentModel,
    ProductModel,
    RoleModel,
    SettingModel,
    SlideModel,
    StaffUserModel,
)
from app.domain.entities import (
    AdminUser,
    Audience,
    Category,
    InventoryItem,
    Payment,
    Product,
    Role,
    Setting,
    Slide,
    StaffUser,
)
from app.services.product_variants import as_image_list, ensure_variant_structure


def product_to_entity(row: ProductModel) -> Product:
    """
    @param row: ORM product row
    @return: Domain Product
    """
    raw_color_images = dict(getattr(row, "color_images", None) or {})
    product = Product(
        id=row.id,
        slug=row.slug,
        name=row.name,
        audience=Audience(row.audience),
        group=row.group_name,
        type=row.type,
        line=row.line,
        price=row.price,
        description=row.description,
        composition=row.composition,
        care=row.care,
        image=row.image,
        images=as_image_list(getattr(row, "images", None) or []),
        colors=list(row.colors or []),
        sizes=list(row.sizes or []),
        options=list(getattr(row, "options", None) or []),
        color_images={str(key): as_image_list(value) for key, value in raw_color_images.items()},
        variants=list(getattr(row, "variants", None) or []),
        featured=row.featured,
        compare_at=row.compare_at,
        active=row.active,
    )
    return ensure_variant_structure(product)


def product_to_model(entity: Product) -> ProductModel:
    """
    @param entity: Domain Product
    @return: ORM product row
    """
    normalized = ensure_variant_structure(entity)
    return ProductModel(
        id=normalized.id,
        slug=normalized.slug,
        name=normalized.name,
        audience=normalized.audience.value if isinstance(normalized.audience, Audience) else str(normalized.audience),
        group_name=normalized.group,
        type=normalized.type,
        line=normalized.line,
        price=normalized.price,
        description=normalized.description,
        composition=normalized.composition,
        care=normalized.care,
        image=normalized.image,
        images=list(normalized.images),
        colors=list(normalized.colors),
        sizes=list(normalized.sizes),
        options=list(normalized.options),
        color_images=dict(normalized.color_images),
        variants=list(normalized.variants),
        featured=normalized.featured,
        compare_at=normalized.compare_at,
        active=normalized.active,
    )


def admin_to_entity(row: AdminUserModel) -> AdminUser:
    """
    @param row: ORM admin user row
    @return: Domain AdminUser
    """
    return AdminUser(
        id=row.id,
        email=row.email,
        full_name=row.full_name,
        hashed_password=row.hashed_password,
        role=row.role,
    )


def admin_to_model(entity: AdminUser) -> AdminUserModel:
    """
    @param entity: Domain AdminUser
    @return: ORM admin user row
    """
    return AdminUserModel(
        id=entity.id,
        email=entity.email,
        full_name=entity.full_name,
        hashed_password=entity.hashed_password,
        role=entity.role,
    )


def inventory_to_entity(row: InventoryItemModel) -> InventoryItem:
    """
    @param row: ORM inventory row
    @return: Domain InventoryItem
    """
    return InventoryItem(
        id=row.id,
        product_id=row.product_id,
        sku=row.sku,
        warehouse=row.warehouse,
        quantity=row.quantity,
        reserved=row.reserved,
        average_cost=float(row.average_cost or 0),
        active=row.active,
    )


def inventory_to_model(entity: InventoryItem) -> InventoryItemModel:
    """
    @param entity: Domain InventoryItem
    @return: ORM inventory row
    """
    return InventoryItemModel(
        id=entity.id,
        product_id=entity.product_id,
        sku=entity.sku,
        warehouse=entity.warehouse,
        quantity=entity.quantity,
        reserved=entity.reserved,
        average_cost=float(entity.average_cost or 0),
        active=entity.active,
    )


def payment_to_entity(row: PaymentModel) -> Payment:
    """
    @param row: ORM payment row
    @return: Domain Payment
    """
    return Payment(
        id=row.id,
        reference=row.reference,
        customer_name=row.customer_name,
        amount=row.amount,
        method=row.method,
        status=row.status,
        paid_at=row.paid_at,
        active=row.active,
    )


def payment_to_model(entity: Payment) -> PaymentModel:
    """
    @param entity: Domain Payment
    @return: ORM payment row
    """
    return PaymentModel(
        id=entity.id,
        reference=entity.reference,
        customer_name=entity.customer_name,
        amount=entity.amount,
        method=entity.method,
        status=entity.status,
        paid_at=entity.paid_at,
        active=entity.active,
    )


def staff_to_entity(row: StaffUserModel) -> StaffUser:
    """
    @param row: ORM staff user row
    @return: Domain StaffUser
    """
    return StaffUser(
        id=row.id,
        full_name=row.full_name,
        email=row.email,
        role=row.role,
        phone=row.phone,
        active=row.active,
    )


def staff_to_model(entity: StaffUser) -> StaffUserModel:
    """
    @param entity: Domain StaffUser
    @return: ORM staff user row
    """
    return StaffUserModel(
        id=entity.id,
        full_name=entity.full_name,
        email=entity.email,
        role=entity.role,
        phone=entity.phone,
        active=entity.active,
    )


def role_to_entity(row: RoleModel) -> Role:
    """
    @param row: ORM role row
    @return: Domain Role
    """
    return Role(
        id=row.id,
        key=row.key,
        name=row.name,
        description=row.description or "",
        color=row.color,
        permissions=list(row.permissions or []),
        is_system=bool(row.is_system),
        active=bool(row.active),
    )


def role_to_model(entity: Role) -> RoleModel:
    """
    @param entity: Domain Role
    @return: ORM role row
    """
    return RoleModel(
        id=entity.id,
        key=entity.key,
        name=entity.name,
        description=entity.description,
        color=entity.color,
        permissions=list(entity.permissions or []),
        is_system=entity.is_system,
        active=entity.active,
    )


def setting_to_entity(row: SettingModel) -> Setting:
    """
    @param row: ORM setting row
    @return: Domain Setting
    """
    return Setting(
        id=row.id,
        key=row.key,
        label=row.label,
        value=row.value,
        group=row.group_name,
        active=row.active,
    )


def setting_to_model(entity: Setting) -> SettingModel:
    """
    @param entity: Domain Setting
    @return: ORM setting row
    """
    return SettingModel(
        id=entity.id,
        key=entity.key,
        label=entity.label,
        value=entity.value,
        group_name=entity.group,
        active=entity.active,
    )


def slide_to_entity(row: SlideModel) -> Slide:
    """
    @param row: ORM slide row
    @return: Domain Slide
    """
    return Slide(
        id=row.id,
        sort_order=row.sort_order,
        kicker=row.kicker,
        title=row.title,
        text=row.text,
        cta_label=row.cta_label,
        cta_to=row.cta_to,
        image=row.image,
        image_position=row.image_position,
        active=row.active,
    )


def slide_to_model(entity: Slide) -> SlideModel:
    """
    @param entity: Domain Slide
    @return: ORM slide row
    """
    return SlideModel(
        id=entity.id,
        sort_order=entity.sort_order,
        kicker=entity.kicker,
        title=entity.title,
        text=entity.text,
        cta_label=entity.cta_label,
        cta_to=entity.cta_to,
        image=entity.image,
        image_position=entity.image_position,
        active=entity.active,
    )


def category_to_entity(row: CategoryModel) -> Category:
    """
    @param row: ORM category row
    @return: Domain Category
    """
    return Category(
        id=row.id,
        slug=row.slug,
        name=row.name,
        line=row.line,
        image=row.image,
        sort_order=row.sort_order,
        active=row.active,
    )


def category_to_model(entity: Category) -> CategoryModel:
    """
    @param entity: Domain Category
    @return: ORM category row
    """
    return CategoryModel(
        id=entity.id,
        slug=entity.slug,
        name=entity.name,
        line=entity.line,
        image=entity.image,
        sort_order=entity.sort_order,
        active=entity.active,
    )
