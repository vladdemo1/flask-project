"""
This mod contains main class about model Genre in database
"""

from sqlalchemy import Column, Integer, String

from app.main.database import Base


class Genre(Base):
    """
    This is a base genre model
    """
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True, nullable=False)
    genre = Column(String(50), nullable=False)

    def __init__(self, genre):
        self.genre = genre

    def __repr__(self):
        return f"<Genre(id={self.id}, genre={self.genre})>"
