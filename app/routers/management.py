from app.dependencies.admin import ProtectedRouteDep
from app.models.management import AdminPasswordChange
from app.routers.auth import AdminServiceDep
from fastapi import APIRouter, HTTPException, Response
from app.core import security

from app.schemas.management import APICapabilities
from app.service.pastedService import PastedServiceDep

router = APIRouter(
    tags=["Pasted: Management routes"],
    prefix="/management",
)


@router.get("/what-is-available", response_model=APICapabilities, status_code=200)
def api_capabilities(admin_service: AdminServiceDep, response: Response):
    response.headers["Cache-Control"] = "public, max-age=30"
    print("ASsadsa")
    return admin_service.get_api_capabilities()


@router.delete("/pastes/{pasted_id}", status_code=204)
async def DeletePasted(
    pasted_id: int, pasted_service: PastedServiceDep, admin: ProtectedRouteDep
):
    pasted = pasted_service.delete_pasted(pasted_id)
    if not pasted:
        raise HTTPException(status_code=404, detail="Paste not found.")


@router.post("/change-password", status_code=204)
async def ChangePassword(
    admin_service: AdminServiceDep, admin: ProtectedRouteDep, body: AdminPasswordChange
):

    admin_service.change_password(
        admin.username, body.current_password, body.new_password
    )
