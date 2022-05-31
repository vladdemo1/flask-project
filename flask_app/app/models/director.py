"""
This mod contains main class about model Director in database
"""

from sqlalchemy import Integer, String

from app.main.database import db
from app.models.base_model import BaseModel


class Director(db.Model, BaseModel):
    """
    This is a base director model
    """
    __tablename__ = 'director'

    id = db.Column(Integer, primary_key=True, nullable=False)
    name = db.Column(String(50), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Director(id={self.id}, name={self.name})>"
