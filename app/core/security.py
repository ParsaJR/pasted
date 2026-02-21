from datetime import datetime, timezone, timedelta
from typing import Any
from pwdlib import PasswordHash
import jwt
from app.core import config


JWT_SECRET = config.settings.JWT_Secret
ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str) -> str:
    return password_hash.hash(plain_password)


def create_access_token(
    data: dict[str, Any], expires_at_delta: timedelta | None = None
) -> str:
    """Returns the "JWT Encoded json" To be returned to the user."""

    to_encode = data.copy()

    if expires_at_delta:
        expire = datetime.now(timezone.utc) + expires_at_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verifies the validity of the token, and if it's valid, It returns the decoded jwt dictionary."""
    try:
        payload = jwt.decode(token, config.settings.JWT_Secret, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has been expired.")
    except jwt.InvalidTokenError:
        raise Exception("Token is invalid.")
