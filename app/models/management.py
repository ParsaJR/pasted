from datetime import datetime
import re
from typing import Self

from pydantic import BaseModel, field_validator, model_validator, EmailStr
from sqlmodel import Field, SQLModel


class AdminBase(SQLModel):
    username: str = Field(unique=True)
    email: EmailStr = Field(max_length=50)

    @field_validator("username")
    def username_alphanumeric(cls, v: str):
        assert v.isalnum(), "must be alphanumeric"
        return v


class AdminCreate(AdminBase):
    plain_password: str = Field(min_length=6, max_length=50)
    repeat_password: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.plain_password != self.repeat_password:
            raise ValueError("Passwords do not match!")
        return self

    @field_validator("plain_password")
    def must_contain_number_and_char(cls, value: str) -> str:
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("Password must contain at least one letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number.")
        return value


class Admin(AdminBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    last_logged_in_at: datetime | None = Field(default=None)
    password_reset_required: bool = Field(default=True)
    disabled: bool = False


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
