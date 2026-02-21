from datetime import datetime, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from app import db
from app.models.pasted import Pasted, PastedCreate
from app.utils import utils


class PastedService:
    def __init__(self, session: Session):
        self.db = session

    def delete_pasted(self, pasted_id: int):
        """Soft deletes a paste row."""
        statement = select(Pasted).where(Pasted.id == pasted_id)
        pasted = self.db.exec(statement).first()

        if not pasted:
            return None

        pasted.is_deleted = True
        self.db.add(pasted)
        self.db.commit()
        self.db.refresh(pasted)

        return pasted

    def get_pasted_by_id(self, pasted_id: int) -> Pasted:
        statement = (
            select(Pasted)
            .where(Pasted.id == pasted_id)
            .where(Pasted.is_deleted == False)
        )
        pasted_item = self.db.exec(statement).first()
        if not pasted_item:
            raise HTTPException(status_code=404, detail="Paste not found")

        pasted_item.view_count += 1

        self.db.add(pasted_item)

        self.db.commit()

        return pasted_item

    def get_pasted_by_shortcode(self, shortcode: str) -> Pasted:
        statement = (
            select(Pasted)
            .where(Pasted.shortcode == shortcode)
            .where(Pasted.is_deleted == False)
        )
        pasted_item = self.db.exec(statement).first()
        if not pasted_item:
            raise HTTPException(status_code=404, detail="Paste not found")

        pasted_item.view_count += 1

        # Commit the update to the database
        self.db.add(pasted_item)
        self.db.commit()

        return pasted_item

    def create_pasted(self, p: PastedCreate) -> Pasted:
        db_paste = Pasted(
            **p.model_dump(),
            shortcode=utils.generateShortCode(),
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(db_paste)
        self.db.commit()
        self.db.refresh(db_paste)

        return db_paste


def get_pasted_service(db: Session = Depends(db.get_session)) -> PastedService:
    """Should be called for each request."""
    return PastedService(db)


PastedServiceDep = Annotated[PastedService, Depends(get_pasted_service)]
