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

    admin = session.exec(
        select(Admin).where(Admin.email == sub)
    ).first()

    if not admin:
        raise generic_exception

    return admin  


ProtectedRouteDep = Annotated[Admin,Depends(get_current_active_admin)]
