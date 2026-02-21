from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select

from app.core import security
from app.dependencies.database import SessionDep
from app.models.management import Admin

oauth2_scheme = OAuth2PasswordBearer("/token")


async def get_current_active_admin(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
):

    generic_exception = HTTPException(
        status_code=401,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = security.verify_token(token)
    except Exception:
        raise generic_exception

    sub = payload.get("sub")
    if not sub:
        raise generic_exception

    password_change_required = payload.get("password_change_required")

    if password_change_required:
        raise HTTPException(
            status_code=403,  # 403 means, "i know who you are, but ..."
            detail="Reset your password, before doing anything else",
        )

    admin = session.exec(select(Admin).where(Admin.email == sub)).first()

    if not admin:
        raise generic_exception

    return admin


ProtectedRouteDep = Annotated[Admin, Depends(get_current_active_admin)]
