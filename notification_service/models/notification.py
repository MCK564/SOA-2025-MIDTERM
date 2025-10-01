from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from core.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    message = Column(String(255))
    email_to = Column(String(255))
    email_from = Column(String(255))
    subject = Column(String(255))
    date = Column(DateTime, default=datetime.utcnow)

