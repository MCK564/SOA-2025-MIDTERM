

from sqlalchemy import Column, Integer, ForeignKey, String, Double, DateTime, Enum
from sqlalchemy.orm import relationship
from core.database import Base
from models.TuitionStatus import TuitionStatus


class Tuition(Base):
    __tablename__ = "tuitions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    student_id = Column(String(36), ForeignKey("users.id"))
    student = relationship("User", foreign_keys=[student_id], back_populates="tuitions_as_student")

    payer_id = Column(String(36), ForeignKey("users.id"))
    payer = relationship("User", foreign_keys=[payer_id], back_populates="tuitions_as_payer")

    payments = relationship("Payment", back_populates="tuition")
    amount = Column(Double, nullable=False)
    status = Column(Enum(TuitionStatus), default=TuitionStatus.NOT_YET_PAID)
    description = Column(String(255))
    expires_at = Column(DateTime)

