import logging
import logging.handlers
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

load_dotenv()

# Mirror uvicorn's output (requests + tracebacks) to backend/server.log so it can be
# read by tools even when the server runs in someone else's terminal window.
_log_file = logging.handlers.RotatingFileHandler(
    Path(__file__).parent / "server.log", maxBytes=2_000_000, backupCount=1, encoding="utf-8"
)
_log_file.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
for _name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
    logging.getLogger(_name).addHandler(_log_file)

import auth
import uploads
from database import Base, engine
from limiter import limiter

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

allowed_origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(uploads.router)
app.mount("/uploads", StaticFiles(directory=uploads.UPLOAD_DIR), name="uploads")


@app.get("/api/health")
def health():
    return {"status": "ok"}
