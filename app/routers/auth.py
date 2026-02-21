from datetime import timedelta
from typing import Annotated

from app.core import config, security
from app.schemas.jwt import Token
from app.service.adminService import AdminService, get_admin_service
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Pasted: Management Auth"], include_in_schema=False)

AdminServiceDep = Annotated[AdminService, Depends(get_admin_service)]


@router.post("/token")
async def login_and_get_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    admin_service: AdminServiceDep,
):

    admin = admin_service.authenticate(form_data.username, form_data.password)

    access_token_expires_at = timedelta(minutes=config.settings.JWT_TTL)

    encoded_token = security.create_access_token(
        data={
            "sub": admin.username,
            "password_change_required": admin.password_reset_required,
        },
        expires_at_delta=access_token_expires_at,
    )

    return Token(access_token=encoded_token, token_type="bearer")
