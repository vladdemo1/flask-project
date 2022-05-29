"""
This mod contains main class about model User in database
"""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy_utils import EmailType

from app.main.database import Base


class User(Base):
    """
    This is a base user model
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    name = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    def __init__(self, email, name, password, admin):
        self.email = email
        self.name = name
        self.password = password
        self.admin = admin

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, admin={self.admin})>"
