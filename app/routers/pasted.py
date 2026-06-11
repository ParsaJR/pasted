from fastapi.exceptions import HTTPException
from app.models.pasted import Duration, PastedCreate, PastedPublic
from app.service.pastedService import PastedServiceDep
from fastapi import APIRouter

router = APIRouter(
    tags=["Pasted: Public routes"],
)


@router.get("/pastes/{pasted_id}", response_model=PastedPublic, status_code=200)
async def get_pasted_by_id(pasted_id: int, pasted_service: PastedServiceDep):
    pasted_item = pasted_service.get_pasted_by_id(pasted_id)
    return pasted_item


@router.get("/pastes/", response_model=PastedPublic, status_code=200)
async def get_pasted_by_shortcode(shortcode: str, pasted_service: PastedServiceDep):
    pasted_item = pasted_service.get_pasted_by_shortcode(shortcode)
    if pasted_item is None:
         raise HTTPException(status_code=404, detail="Paste not found")
    return pasted_item


@router.post("/pastes", response_model=PastedPublic, status_code=201)
async def create_pasted(p: PastedCreate, pasted_service: PastedServiceDep):
    pasted_item = pasted_service.create_pasted(p)
    return pasted_item
