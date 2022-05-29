"""
This mod contains main class about model FilmGenre in database
"""

from sqlalchemy import Column, Table
from sqlalchemy import ForeignKey

from app.main.database import Base

film_genre = Table(
    "film_genre",
    Base.metadata,
    Column("film_id", ForeignKey("film.id")),
    Column("genre_id", ForeignKey("genre.id")),
)
