"""
LLM helper (Gemini, free tier). Usage from any router:

    from llm import complete
    text = await complete("Summarize this: ...", system="You are terse.")
    data = await complete(prompt, json_mode=True)   # returns a JSON string
    text = await complete(prompt, fallback="(AI offline) Here's an example answer…")  # never raises
    text = await complete("List the questions on this whiteboard", image=(png_bytes, "image/png"))

Needs GEMINI_API_KEY in backend/.env (free key: https://aistudio.google.com/apikey).
Without it every call raises a clear 503 so the feature can be built and demoed
as "not configured" instead of crashing. Swap providers by rewriting `complete`
only — nothing else in the app knows which model is behind it.
"""

import asyncio
import base64
import http.client
import json
import os
import urllib.error
import urllib.request

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from auth import get_current_user
from limiter import global_key, limiter
from models import User

API_BASE = os.getenv("GEMINI_API_BASE", "https://generativelanguage.googleapis.com/v1beta").rstrip("/")
# Whole-app cap on AI calls per day, across all users. The demo account is public,
# so a per-IP limit alone can't protect the free quota from one person with a loop.
# Put this decorator on every route that calls complete().
AI_DAILY_LIMIT = os.getenv("AI_DAILY_LIMIT", "400/day")
AI_QUOTA_MESSAGE = "AI quota for today is used up — try again tomorrow"
# Flash-Lite: the free tier allows ~500 requests/day on Lite models vs ~20/day on
# full Flash (as of Sept 2026) — a demo needs the 500. Override with GEMINI_MODEL.
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
TIMEOUT_SECONDS = 60

router = APIRouter(prefix="/api/ai", tags=["ai"])


def configured() -> bool:
    return bool(os.getenv("GEMINI_API_KEY"))


def _post_json(url: str, body: dict, key: str) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        return json.loads(resp.read())


async def complete(
    prompt: str,
    system: str | None = None,
    json_mode: bool = False,
    fallback: str | None = None,
    image: tuple[bytes, str] | None = None,
) -> str:
    """`fallback`: a canned answer to return instead of raising if the AI is
    unconfigured, out of quota, or unreachable — so a demo survives a dead API.
    Callers should show that it's a fallback (e.g. an "offline" badge).
    `image`: (bytes, mime_type) to send alongside the prompt, e.g. the `contents`
    from an upload — Gemini reads photos, screenshots, whiteboards, receipts."""
    try:
        return await _complete(prompt, system, json_mode, image)
    except HTTPException:
        if fallback is not None:
            return fallback
        raise


async def _complete(prompt: str, system: str | None, json_mode: bool, image: tuple[bytes, str] | None) -> str:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise HTTPException(
            status_code=503,
            detail="AI is not configured: add GEMINI_API_KEY to backend/.env (free key at aistudio.google.com/apikey)",
        )

    parts: list[dict] = []
    if image is not None:
        data, mime_type = image
        parts.append({"inline_data": {"mime_type": mime_type, "data": base64.b64encode(data).decode()}})
    parts.append({"text": prompt})
    body: dict = {"contents": [{"parts": parts}]}
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    if json_mode:
        body["generationConfig"] = {"responseMimeType": "application/json"}

    url = f"{API_BASE}/models/{MODEL}:generateContent"
    try:
        data = await asyncio.to_thread(_post_json, url, body, key)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:300]
        raise HTTPException(status_code=502, detail=f"AI request failed ({e.code}): {detail}")
    except (urllib.error.URLError, OSError, ValueError, http.client.HTTPException) as e:
        # URLError: unreachable; OSError: dropped connection; ValueError: non-JSON reply;
        # HTTPException: truncated or malformed reply
        raise HTTPException(status_code=502, detail=f"AI request failed: {e}")

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        raise HTTPException(status_code=502, detail="AI returned no text (empty or blocked response)")


class AskRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=8000)


@router.get("/status")
def status():
    return {"configured": configured(), "model": MODEL}


# Example route — copy this shape for real features: auth required, per-visitor
# rate limit, AND the shared daily cap (both decorators).
@router.post("/ask")
@limiter.limit("30/minute")
@limiter.limit(AI_DAILY_LIMIT, key_func=global_key, error_message=AI_QUOTA_MESSAGE)
async def ask(request: Request, body: AskRequest, user: User = Depends(get_current_user)):
    return {"text": await complete(body.prompt)}
