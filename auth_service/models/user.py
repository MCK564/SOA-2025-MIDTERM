import enum


from sqlalchemy import Column, String, Enum

from core.database import Base


class Role(enum.Enum):
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"

class Login_type(enum.Enum):
    ROPC = "ROPC"  #resource Owner Password Credentials
    FACEBOOK = "FACEBOOK"
    GOOGLE = "GOOGLE"


class Auth(Base):
    __tablename__ = "auth"

    id = Column(String(36), primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    role = Column(Enum(Role), default=Role.STUDENT)
    login_type = Column(Enum(Login_type), default=Login_type.ROPC)

