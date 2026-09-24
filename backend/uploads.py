import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, UploadFile

from limiter import limiter

router = APIRouter(prefix="/api", tags=["uploads"])

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/webp"}
MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB


@router.post("/upload")
@limiter.limit("10/minute")
async def upload_file(request: Request, file: UploadFile):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    contents = await file.read()
    if len(contents) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    ext = Path(file.filename or "").suffix
    safe_name = f"{uuid.uuid4().hex}{ext}"
    (UPLOAD_DIR / safe_name).write_bytes(contents)

    return {"filename": safe_name}
