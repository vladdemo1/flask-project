"""
This mod contains main class about model Director in database
"""

from sqlalchemy import Column, Integer, String

from app.main.database import Base


class Director(Base):
    """
    This is a base director model
    """
    __tablename__ = 'director'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Director(id={self.id}, name={self.name})>"
