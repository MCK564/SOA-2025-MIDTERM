

from sqlalchemy import Column, Integer, ForeignKey, String, Double, DateTime, Enum
from sqlalchemy.orm import relationship
from core.database import Base
from models.TuitionStatus import TuitionStatus


class Tuition(Base):
    __tablename__ = "tuitions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    student_id = Column(String(36))
    payer_id = Column(String(36))

    amount = Column(Double, nullable=False)

    status = Column(Enum(TuitionStatus), default=TuitionStatus.NOT_YET_PAID)
    description = Column(String(255))
    expires_at = Column(DateTime)

