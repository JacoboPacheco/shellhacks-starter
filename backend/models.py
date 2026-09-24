from sqlalchemy import ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)


class Upload(Base):
    # Files live in the database, not on disk, so they survive redeploys on hosts
    # with no persistent filesystem (Render free tier). 5MB max each — see uploads.py.
    __tablename__ = "uploads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    content_type: Mapped[str] = mapped_column(String(64))
    data: Mapped[bytes] = mapped_column(LargeBinary)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)


class Item(Base):
    # EXAMPLE table for items.py — copy the shape, then delete or rename it.
    # Keep columns nullable-friendly and plain (String, not Enum): a column added
    # mid-event is created automatically on startup, but only as a nullable column.
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    notes: Mapped[str] = mapped_column(String(2000), default="")
    tags: Mapped[str] = mapped_column(String(120), default="")  # comma-separated
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
