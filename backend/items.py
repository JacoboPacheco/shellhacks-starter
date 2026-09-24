"""
EXAMPLE FEATURE — the shape every feature in this app follows. Copy it for the
walking skeleton, then delete or rename it once the real feature exists:

    model in models.py  ->  this router  ->  smoke checks in smoke_test.py
    ->  demo rows in seed.py  ->  the panel in frontend/src/ItemsPanel.jsx

It shows: auth on every route, a per-visitor rate limit on the POST, an AI call
that falls back instead of failing (and tells the UI it did), owner-only access,
and input validation with limits.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from limiter import limiter
from llm import complete_json
from models import Item, User

router = APIRouter(tags=["items"])

# The fallback is a distinct object, so `result is NO_TAGS` tells us the AI didn't answer.
NO_TAGS: dict = {"tags": []}


class ItemIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    notes: str = Field("", max_length=2000)


def serialize(item: Item, fallback: bool = False) -> dict:
    return {
        "id": item.id,
        "title": item.title,
        "notes": item.notes,
        "tags": [t for t in item.tags.split(",") if t],
        "fallback": fallback,
    }


async def suggest_tags(title: str, notes: str) -> tuple[list[str], bool]:
    """Up to 3 short tags from the AI; ([], True) when it's unconfigured, out of
    quota, or unreachable — the item still saves."""
    result = await complete_json(
        f"Suggest up to 3 short lowercase tags for this item.\nTitle: {title}\nNotes: {notes}\n"
        'Answer as {"tags": ["..."]}.',
        fallback=NO_TAGS,
    )
    if result is NO_TAGS:
        return [], True
    tags = result.get("tags") if isinstance(result, dict) else None
    if not isinstance(tags, list):
        return [], True
    return [str(t).strip().lower()[:24] for t in tags if str(t).strip()][:3], False


@router.get("/api/items")
def list_items(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    items = db.query(Item).filter(Item.user_id == user.id).order_by(Item.id.desc()).all()
    return [serialize(it) for it in items]


@router.post("/api/items")
@limiter.limit("30/minute")
async def create_item(
    request: Request, body: ItemIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    tags, fallback = await suggest_tags(body.title, body.notes)
    item = Item(title=body.title.strip(), notes=body.notes.strip(), tags=",".join(tags), user_id=user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return serialize(item, fallback)


@router.delete("/api/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Filtering by owner turns "someone else's item" into a plain 404 — no information leak.
    item = db.query(Item).filter(Item.id == item_id, Item.user_id == user.id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
