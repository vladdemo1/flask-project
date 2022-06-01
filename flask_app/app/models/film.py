"""
This mod contains main class about model Film in database
"""

from sqlalchemy import Integer, String, Date, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.main.database import db
from app.models.film_genre import film_genre
from app.models.base_model import BaseModel


class Film(db.Model, BaseModel):
    """
    This is a base film model
    """
    __tablename__ = 'film'

    id = db.Column(Integer, primary_key=True, nullable=False)
    name = db.Column(String(200), nullable=False)
    date = db.Column(Date, nullable=False)
    rating = db.Column(Integer, nullable=False)
    poster = db.Column(String(200), nullable=False)
    description = db.Column(Text)
    director_id = db.Column(Integer, ForeignKey("director.id"), nullable=False)
    user_id = db.Column(Integer, ForeignKey("user.id"), nullable=False)
    genre_id = relationship("Genre", secondary=film_genre)

    def __init__(self, name, date, rating, poster, description, director_id, user_id, genre_id):
        self.name = name
        self.date = date
        self.rating = rating
        self.poster = poster
        self.description = description
        self.director_id = director_id
        self.user_id = user_id
        self.genre_id = genre_id

    def __repr__(self):
        return f"<Film(id={self.id}, name={self.name}, director_id={self.director_id}, " \
               f"user_id={self.user_id}, genre_id={self.genre_id})>"
