from core.database import Base
import enum
from sqlalchemy import Column, Integer, String, Double , Enum
from sqlalchemy.orm import relationship


class Role(enum.Enum):
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    fullname = Column(String(255))
    address = Column(String(255))
    phone = Column(String(10))
    available_balance = Column(Double, default=0.00)
    role = Column(Enum(Role), default=Role.STUDENT)
    auth_id = Column(String(36))




