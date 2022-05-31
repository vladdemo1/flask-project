"""
This mod contains main class about model Genre in database
"""

from sqlalchemy import Integer, String

from app.main.database import db
from app.models.base_model import BaseModel


class Genre(db.Model, BaseModel):
    """
    This is a base genre model
    """
    __tablename__ = 'genre'

    id = db.Column(Integer, primary_key=True, nullable=False)
    genre = db.Column(String(50), nullable=False)

    def __init__(self, genre):
        self.genre = genre

    def __repr__(self):
        return f"<Genre(id={self.id}, genre={self.genre})>"
