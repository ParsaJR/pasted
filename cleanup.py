from datetime import datetime, timedelta, timezone
from sqlmodel import select

from app.db import get_session
from app.models.pasted import Pasted


deletedEntities = 0

session = get_session()

session = next(session)

fifteen_days_ago = datetime.now(tz=timezone.utc) - timedelta(minutes=10)
statement = select(Pasted).where(Pasted.created_at < fifteen_days_ago)
candidates = session.exec(statement).all()


for candidate in candidates:
    candidate.is_deleted = True
    deletedEntities += 1

session.bulk_save_objects(candidates)
session.commit()

print(f"Done. Soft Deleted {deletedEntities} rows.")
