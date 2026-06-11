from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


class Duration(Enum):
    oneTime = "0"
    oneDay = "1"
    tenDays = "10"



class PastedExpiryDuration(SQLModel, table=True):
    __tablename__ = "expiry_duration"  # pyright: ignore[reportAssignmentType]

    id: int | None = Field(default=None, primary_key=True)
    name: str # "1 day", "1 week"
    code: str = Field(unique=True,nullable=False)
    days: int # 1, 2, 10
    is_enabled: bool = Field(default=True,index=True)
    

class PastedBase(SQLModel):
    # Roughly 10 Kb in Si system. It seems sensible.
    content: str = Field(max_length=10 * 1024, nullable=False)


class PastedCreate(PastedBase):
    expiry_code: str
    is_one_time: bool


class PastedPublic(PastedBase):
    shortcode: str


class Pasted(PastedBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    shortcode: str = Field(max_length=8, index=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = Field(nullable=False)
    view_count: int = Field(default=0)
    is_deleted: bool = Field(default=False, index=True)
    is_one_time: bool = Field(default=False,index=True)
    duration: Duration
