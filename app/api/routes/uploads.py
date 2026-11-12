from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.api.deps import get_current_admin

router = APIRouter(prefix="/uploads", tags=["uploads"])

UPLOAD_ROOT = Path(__file__).resolve().parents[3] / "uploads"
ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    folder: str = "categories",
    _: object = Depends(get_current_admin),
) -> dict[str, str]:
    """
    Upload an image and return its public media path.

    @param file: Multipart image file
    @param folder: Destination folder under uploads/
    @return: Dict with public url
    """
    content_type = file.content_type or ""
    extension = ALLOWED_TYPES.get(content_type)
    if not extension:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato no permitido. Usa JPG, PNG, WEBP o GIF.",
        )

    safe_folder = "".join(ch for ch in folder if ch.isalnum() or ch in {"-", "_"}) or "misc"
    target_dir = UPLOAD_ROOT / safe_folder
    target_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4().hex}{extension}"
    destination = target_dir / filename
    payload = await file.read()
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Archivo vacío")
    destination.write_bytes(payload)

    return {"url": f"/media/uploads/{safe_folder}/{filename}"}
