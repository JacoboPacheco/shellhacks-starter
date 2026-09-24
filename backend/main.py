import logging
import logging.handlers
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text

load_dotenv()

# Mirror uvicorn's output (requests + tracebacks) to backend/server.log so it can be
# read by tools even when the server runs in someone else's terminal window.
_log_file = logging.handlers.RotatingFileHandler(
    Path(__file__).parent / "server.log", maxBytes=2_000_000, backupCount=1, encoding="utf-8"
)
_log_file.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
# "uvicorn.error" propagates to "uvicorn"; attaching to both would log each line twice
for _name in ("uvicorn", "uvicorn.access"):
    logging.getLogger(_name).addHandler(_log_file)

import auth
import llm
import uploads
from database import Base, engine
from limiter import limiter

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Runs before routing and body parsing, so a huge upload is refused without being
# downloaded. Defined before CORSMiddleware is added so the 413 still gets CORS headers.
@app.middleware("http")
async def reject_oversized_uploads(request: Request, call_next):
    if request.url.path == "/api/upload":
        declared = request.headers.get("content-length", "")
        if declared.isdigit() and int(declared) > uploads.MAX_UPLOAD_BYTES + 4096:
            return JSONResponse({"detail": "File too large (max 5MB)"}, status_code=413)
    return await call_next(request)


allowed_origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(uploads.router)
app.include_router(llm.router)
app.mount("/uploads", StaticFiles(directory=uploads.UPLOAD_DIR), name="uploads")


@app.get("/api/health")
def health():
    # touches the database so a deploy with a broken DB doesn't report green
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:  # noqa: BLE001 — any DB failure should surface here
        return JSONResponse({"status": "db-error", "detail": str(e)[:200]}, status_code=503)
    return {"status": "ok"}
