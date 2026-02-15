from datetime import datetime, timezone

from sqlmodel import select

from app.dependencies.database import SessionDep
from app.models import pasted
from app.utils import utils
from fastapi import APIRouter, HTTPException

router = APIRouter(
    tags=["Pasted: Public routes"],
)


@router.get("/pastes/{pasted_id}", response_model=pasted.PastedPublic, status_code=200)
async def GetPasted(pasted_id: int, session: SessionDep):
    statement = select(pasted.Pasted).where(pasted.Pasted.id == pasted_id)
    pasted_item = session.exec(statement).first()
    if not pasted_item:
        raise HTTPException(status_code=404, detail="Pasted not found.")
    return pasted_item


@router.post("/pastes", response_model=pasted.PastedPublic)
async def CreatePasted(p: pasted.PastedCreate, session: SessionDep):
    db_paste = pasted.Pasted(
        **p.model_dump(),
        shortcode=utils.generateShortCode(),
        created_at=datetime.now(timezone.utc),
    )
    session.add(db_paste)
    session.commit()
    session.refresh(db_paste)
    return db_paste
