from app.domain.entities import Audience, Product
from app.services.product_variants import build_cartesian_variants, ensure_variant_structure, normalize_product_payload


def test_build_cartesian_variants_supports_sparse_edit() -> None:
    options = [
        {"key": "color", "label": "Color", "values": ["Azul", "Negro"]},
        {"key": "size", "label": "Talla", "values": ["Única", "M"]},
    ]
    variants = build_cartesian_variants(options)
    assert len(variants) == 4
    sparse = [item for item in variants if item["attributes"] != {"color": "Negro", "size": "M"}]
    assert len(sparse) == 3


def test_normalize_derives_colors_sizes_and_color_images() -> None:
    payload = normalize_product_payload(
        options=[{"key": "color", "label": "Color", "values": ["Azul"]}],
        variants=[{"attributes": {"color": "Azul"}, "active": True}],
        color_images={},
        image="/media/products/x.jpg",
    )
    assert payload["colors"] == ["Azul"]
    assert payload["color_images"]["Azul"] == ["/media/products/x.jpg"]
    assert payload["images"] == ["/media/products/x.jpg"]


def test_ensure_variant_structure_from_legacy_lists() -> None:
    product = Product(
        id="p1",
        slug="p1",
        name="P1",
        audience=Audience.MEN,
        group="Calzado",
        type="Zapatillas",
        line="footwear",
        price=1000,
        description="d",
        composition="c",
        care="care",
        image="/media/a.jpg",
        colors=["Negro"],
        sizes=["40", "41"],
    )
    ensured = ensure_variant_structure(product)
    assert len(ensured.options) == 2
    assert len(ensured.variants) == 2
    assert ensured.color_images["Negro"] == ["/media/a.jpg"]
    assert ensured.images == ["/media/a.jpg"]
