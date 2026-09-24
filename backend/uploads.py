import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, UploadFile

from limiter import limiter

router = APIRouter(prefix="/api", tags=["uploads"])

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB

# maps file signature (magic bytes) -> (extension, content-type). Checked against
# the actual bytes, not the client-supplied Content-Type header, which is trivial
# to spoof (e.g. curl -F "file=@payload.exe;type=image/png").
SIGNATURES = {
    b"\x89PNG\r\n\x1a\n": (".png", "image/png"),
    b"\xff\xd8\xff": (".jpg", "image/jpeg"),
}


def sniff(contents: bytes) -> str | None:
    for magic, (ext, _content_type) in SIGNATURES.items():
        if contents.startswith(magic):
            return ext
    if contents[:4] == b"RIFF" and contents[8:12] == b"WEBP":
        return ".webp"
    return None


@router.post("/upload")
@limiter.limit("10/minute")
async def upload_file(request: Request, file: UploadFile):
    contents = await file.read()
    if len(contents) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    ext = sniff(contents)
    if ext is None:
        raise HTTPException(status_code=400, detail="Unsupported file type (must be PNG, JPEG, or WEBP)")

    safe_name = f"{uuid.uuid4().hex}{ext}"
    (UPLOAD_DIR / safe_name).write_bytes(contents)

    return {"filename": safe_name, "url": f"/uploads/{safe_name}"}
