from itertools import product as cartesian
from uuid import uuid4

from app.domain.entities import Product


def _option_values(option: dict) -> list[str]:
    values = option.get("values") or []
    return [str(value).strip() for value in values if str(value).strip()]


def as_image_list(value) -> list[str]:
    """
    Coerce a string or list into a max-4 image list.

    @param value: Raw image value
    @return: Clean image URLs
    """
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()][:4]
    return []


def sync_colors_and_sizes(options: list[dict]) -> tuple[list[str], list[str]]:
    """
    Derive legacy colors/sizes lists from structured options.

    @param options: Product option definitions
    @return: (colors, sizes)
    """
    colors: list[str] = []
    sizes: list[str] = []
    for option in options or []:
        key = str(option.get("key") or "").strip().lower()
        values = _option_values(option)
        if key == "color":
            colors = values
        elif key == "size":
            sizes = values
    return colors, sizes


def build_cartesian_variants(options: list[dict], existing: list[dict] | None = None) -> list[dict]:
    """
    Build sellable variant rows from option values (full matrix).

    Existing variants with the same attributes keep id/price/active.

    @param options: Option definitions
    @param existing: Previously saved variants
    @return: Variant dictionaries
    """
    axes = []
    for option in options or []:
        key = str(option.get("key") or "").strip()
        values = _option_values(option)
        if not key or not values:
            continue
        axes.append([(key, value) for value in values])

    if not axes:
        return []

    by_attrs = {}
    for item in existing or []:
        attrs = {str(k): str(v) for k, v in dict(item.get("attributes") or {}).items()}
        by_attrs[tuple(sorted(attrs.items()))] = item

    variants = []
    for combo in cartesian(*axes):
        attributes = dict(combo)
        fingerprint = tuple(sorted(attributes.items()))
        previous = by_attrs.get(fingerprint, {})
        variants.append(
            {
                "id": previous.get("id") or str(uuid4()),
                "attributes": attributes,
                "price": previous.get("price"),
                "compare_at": previous.get("compare_at"),
                "image": previous.get("image"),
                "active": previous.get("active", True) is not False,
            }
        )
    return variants


def ensure_variant_structure(product: Product) -> Product:
    """
    Ensure options/variants/images exist, deriving defaults when missing.

    @param product: Domain product
    @return: Product with options/variants/images populated
    """
    options = [dict(item) for item in (product.options or [])]
    variants = [dict(item) for item in (product.variants or [])]
    images = as_image_list(getattr(product, "images", None) or [])
    if not images and product.image:
        images = [product.image]

    color_images_raw = dict(product.color_images or {})
    color_images: dict[str, list[str]] = {
        str(key): as_image_list(value) for key, value in color_images_raw.items() if str(key).strip()
    }

    if not options:
        if product.colors:
            options.append({"key": "color", "label": "Color", "values": list(product.colors)})
        if product.sizes:
            options.append({"key": "size", "label": "Talla", "values": list(product.sizes)})

    if options and not variants:
        variants = build_cartesian_variants(options)

    colors, sizes = sync_colors_and_sizes(options)
    if not colors and product.colors:
        colors = list(product.colors)
    if not sizes and product.sizes:
        sizes = list(product.sizes)

    fallback = images[0] if images else product.image
    for color in colors:
        if color not in color_images or not color_images[color]:
            color_images[color] = [fallback] if fallback else []

    product.images = images[:4]
    product.image = product.images[0] if product.images else (product.image or "")
    product.options = options
    product.variants = variants
    product.color_images = color_images
    product.colors = colors
    product.sizes = sizes
    return product


def normalize_product_payload(
    *,
    options: list[dict] | None,
    variants: list[dict] | None,
    color_images: dict | None,
    colors: list[str] | None = None,
    sizes: list[str] | None = None,
    image: str | None = None,
    images: list[str] | None = None,
) -> dict:
    """
    Normalize option/variant/gallery payload before persistence.

    @return: Dict with options, variants, color_images, colors, sizes, images, image
    """
    clean_options = []
    for option in options or []:
        key = str(option.get("key") or "").strip().lower().replace(" ", "_")
        label = str(option.get("label") or key).strip()
        values = _option_values(option)
        if not key or not values:
            continue
        clean_options.append({"key": key, "label": label or key, "values": values})

    clean_variants = []
    for item in variants or []:
        attributes = {
            str(k).strip(): str(v).strip()
            for k, v in dict(item.get("attributes") or {}).items()
            if str(k).strip() and str(v).strip()
        }
        clean_variants.append(
            {
                "id": str(item.get("id") or uuid4()),
                "attributes": attributes,
                "price": item.get("price"),
                "compare_at": item.get("compare_at"),
                "image": item.get("image"),
                "active": item.get("active", True) is not False,
            }
        )

    if clean_options and not clean_variants:
        clean_variants = build_cartesian_variants(clean_options)

    derived_colors, derived_sizes = sync_colors_and_sizes(clean_options)
    clean_colors = derived_colors or list(colors or [])
    clean_sizes = derived_sizes or list(sizes or [])

    clean_gallery = as_image_list(images if images is not None else [])
    if not clean_gallery and image:
        clean_gallery = as_image_list(image)

    clean_color_images: dict[str, list[str]] = {}
    for key, value in dict(color_images or {}).items():
        label = str(key).strip()
        urls = as_image_list(value)
        if label and urls:
            clean_color_images[label] = urls

    primary = clean_gallery[0] if clean_gallery else (image or "")
    for color in clean_colors:
        if color not in clean_color_images and primary:
            clean_color_images[color] = [primary]

    return {
        "options": clean_options,
        "variants": clean_variants,
        "color_images": clean_color_images,
        "colors": clean_colors,
        "sizes": clean_sizes,
        "images": clean_gallery[:4],
        "image": primary or "",
    }
