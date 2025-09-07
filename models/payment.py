import enum

from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, String,Double, Enum, DateTime
from sqlalchemy.orm import relationship
from core.database import Base

class PaymentStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"
    PAID = "PAID"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    amount = Column(Double, nullable=False)
    status = Column(Enum(PaymentStatus))
    date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String(36), ForeignKey("users.id"))
    user = relationship("User", back_populates="payments")

    tuition_id = Column(Integer, ForeignKey("tuitions.id"))
    tuition = relationship("Tuition", back_populates="payments")