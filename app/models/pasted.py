from datetime import datetime, timezone
from enum import Enum
from sqlmodel import SQLModel, Field


class Duration(Enum):
    oneTime = "0"
    oneDay = "1"
    tenDays = "10"


class PastedBase(SQLModel):
    # Roughly 10 Kb in Si system? It seems sensible.
    content: str = Field(max_length=10 * 1024, nullable=False)


class PastedCreate(PastedBase):
    duration: Duration


class PastedPublic(PastedBase):
    shortcode: str


class Pasted(PastedBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    shortcode: str = Field(max_length=8, index=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    view_count: int = Field(default=0)
    is_deleted: bool = Field(default=False, index=True)
    duration: Duration
