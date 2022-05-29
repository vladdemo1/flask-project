"""
This mod contains main class about model Film in database
"""

from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.main.database import Base
from app.models.film_genre import film_genre


class Film(Base):
    """
    This is a base film model
    """
    __tablename__ = 'film'

    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(Date, nullable=False)
    rating = Column(Integer, nullable=False)
    poster = Column(String(200), nullable=False)
    description = Column(Text)
    director_id = Column(Integer, ForeignKey("director.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    genre_id = relationship("Genre", secondary=film_genre)

    def __init__(self, date, rating, poster, description, director_id, user_id, genre_id):
        self.date = date
        self.rating = rating
        self.poster = poster
        self.description = description
        self.director_id = director_id
        self.user_id = user_id
        self.genre_id = genre_id

    def __repr__(self):
        return f"<Film(id={self.id}, director_id={self.director_id}, user_id={self.user_id}, genre_id={self.genre_id})>"
