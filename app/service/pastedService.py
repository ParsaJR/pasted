from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from app import db
from app.models.pasted import Duration, Pasted, PastedCreate, PastedExpiryDuration
from app.service.exceptions import ServiceError
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

    def get_pasted_by_id(self, pasted_id: int) -> Pasted|None:
        statement = (
            select(Pasted)
            .where(Pasted.id == pasted_id)
            .where(Pasted.is_deleted == False)  # noqa: E712
        )
        pasted_item = self.db.exec(statement).first()
        if not pasted_item:
            return None

        if pasted_item.duration == Duration.oneTime or pasted_item.is_one_time:
            if pasted_item.view_count >= 1:
                return None

        pasted_item.view_count += 1

        self.db.add(pasted_item)

        self.db.commit()

        return pasted_item

    def get_pasted_by_shortcode(self, shortcode: str) -> Pasted|None:
        statement = (
            select(Pasted)
            .where(Pasted.shortcode == shortcode)
            .where(Pasted.is_deleted == False)  # noqa: E712
        )

        pasted_item = self.db.exec(statement).first()

        if not pasted_item:
            return None


        if pasted_item.duration == Duration.oneTime or pasted_item.is_one_time:
            if pasted_item.view_count >= 1:
                assert pasted_item.id is not None
                _ = self.delete_pasted(pasted_item.id)
                return None

        pasted_item.view_count += 1

        # Commit the update to the database
        self.db.add(pasted_item)
        self.db.commit()

        return pasted_item

    def create_pasted(self, p: PastedCreate) -> Pasted:
        day_amount_statement = select(PastedExpiryDuration).where(PastedExpiryDuration.code == p.expiry_code)

        day_amount = self.db.exec(day_amount_statement).first()
        if not day_amount:
            raise ServiceError("Internal server error")
            
        

        now = datetime.now(timezone.utc)

        expiry_date = now + timedelta(days=day_amount.days)

        db_paste = Pasted(
            **p.model_dump(),
            shortcode=utils.generateShortCode(),
            created_at=now,
            expires_at=expiry_date,
        )

        self.db.add(db_paste)
        self.db.commit()
        self.db.refresh(db_paste)

        return db_paste


def get_pasted_service(db: Session = Depends(db.get_session)) -> PastedService:
    """Should be called for each request."""
    return PastedService(db)


PastedServiceDep = Annotated[PastedService, Depends(get_pasted_service)]
