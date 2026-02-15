from datetime import datetime
from typing import Self

from pydantic import BaseModel, model_validator
from sqlmodel import Field, SQLModel


class AdminBase(SQLModel):
    username: str = Field(unique=True)
    email: str
    disabled: bool = False


class AdminCreate(AdminBase):
    plain_password: str


class Admin(AdminBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    last_logged_in_at: datetime | None = Field(default=None)
    needs_to_reset_password: bool = Field(default=True)


class AdminPasswordChange(BaseModel):
    """Used for the password-change operation"""

    current_password: str
    new_password: str
    repeat_new_password: str

    @model_validator(mode="after")
    def check_password_match(self) -> Self:
        if self.new_password != self.repeat_new_password:
            raise ValueError("Passwords do not match")
        return self
