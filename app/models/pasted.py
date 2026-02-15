from datetime import datetime, timezone
from enum import Enum
from sqlmodel import SQLModel, Field


class Duration(Enum):
    oneTime = "0"
    oneDay = "1"
    tenDays = "10"


class PastedBase(SQLModel):
    content: str


class PastedCreate(PastedBase):
    duration: Duration


class PastedPublic(PastedBase):
    id: int
    shortcode: str


class Pasted(PastedBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    shortcode: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    view_count: int = Field(default=0)
    is_deleted: bool = Field(default=False, index=True)
    duration: Duration
