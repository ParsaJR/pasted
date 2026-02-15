from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, select

from app import db
from app.models.pasted import Pasted


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


def get_pasted_service(db: Session = Depends(db.get_session)) -> PastedService:
    """Should be called for each request."""
    return PastedService(db)


PastedServiceDep = Annotated[PastedService, Depends(get_pasted_service)]
