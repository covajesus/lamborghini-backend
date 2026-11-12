from app.domain.entities import Category, InventoryItem, Payment, Role, Setting, Slide, StaffUser
from app.domain.permissions import ALL_PERMISSION_KEYS


def seed_inventory() -> list[InventoryItem]:
    return [
        InventoryItem(
            id="inv-1",
            product_id="cap-02",
            sku="LB-H02-01",
            warehouse="Santiago",
            quantity=42,
            reserved=3,
            average_cost=18500,
        ),
        InventoryItem(
            id="inv-2",
            product_id="cap-01",
            sku="LB-H-CREAM",
            warehouse="Santiago",
            quantity=28,
            reserved=1,
            average_cost=21000,
        ),
        InventoryItem(
            id="inv-3",
            product_id="sn-01",
            sku="LB-SN-CREAM",
            warehouse="Viña del Mar",
            quantity=15,
            reserved=2,
            average_cost=42000,
        ),
        InventoryItem(
            id="inv-4",
            product_id="bx-01",
            sku="LB-BX-6PACK",
            warehouse="Santiago",
            quantity=60,
            reserved=8,
            average_cost=12500,
        ),
    ]


def seed_payments() -> list[Payment]:
    return [
        Payment(
            id="pay-1",
            reference="ORD-10021",
            customer_name="Camila Rojas",
            amount=189000,
            method="Webpay",
            status="paid",
            paid_at="2026-11-02",
        ),
        Payment(
            id="pay-2",
            reference="ORD-10022",
            customer_name="Diego Muñoz",
            amount=99000,
            method="Transferencia",
            status="pending",
            paid_at="2026-11-05",
        ),
        Payment(
            id="pay-3",
            reference="ORD-10023",
            customer_name="Ana Pérez",
            amount=129000,
            method="Webpay",
            status="paid",
            paid_at="2026-11-06",
        ),
    ]


def seed_staff_users() -> list[StaffUser]:
    return [
        StaffUser(id="staff-1", full_name="Store Admin", email="admin@example.com", role="admin", phone="+56 9 1111 1111"),
        StaffUser(id="staff-2", full_name="Valentina Soto", email="valentina@example.com", role="editor", phone="+56 9 2222 2222"),
        StaffUser(id="staff-3", full_name="Mateo Silva", email="mateo@example.com", role="viewer", phone="+56 9 3333 3333", active=False),
    ]


def seed_roles() -> list[Role]:
    editor_permissions = [
        "dashboard.view",
        "products.read",
        "products.write",
        "categories.read",
        "categories.write",
        "slides.read",
        "slides.write",
        "inventory.read",
        "inventory.write",
        "payments.read",
        "payments.write",
    ]
    viewer_permissions = [
        "dashboard.view",
        "products.read",
        "categories.read",
        "slides.read",
        "inventory.read",
        "payments.read",
    ]
    return [
        Role(
            id="role-admin",
            key="admin",
            name="Admin",
            description="Acceso total al administrador: usuarios, roles, catálogo y configuraciones.",
            color="#B8860B",
            permissions=list(ALL_PERMISSION_KEYS),
            is_system=True,
            active=True,
        ),
        Role(
            id="role-editor",
            key="editor",
            name="Editor",
            description="Puede gestionar catálogo, slider, inventario y pagos. Sin acceso a usuarios ni roles.",
            color="#2F5D50",
            permissions=editor_permissions,
            is_system=True,
            active=True,
        ),
        Role(
            id="role-viewer",
            key="viewer",
            name="Viewer",
            description="Solo lectura en catálogo, inventario y pagos. No puede crear ni editar.",
            color="#5B6B7A",
            permissions=viewer_permissions,
            is_system=True,
            active=True,
        ),
    ]


def seed_settings() -> list[Setting]:
    return [
        Setting(id="set-1", key="store_name", label="Nombre de tienda", value="Lamborghini Colección", group="general"),
        Setting(id="set-2", key="currency", label="Moneda", value="CLP", group="general"),
        Setting(id="set-3", key="free_shipping_from", label="Despacho gratis desde", value="250000", group="shipping"),
        Setting(id="set-4", key="support_email", label="Correo soporte", value="soporte@example.com", group="contact"),
        Setting(
            id="set-social-instagram",
            key="social_instagram",
            label="Instagram",
            value="https://www.instagram.com/lamborghini/",
            group="social",
        ),
        Setting(
            id="set-social-facebook",
            key="social_facebook",
            label="Facebook",
            value="https://www.facebook.com/Lamborghini/",
            group="social",
        ),
        Setting(
            id="set-social-tiktok",
            key="social_tiktok",
            label="TikTok",
            value="https://www.tiktok.com/@lamborghini",
            group="social",
        ),
        Setting(
            id="set-social-youtube",
            key="social_youtube",
            label="YouTube",
            value="https://www.youtube.com/user/Lamborghini",
            group="social",
        ),
        Setting(
            id="set-social-x",
            key="social_x",
            label="X (Twitter)",
            value="https://x.com/Lamborghini",
            group="social",
        ),
    ]


def seed_slides() -> list[Slide]:
    return [
        Slide(
            id="slide-1",
            sort_order=1,
            kicker="Lamborghini",
            title="MISMA\nACTITUD",
            text="Gorras, zapatillas y el escudo en la calle.",
            cta_label="Descubrir",
            cta_to="/shop/accessories",
            image="/media/slider-1.jpg",
            image_position="center center",
        ),
        Slide(
            id="slide-2",
            sort_order=2,
            kicker="Lamborghini",
            title="ITALIAN\nDESIGN",
            text="Premium Caps Collection. Ajuste metálico y malla técnica.",
            cta_label="Descubrir",
            cta_to="/collection/caps",
            image="/media/slider-2.jpg",
            image_position="center 42%",
        ),
        Slide(
            id="slide-3",
            sort_order=3,
            kicker="Lamborghini",
            title="PASO\nFIRME",
            text="Zapatillas coordinadas con cada colorway de gorra.",
            cta_label="Descubrir",
            cta_to="/collection/footwear",
            image="/media/slider-3.jpg",
            image_position="center 40%",
        ),
        Slide(
            id="slide-4",
            sort_order=4,
            kicker="Lamborghini",
            title="SEIS\nLEYENDAS",
            text="Pack 6 boxer trunk. Aventador a Sián.",
            cta_label="Descubrir",
            cta_to="/collection/icons",
            image="/media/slider-4.jpg",
            image_position="65% center",
        ),
    ]


def seed_categories() -> list[Category]:
    return [
        Category(
            id="cat-men",
            slug="men",
            name="Hombre",
            line="Calzado, ropa interior y lifestyle de pista.",
            image="/media/products/prod-sneaker-cream.jpg",
            sort_order=1,
        ),
        Category(
            id="cat-women",
            slug="women",
            name="Mujer",
            line="Zapatillas y gorras de la colección lifestyle.",
            image="/media/products/prod-sneaker-white.jpg",
            sort_order=2,
        ),
        Category(
            id="cat-accessories",
            slug="accessories",
            name="Accesorios",
            line="Gorras premium: Italian Design, ajuste metálico y escudo.",
            image="/media/products/prod-cap-cream.jpg",
            sort_order=3,
        ),
    ]
