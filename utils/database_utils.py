from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from core.database import get_db
from models import Tuition
from models.TuitionStatus import TuitionStatus


def mark_expired_tuitions(db: Optional[Session] = None) -> int:
    """
    Find all tuitions past their expiration date that are not already marked as EXPIRED
    and mark them as EXPIRED. Returns the number of records updated.

    If no session is provided, a new one will be obtained and managed internally.
    """
    owns_session = db is None
    session: Session = db or get_db()
    try:
        now = datetime.now()
        expired = (
            session.query(Tuition)
            .filter(Tuition.expires_at < now, Tuition.status != TuitionStatus.EXPIRED)
            .all()
        )
        for tuition in expired:
            tuition.status = TuitionStatus.EXPIRED
        if expired:
            session.commit()
        return len(expired)
    except Exception:
        if owns_session:
            session.rollback()
        raise
    finally:
        if owns_session:
            session.close()



