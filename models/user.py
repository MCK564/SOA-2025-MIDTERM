import enum
from sqlalchemy import Column, Integer, String, Double , Enum
from sqlalchemy.orm import relationship

from core.database import Base

class Role(enum.Enum):
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    fullname = Column(String(255))
    phone = Column(String(10))
    available_balance = Column(Double, default=0.00)
    role = Column(Enum(Role), default=Role.STUDENT)

    payments = relationship("Payments", back_populates="user")
    tuitions = relationship("Tuition", back_populates="user")

